import math


def return_highest(a: int, b: int):
    return a if a > b else b


def square_or_square_root(a: int):
    return a**(1/2) if a > 0 else a**2


def even_or_odd(num: int):
    return 'even' if num % 2 == 0 else 'odd'


def get_percentage(salary: float, bills: float):
    return bills/salary


def get_car_price(factory_cost: float):
    taxes = 0
    distributor = 0

    if factory_cost < 12000:
        taxes = 0
        distributor = factory_cost * 0.05

    elif factory_cost < 25000:
        taxes = factory_cost * 0.15
        distributor = factory_cost * 0.10
    else:
        taxes = factory_cost * 0.10
        distributor = factory_cost * 0.15

    return factory_cost + distributor + taxes


print(return_highest(2, 3))
print(return_highest(5, 3))

print(square_or_square_root(-3))
print(square_or_square_root(4))

print(even_or_odd(8))
print(even_or_odd(15))

print(get_percentage(1231, 12))

print(get_car_price(12314))
