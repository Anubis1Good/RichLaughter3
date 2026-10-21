import pandas as pd
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

"""
Как интерпретировать результат
После добавления колонки fdi вы можете использовать её в стратегии:

FDI ≤ 1.5 (ближе к 1): Рынок в тренде (движение более линейное). Значения ниже 1.5 часто считаются сигналом к трендовой торговле .

FDI ≥ 1.5 (ближе к 2): Рынок в боковике или хаотичном движении. Значения выше 1.65 (например) могут сигнализировать о флэте .

Порог: В примере с TradingView часто используется порог 1.65 для определения "гладкого" (трендового) режима .

Важное замечание
Параметр period (окно) сильно влияет на результат. Для дневных графиков часто берут 60–100 баров. Если окно слишком короткое, индикатор будет шумным; если слишком длинное — он станет запаздывающим.
"""

def add_fractal_dimension_index(df: pd.DataFrame, period: int = 60, price_col: str = 'close'):
    """
    Добавляет 'fdi' (Fractal Dimension Index) по методу Хигучи (упрощённый).
    Векторизованный вариант, эквивалентный исходному коду.
    """
    price = df[price_col].values
    
    # L(1): |price[t] - price[t-1]|, среднее по окну
    abs_diff_1 = np.abs(np.diff(price, prepend=np.nan))
    L1 = pd.Series(abs_diff_1).rolling(window=period).mean().values
    
    # L(4): |price[t] - price[t-4]| / 4, среднее по окну
    # ВАЖНО: это разность с шагом 4, а НЕ diff 4-го порядка!
    abs_diff_4 = np.full_like(price, np.nan, dtype=float)
    abs_diff_4[4:] = np.abs(price[4:] - price[:-4])
    L4 = pd.Series(abs_diff_4).rolling(window=period).mean().values / 4
    
    # ratio = L1 / L4 с защитой
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = L1 / L4
        fdi = np.log(ratio) / np.log(4) + 1
    
    fdi[~np.isfinite(fdi)] = np.nan
    df['fdi'] = np.clip(fdi, 1.0, 2.0)
    
    return df

"""
H > 0.55 → тренд (персистентность)

H ≈ 0.5 → случайное блуждание

H < 0.45 → возврат к среднему
"""

def add_hurst_exponent(df: pd.DataFrame, period: int = 60, price_col: str = 'close'):
    """
    Добавляет колонку 'hurst' (показатель Хёрста) через векторизованный R/S-анализ.
    Быстрый вариант: все операции — скользящие max/min/std/sum на C-уровне.
    
    :param df: DataFrame с колонкой цены
    :param period: Окно расчёта (рекомендуется 100+)
    :param price_col: Колонка с ценой
    :return: DataFrame с добавленной колонкой 'hurst'
    """
    # Логарифмические доходности (стационарный ряд для R/S)
    log_ret = np.log(df[price_col] / df[price_col].shift(1))
    
    # Кумулятивная сумма отклонений от скользящего среднего (Y)
    # Считаем через rolling mean и cumsum — это ключ к векторизации
    roll_mean = log_ret.rolling(window=period).mean()
    deviations = log_ret - roll_mean
    # Кумулятивная сумма отклонений внутри окна:
    # cumsum по всему ряду минус cumsum, сдвинутый на period (граница окна)
    cum_dev = deviations.cumsum()
    # Значение кумулятивной суммы на левой границе окна (за period баров назад)
    cum_dev_shifted = cum_dev.shift(period)
    # Кумулятивная сумма отклонений внутри текущего окна
    y = cum_dev - cum_dev_shifted
    
    # Размах R = max(Y) - min(Y) внутри окна
    roll_max = y.rolling(window=period).max()
    roll_min = y.rolling(window=period).min()
    R = roll_max - roll_min
    
    # Стандартное отклонение S внутри окна
    S = log_ret.rolling(window=period).std()
    
    # Нормированный размах R/S
    rs = R / S.replace(0, np.nan)
    
    # Оценка H: H ≈ log(R/S) / log(period/2)
    df['hurst'] = (np.log(rs) / np.log(period / 2)).clip(lower=0.0, upper=1.0)
    
    return df

