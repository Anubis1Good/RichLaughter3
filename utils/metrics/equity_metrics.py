import numpy as np
from scipy.stats import linregress

def equity_curve_metrics(eq, eps=1e-12):
    """
    eq — одномерный массив (equity_fee / equity по сделкам).
    Возвращает dict с метриками линейности и риска.
    Все 'norm'-метрики делятся на масштаб, чтобы сравнивать роботов
    с разной прибылью/длиной ряда.
    """
    y = np.asarray(eq, dtype=float)
    n = len(y)
    out = {}
    if n < 3:
        # вырожденный случай
        for k in ('r2', 'rmse_reg', 'rmse_reg_norm', 'max_dev_reg',
                  'max_dev_reg_norm', 'l1_mean_reg', 'slope_reg',
                  'max_dd', 'max_dd_norm', 'jump_ratio', 'sharpe',
                  'total_return', 'calmar', 'linearity_score'):
            out[k] = 0.0
        return out

    x = np.arange(n)
    y0, yN = y[0], y[-1]
    total = yN - y0
    scale = abs(total) if abs(total) > eps else (np.std(y) + eps)

    # --- регрессия ---
    res = linregress(x, y)
    slope = res.slope
    intercept = res.intercept
    line_reg = intercept + slope * x
    resid_reg = y - line_reg
    ss_res = np.sum(resid_reg ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2) + eps
    r2 = 1.0 - ss_res / ss_tot
    rmse_reg = np.sqrt(np.mean(resid_reg ** 2))
    max_dev_reg = np.max(np.abs(resid_reg))

    # --- хорда ---
    chord = y0 + (total / (n - 1)) * x
    resid_ch = y - chord
    rmse_ch = np.sqrt(np.mean(resid_ch ** 2))
    max_dev_ch = np.max(np.abs(resid_ch))
    l1_mean_ch = np.mean(np.abs(resid_ch))

    # --- просадка ---
    running_max = np.maximum.accumulate(y)
    dd = running_max - y
    max_dd = np.max(dd)

    # --- шаговые метрики ---
    diffs = np.diff(y)
    mean_step = np.mean(np.abs(diffs)) + eps
    max_step = np.max(np.abs(diffs))
    jump_ratio = max_step / mean_step

    # --- Sharpe по приращениям (без rf) ---
    std_d = np.std(diffs)
    sharpe = np.mean(diffs) / std_d if std_d > eps else 0.0

    out.update({
        'total_return': total,
        'slope_reg': slope,
        'r2': r2,
        'rmse_reg': rmse_reg,
        'rmse_reg_norm': rmse_reg / scale,
        'max_dev_reg': max_dev_reg,
        'max_dev_reg_norm': max_dev_reg / scale,
        'l1_mean_chord': l1_mean_ch,
        'rmse_chord': rmse_ch,
        'max_dev_chord': max_dev_ch,
        'max_dd': max_dd,
        'max_dd_norm': max_dd / scale,
        'jump_ratio': jump_ratio,
        'sharpe': sharpe,
        'calmar': total / (max_dd + eps),
    })

    # --- композитный linearity_score (пример, калибруй веса) ---
    # Нормируем в 0..1: R² уже 0..1, штрафы ограничиваем
    out['linearity_score'] = (
        0.5 * max(0.0, min(1.0, r2))
        + 0.2 * max(0.0, 1.0 - min(1.0, out['rmse_reg_norm']))
        + 0.2 * max(0.0, 1.0 - min(1.0, out['max_dd_norm']))
        + 0.1 * max(0.0, 1.0 - min(1.0, jump_ratio / 20.0))
    )
    return out

def composite_score(total_return, metrics,
                    w=(1.0, 0.6, 0.5, 0.5, 0.3),   # <-- 5 весов: total, r2, lin, dd, jump
                    ref=None):
    """
    total_return — curve_total_return (или total_fee_per)
    ref — пока не используется (задел под нормировку по популяции).
    """
    # --- защита от неверной длины w ---
    if len(w) != 5:
        raise ValueError(f"composite_score: w must have 5 elements, got {len(w)}")

    r2   = max(0.0, min(1.0, metrics['r2']))
    lin  = metrics['linearity_score']
    dd   = 1.0 - min(1.0, metrics['max_dd_norm'])
    jump = 1.0 - min(1.0, metrics['jump_ratio'] / 20.0)
    tr = np.sign(total_return) * np.log1p(abs(total_return))
    return (w[0] * tr
            + w[1] * r2
            + w[2] * lin
            + w[3] * dd
            + w[4] * jump)

def lex_score(em, tr_eps=0.01, dd_limit=1.0):
    """
    Лексикографический скор для maximize.
    Приоритет 1: прибыль (curve_total_return), с шагом tr_eps.
    Приоритет 2: среди «почти равных по прибыли» — качество кривой.
    Приоритет 3: жёсткий штраф за катастрофическую просадку.
    """
    tr = em['total_return']
    dd = em['max_dd_norm']

    # квантуем прибыль: роботы в пределах tr_eps считаются «равными»
    tr_bucket = np.floor(tr / tr_eps)

    # качество в 0..1 (r2 уже 0..1, lin уже 0..1, dd/jump — штрафы)
    quality = (0.5 * max(0.0, min(1.0, em['r2']))
               + 0.3 * em['linearity_score']
               + 0.2 * (1.0 - min(1.0, dd)))

    # штраф за запредельную просадку — ниже любого «прошедшего»
    if dd > dd_limit or tr <= 0:
        return -1e6 + tr_bucket + quality   # всё равно упорядочено по tr

    return tr_bucket * 10.0 + quality       # прибыль доминирует, качество — tie-break