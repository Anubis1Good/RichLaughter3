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