"""
Vertical Horizontal Filter (VHF) — это индикатор, который измеряет силу тренда, сравнивая пройденное ценой расстояние с общим «шумом» (суммой всех колебаний). Чем ближе значение к 1, тем более направленным было движение; чем ближе к 0, тем более хаотичным был рынок .

📊 Интерпретация
Рост VHF: Тренд усиливается (цена движется в одном направлении) .

Падение VHF: Рынок переходит в боковик или консолидацию .

Экстремумы: Слишком высокие значения могут предупреждать о возможной коррекции, а низкие — о скором начале тренда .
"""
def add_vhf(df: pd.DataFrame, period: int = 28, price_col: str = 'close'):
    """
    Добавляет 'vhf' (Vertical Horizontal Filter) по Адаму Уайту.
    
    :param df: DataFrame с колонкой цены
    :param period: Период расчёта (по умолчанию 28)
    :param price_col: Колонка с ценой
    :return: DataFrame с добавленной колонкой 'vhf'
    """
    # Извлекаем цены как numpy-массив для скорости
    close = df[price_col].values
    
    # Числитель: размах за период (Max - Min)
    # Используем pandas rolling для векторизации
    rolling_max = pd.Series(close).rolling(window=period).max()
    rolling_min = pd.Series(close).rolling(window=period).min()
    num = rolling_max - rolling_min
    
    # Знаменатель: сумма абсолютных изменений за период
    # abs_diff = |Close[t] - Close[t-1]|
    abs_diff = np.abs(np.diff(close, prepend=np.nan))
    den = pd.Series(abs_diff).rolling(window=period).sum()
    
    # Расчёт VHF с защитой от деления на ноль (если нет движения)
    # Если den == 0 (цена стоит на месте), VHF = 0
    df['vhf'] = (num / den.replace(0, np.nan)).fillna(0.0)
    
    return df


"""
Смысл простой: если доходности независимы (случайное блуждание), то дисперсия суммы = сумме дисперсий, и VR = 1. Любое отклонение от 1 — это след автокорреляции:

Значение	Что означает	Рыночный режим
VR ≈ 1	Доходности независимы	Случайное блуждание, нет памяти
VR > 1	q-периодная дисперсия больше, чем q·однопериодная	Положительная автокорреляция — тренд (моментум)
VR < 1	q-периодная дисперсия меньше	Отрицательная автокорреляция — возврат к среднему
Интуиция: при тренде движение «складывается» — несколько баров подряд в одну сторону дают большой размах, дисперсия растёт быстрее линейного → VR > 1. При возврате к среднему движение «гасится» — рост сменяется падением, размах меньше → VR < 1.

Практическая шкала (стандартное нормальное приближение):

vr_z	Что означает
> +1.96	VR значимо > 1 → тренд (p < 0.05)
< −1.96	VR значимо < 1 → возврат к среднему (p < 0.05)
−1.96 … +1.96	Статистически не отличимо от случайного блуждания
То есть vr говорит в какую сторону, а vr_z — насколько этому можно верить. Одно без другого малоинформативно: vr = 1.3 при vr_z = 0.4 — это шум, а vr = 1.15 при vr_z = 3.2 — сильный сигнал.
"""

