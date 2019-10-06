import math

def d2r(deg: int):
    # degrees to radians
    return deg / 360 * 2 * math.pi


def normalize_into_interval(value: any, interval: tuple):
    interval_length = max(interval) - min(interval)
    if min(interval) <= value <= max(interval):
        return value
    elif value < min(interval):
        return normalize_into_interval(value + interval_length, interval)
    elif value > max(interval):
        return normalize_into_interval(value - interval_length, interval)


def abs_sin(theta: int):
    # theta in degrees
    return abs(math.sin(d2r(theta)))

def abs_cos(theta: int):
    return abs(math.cos(d2r(theta)))