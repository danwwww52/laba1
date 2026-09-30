"""
Лабораторная работа № 1.
Задание 3: вычисление ln c с нормализацией аргумента (c = m * 2^k)
и сравнение числа итераций с ненормализованным вариантом.
"""

import math

EPS = 1e-6
N_MAX = 100_000


def ln_series(c, eps=EPS, n_max=N_MAX):
    """
    Натуральный логарифм через ряд
        ln c = 2 * (y + y^3/3 + y^5/5 + ...),  y = (c - 1)/(c + 1)
    Без нормализации аргумента.
    Возвращает (значение, число итераций).
    """
    if c <= 0:
        raise ValueError("Аргумент логарифма должен быть положительным")

    y = (c - 1) / (c + 1)
    y2 = y * y
    power = y          # текущая степень y^(2k+1)
    total = 0.0

    for k in range(n_max):
        term = 2 * power / (2 * k + 1)
        if abs(term) < eps:
            return total, k
        total += term
        power *= y2

    raise RuntimeError("Точность не достигнута за n_max итераций")


def _ln_series_normalized_argument(c, eps=EPS, n_max=N_MAX):
    """
    Вспомогательная функция: ln c для c в диапазоне [0.5, 1)
    (|y| <= 1/3, ряд сходится быстро).
    """
    y = (c - 1) / (c + 1)
    y2 = y * y
    power = y
    total = 0.0

    for k in range(n_max):
        term = 2 * power / (2 * k + 1)
        if abs(term) < eps:
            return total, k
        total += term
        power *= y2

    raise RuntimeError("Точность не достигнута за n_max итераций")


def ln_normalized(c, eps=EPS, n_max=N_MAX):
    """
    Натуральный логарифм с нормализацией аргумента:
        c = m * 2^k,  m in [0.5; 1)
        ln c = ln m + k * ln 2
    Возвращает (значение, суммарное число итераций).
    """
    if c <= 0:
        raise ValueError("Аргумент логарифма должен быть положительным")

    # Приводим c к виду m * 2^k, m in [0.5; 1)
    k = 0
    m = c
    while m >= 1.0:
        m *= 0.5
        k += 1
    while m < 0.5:
        m *= 2.0
        k -= 1

    ln_m, it_m = _ln_series_normalized_argument(m, eps)
    ln_2, it_2 = _ln_series_normalized_argument(2.0, eps)

    return ln_m + k * ln_2, it_m + it_2


if __name__ == "__main__":
    # Аргументы для сравнения: от малых до больших значений
    values = [0.1, 0.5, 1.5, 5, 10, 50, 100, 1000]

    print(f"{'c':>10}{'ln(c)':>20}{'эталон':>20}"
          f"{'итер. без норм.':>18}{'итер. с норм.':>18}")
    print("-" * 86)

    for c in values:
        val_plain, it_plain = ln_series(c, EPS)
        val_norm, it_norm = ln_normalized(c, EPS)
        ref = math.log(c)

        print(f"{c:>10}{val_plain:>20.10f}{ref:>20.10f}"
              f"{it_plain:>18}{it_norm:>18}")

    # Дополнительно: проверка точности
    print("\nПроверка точности:")
    for c in values:
        val_norm, _ = ln_normalized(c, EPS)
        err = abs(val_norm - math.log(c))
        print(f"  c = {c:>8}: |ln(c) - math.log(c)| = {err:.3e}")