def add_variance_ratio(df: pd.DataFrame, period: int = 60, q: int = 4, price_col: str = 'close'):
    """
    Добавляет 'vr' (Variance Ratio) и 'vr_z' (z-статистика Lo-MacKinlay Z2),
    рассчитанные в скользящем окне `period`. Результат пишется в последнюю
    строку каждого окна (т.е. в бар t для окна [t-period+1 ... t]).
    
    Полностью детерминирован в окне: значение в строке t зависит только
    от цен [t-period ... t] (period+1 цена для period доходностей).
    
    :param df: DataFrame с колонкой цены
    :param period: Размер окна в барах доходностей (рекомендуется 100+)
    :param q: Горизонт агрегации (по умолчанию 4)
    :param price_col: Колонка с ценой
    :return: DataFrame с колонками 'vr' и 'vr_z'
    """
    price = df[price_col].values.astype(float)
    
    # Логарифмические доходности: r[t] = log(P[t] / P[t-1])
    # Длина n-1, r[0] соответствует t=1
    log_ret = np.full_like(price, np.nan)
    log_ret[1:] = np.log(price[1:] / price[:-1])
    
    n = len(log_ret)
    df['vr'] = np.nan
    df['vr_z'] = np.nan
    
    # Нужно period доходностей в окне → окно длиной period+1 цена
    # Первый валидный бар: индекс period (нужно period доходностей начиная с r[1])
    if n < period + 1 or period < q + 2:
        return df
    
    # Берём доходности без первого NaN: r[1:] длины n-1
    rets = log_ret[1:]  # длина n-1, rets[i] соответствует t=i+1
    
    # Окна по period доходностей: shape (n-1-period+1, period) = (n-period, period)
    windows = sliding_window_view(rets, period)
    
    # --- Векторизованный расчёт по всем окнам ---
    # mu: среднее по окну, shape (num_windows,)
    mu = windows.mean(axis=1, keepdims=True)
    demeaned = windows - mu  # (W, period)
    
    # var_1 = sum(demeaned^2) / (period - 1)
    var_1 = np.sum(demeaned ** 2, axis=1) / (period - 1)
    
    # q-периодные перекрывающиеся доходности внутри окна:
    # q_rets[i] = sum_{j=0}^{q-1} r_{i+j},  i = 0..period-q
    # Реализуем через cumsum по оси 1
    csum = np.cumsum(windows, axis=1)  # (W, period)
    # q_rets: (W, period - q + 1)
    q_rets = csum[:, q - 1:] - np.concatenate(
        [np.zeros((windows.shape[0], 1)), csum[:, :-q]], axis=1
    ) if q > 1 else csum
    # Проверка формы: period - q + 1
    q_rets = q_rets[:, :period - q + 1]
    
    # m = q * (period - q + 1) * (1 - q / period)  — поправка на перекрытие
    m = q * (period - q + 1) * (1 - q / period)
    q_demeaned = q_rets - q * mu  # mu broadcast (W,1)
    var_q = np.sum(q_demeaned ** 2, axis=1) / m
    
    # VR = var_q / var_1
    with np.errstate(divide='ignore', invalid='ignore'):
        vr = var_q / var_1
    
    # --- Гетероскедастичная дисперсия (Lo-MacKinlay Z2) ---
    sq = demeaned ** 2  # (W, period)
    sum_sq = np.sum(sq, axis=1)  # (W,)
    
    theta = np.zeros(windows.shape[0])
    for j in range(1, q):
        # delta_j = period * sum(sq[:, j:] * sq[:, :-j]) / sum_sq^2
        prod = np.sum(sq[:, j:] * sq[:, :-j], axis=1)
        with np.errstate(divide='ignore', invalid='ignore'):
            delta_j = period * prod / (sum_sq ** 2)
        weight = (2 * (q - j) / q) ** 2
        theta += weight * delta_j
    
    with np.errstate(divide='ignore', invalid='ignore'):
        vr_z = (vr - 1) / np.sqrt(theta)
    
    # Чистим inf/nan
    vr = np.where(np.isfinite(vr), vr, np.nan)
    vr_z = np.where(np.isfinite(vr_z), vr_z, np.nan)
    
    # Индексы последних баров окон в df:
    # windows[i] соответствует доходностям rets[i : i+period],
    # rets[i] = log_ret[i+1] → последний бар окна = i + period в df
    # i = 0..n-period-1 → индексы df: period .. n-1
    df.loc[df.index[period:], 'vr'] = vr
    df.loc[df.index[period:], 'vr_z'] = vr_z
    
    return df

