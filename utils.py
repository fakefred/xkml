import re


def getValueOrFallback(dictionary: dict, key: str or list, default: any):
    if type(key) == str:
        return dictionary[key] if key in dictionary else default
    elif type(key) == list:
        if len(key) == 1:
            return getValueOrFallback(dictionary, key[0], default)
        elif len(key) > 1:
            return getValueOrFallback(dictionary[key[0]], key[1:], default)


def setProperty(dictionary: dict, trace: list, value: any):
    if len(trace) == 1:
        dictionary[trace[0]] = value
    elif len(trace) > 1:
        # dictionary[trace[0]] needs to be nested with further properties.
        # convert to dict.
        if dictionary[trace[0]] == '':
            dictionary[trace[0]] = {}
        dictionary[trace[0]] = setProperty(
            dictionary[trace[0]], trace[1:], value)

    return dictionary


def numberifyIfIsNumber(str: str):
    if re.match(r'^-?\d+?\.?\d+$|^-?\d+$', str) is not None:
        if str.find('.') != -1:
            # found decimal point; is float
            return float(str)
        else:
            return int(str)
    return str
