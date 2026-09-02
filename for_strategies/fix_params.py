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
    return period1,period2

def fix_two_periods_hm(period1,period2,max_period):
    total = period1 + period2

    if total > max_period:
        ratio = max_period / total
        period1 = int(period1 * ratio)
        period2 = int(period2 * ratio)
    return period1,period2