"""
Основная идея: вы берёте размах (High − Low) за некое окно, нормируете его (например, в проценты от цены) и считаете Z-скор относительно того, каким этот размах был в прошлом.

Z ≈ 0: Текущий диапазон в пределах нормы. Рынок «как обычно».

Z < 0 (отрицательный): Диапазон уже исторической нормы. Это и есть «сжатие» (compression). Чем ниже значение (например, ниже −1.5 или −2), тем более аномально узок рынок и тем выше вероятность скорого выхода из этого состояния .

Z > 0 (положительный): Диапазон шире обычного. Расширение волатильности (после новостей, пробоев) .

Важно: сам по себе отрицательный Z-скор не даёт направления сделки. Он лишь говорит: «рынок сжат, готовься». Направление выхода определяется другими инструментами (пробоем уровня, объемом, CVD) .
"""

def add_range_compression_zscore(df: pd.DataFrame, period: int = 60, price_col: str = 'close'):
    """
    Добавляет 'rc_z' (Range Compression Z-Score).
    Считает Z-скор текущего размаха (High-Low) относительно его
    собственного распределения за скользящее окно `period`.
    
    Значение пишется в последнюю строку окна (детерминировано в окне).
    Отрицательные значения = сжатие диапазона.
    
    :param df: DataFrame с колонками 'high' и 'low' (или только цена)
    :param period: Окно для исторического среднего и std размаха
    :param price_col: Если нет 'high'/'low', используется эта колонка для range = 0
    :return: DataFrame с колонкой 'rc_z'
    """
    # Проверяем наличие high/low, иначе используем цену (но range будет 0)
    if 'high' in df.columns and 'low' in df.columns:
        high = df['high'].values.astype(float)
        low = df['low'].values.astype(float)
    else:
        # Fallback: если нет high/low, используем close как high и low (range=0, Z-score не имеет смысла)
        # Лучше требовать high/low, но для совместимости оставим заглушку
        high = df[price_col].values.astype(float)
        low = df[price_col].values.astype(float)
    
    # Текущий размах в процентах от цены (нормировка для сопоставимости)
    # Используем close как базу, но можно и open
    price = df[price_col].values.astype(float) if price_col in df.columns else (high + low) / 2
    
    # Range % = (High - Low) / Price * 100
    # Защита от деления на ноль
    with np.errstate(divide='ignore', invalid='ignore'):
        range_pct = (high - low) / price * 100
    
    # Z-скор: (текущий range - среднее range) / std range
    # Всё считается в скользящем окне period
    range_series = pd.Series(range_pct)
    mean_range = range_series.rolling(window=period).mean().values
    std_range = range_series.rolling(window=period).std().values
    
    with np.errstate(divide='ignore', invalid='ignore'):
        rc_z = (range_pct - mean_range) / std_range
    
    # Чистим inf/nan
    rc_z = np.where(np.isfinite(rc_z), rc_z, np.nan)
    
    # Пишем в последнюю строку окна: результат для бара t доступен только когда окно [t-period+1 ... t] заполнено
    # rolling уже даёт NaN для первых period-1 баров, что корректно
    df['rc_z'] = rc_z
    
    return df

"""
📊 Интерпретация
≈ 50: Текущее значение — медиана окна. Нейтральная зона.

> 80–90: Значение в верхней части исторического распределения. Для цены — потенциальная перекупленность или пробой вверх; для волатильности — расширение.

< 10–20: Значение в нижней части распределения. Для цены — потенциальная перепроданность; для волатильности — сжатие.

Экстремумы (0 или 100): Текущее значение — абсолютный максимум/минимум за окно.

Важно: процентиль не говорит о направлении, он лишь показывает относительное положение значения в его собственной истории.
"""

