def fix_supertrend_params(period, multiplier, max_period):
    """
    Корректирует параметры супертренда.
    Приоритет: сохраняем множитель, уменьшаем период.
    """
    if period * multiplier >= max_period:
        # Уменьшаем период
        period = int(max_period / multiplier)
        # Минимальный период 3
        period = max(period, 3)
    
    return period

def fix_two_periods(period1,period2,max_period):
    max_total = (max_period // 3) * 2
    total = period1 + period2

    if total > max_total:
        ratio = max_total / total
        period1 = int(period1 * ratio)
        period2 = int(period2 * ratio)
    if period1 < 2:
        dif = 2 - period1
        period1 += dif
        period2 -= dif
    if period2 < 2:
        dif = 2 - period2
        period2 += dif
        period1 -= dif
    return period1,period2

def fix_two_periods_hm(period1,period2,max_period):
    total = period1 + period2
    if total > max_period:
        ratio = max_period / total
        period1 = int(period1 * ratio)
        period2 = int(period2 * ratio)
    if period1 < 2:
        period1 = 2
    if period2 < 2:
        period2 = 2
    total = period1 + period2
    if total > max_period:
        dif = total - max_period
        periods = [period1, period2]
        max_idx = periods.index(max(periods))
        periods[max_idx] -= dif
        period1, period2 = periods
    return period1,period2

def fix_three_periods_hm(period1,period2,period3,max_period):
    total = period1 + period2 + period3

    if total > max_period:
        ratio = max_period / total
        period1 = int(period1 * ratio)
        period2 = int(period2 * ratio)
        period3 = int(period3 * ratio)
    if period1 < 2:
        period1 = 2
    if period2 < 2:
        period2 = 2
    if period3 < 2:
        period3 = 2
    total = period1 + period2 + period3
    if total > max_period:
        dif = total - max_period
        periods = [period1, period2, period3]
        max_idx = periods.index(max(periods))
        periods[max_idx] -= dif
        period1, period2, period3 = periods
    return period1,period2,period3