import math


def get_double(num: int):
    return num * 2


def display_date(day, month, year):
    print(f'{day}/{month}/{year}')


def is_positive(num: int):
    return num >= 0


def is_perfect_square(num: int):
    sqr_root = num ** (1 / 2)
    return sqr_root - int(sqr_root) == 0 and num > 0


def get_sphere_vol(radius: float):
    return 4 / 3 * math.pi * radius ** 3


def celsius_to_fahrenheit(temp: float):
    return temp * (9 / 5) + 32


if __name__ == "__main__":header=None
    print(get_double(4))

    display_date(24, 10, 2019)

    print(is_positive(8))
    print(is_positive(-8))

    print(is_perfect_square(4))
    print(is_perfect_square(5))

    print(get_sphere_vol(4))

    print(celsius_to_fahrenheit(21))