def add_percentile_rank(df: pd.DataFrame, period: int = 60, col: str = 'close', out_col: str = 'pct_rank'):
    """
    add 'pct_rank' \n
    Добавляет `out_col` — процентильный ранг текущего значения `col`
    относительно его распределения в скользящем окне `period`.
    
    Значение в баре t зависит только от данных [t-period+1 ... t]
    (детерминировано в окне).
    
    :param df: DataFrame с колонкой `col`
    :param period: Размер окна
    :param col: Колонка, для которой считается процентиль
    :param out_col: Имя выходной колонки
    :return: DataFrame с добавленной колонкой
    """
    values = df[col].values.astype(float)
    n = len(values)
    
    # Результат: процентиль в диапазоне [0, 100]
    pct = np.full(n, np.nan)
    
    if n < period:
        df[out_col] = pct
        return df
    
    # Используем sliding_window_view для векторизации по всем окнам сразу
    # Каждое окно: values[i : i+period], последний бар окна — i+period-1

    windows = sliding_window_view(values, period)  # shape (n-period+1, period)
    
    # Текущее значение (последний элемент каждого окна)
    current = windows[:, -1:]  # shape (W, 1)
    
    # Процентиль = доля значений в окне, которые <= текущего * 100
    # Сравниваем каждое значение окна с текущим (broadcast)
    # <= даёт bool, mean по оси 1 даёт долю в [0,1]
    # Умножаем на 100 и округляем до 2 знаков для читаемости
    pct_vals = (windows <= current).mean(axis=1) * 100.0
    
    # Записываем в последний бар каждого окна
    # windows[i] соответствует df.index[i + period - 1]
    pct[period - 1:] = pct_vals
    
    df[out_col] = pct
    return df

"""
Поскольку веса в примере суммируются в 1.0, а каждый компонент нормирован примерно в [-1, +1], итоговый скор лежит в диапазоне [-1, +1] (на практике — чуть уже, из-за fillna(0) и клиппинга).

Диапазон	Что означает	Действие
> +0.5	Сильный тренд вверх: VR значим, FDI низкий, Hurst > 0.5, сжатия нет	Разрешить трендовые лонги, полный размер
+0.2 … +0.5	Умеренный тренд вверх, но не все метрики согласны	Трендовые лонги с уменьшенным размером
−0.2 … +0.2	Серая зона: метрики противоречат друг другу или всё около нейтрали	Не торговать по тренду; ждать
−0.5 … −0.2	Умеренный тренд вниз / слабость	Трендовые шорты с уменьшенным размером
< −0.5	Сильный тренд вниз: VR значим отрицательно, FDI низкий, Hurst > 0.5	Разрешить трендовые шорты, полный размер
Важно: знак скора — это направление режима, а не сигнал входа. Скор > +0.5 говорит «сейчас тренд вверх статистически подтверждён», но точку входа всё равно даёт ваша основная логика (пробой, откат).
"""
def add_composite_blender_score(df: pd.DataFrame):
    """
    Пример композитного скора из уже рассчитанных индикаторов.
    Требует наличия колонок: 'vr_z', 'fdi', 'hurst', 'rc_z'
    """
    # Нормализуем каждый индикатор в диапазон примерно [-1, 1] или [0, 1]
    # Это простая эвристика, логику можно настроить под стратегию
    vr_norm = df['vr_z'].clip(-2, 2) / 2  # -1..1
    fdi_norm = (1.5 - df['fdi']) / 0.5     # >1 = тренд (положительно)
    hurst_norm = (df['hurst'] - 0.5) * 4   # >0.5 = тренд (положительно)
    rc_norm = df['rc_z'].clip(-2, 2) / -2  # сжатие (отрицательный rc_z) = положительно
    
    # Взвешенная сумма (веса подбираются)
    df['blender_score'] = (
        0.3 * vr_norm.fillna(0) +
        0.3 * fdi_norm.fillna(0) +
        0.2 * hurst_norm.fillna(0) +
        0.2 * rc_norm.fillna(0)
    )
    return df