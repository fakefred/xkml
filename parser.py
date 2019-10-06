from utils import setProperty, numberifyIfIsNumber

# '.' should not be a delimiter
# because it appears in numbers
KEYS_WITH_SPECIAL_VALUE_DELIMITERS = {
    'size': '*',
    'position': ',',
    'neck': ',',
    'l': ',',
    'r': ','
}

SPECIAL_KEY_TRANSFORMS = {
    'l': 0,
    'r': 1
}


def countLeadingSpaces(str: str) -> int:
    return len(str) - len(str.lstrip())


def parse(filename: str):
    # open the xkml file
    raw_xkml_lines = open(filename).readlines()

    # removes blank lines and comment lines
    xkml_lines = []
    for line in raw_xkml_lines:
        if line.strip() != '' and not line.strip().startswith('#'):
            xkml_lines.append(line)

    # detect indentation spaces
    spaces = 4
    for line in xkml_lines:
        spaces = countLeadingSpaces(line)
        if spaces > 0:
            break

    # parse lines into nested dict
    root = {}
    trace = []  # as a stack
    indent = -1
    for line in xkml_lines:
        # extract kv pairs
        # the value of key-only lines
        # (to be nested with the next line)
        # is temporarily set to ''
        kv = line.split(':')
        k = kv[0].strip()

        # special cases for k
        # k is an int
        if k.isnumeric():
            k = int(k)
        v = ''

        # k is split with a designated delimiter
        v_delim = ''
        if k in KEYS_WITH_SPECIAL_VALUE_DELIMITERS:
            v_delim = KEYS_WITH_SPECIAL_VALUE_DELIMITERS[k]

        # k needs to be transformed
        if k in SPECIAL_KEY_TRANSFORMS:
            k = SPECIAL_KEY_TRANSFORMS[k]

        # the rest is v
        for substr in kv[1:]:
            v += substr + ':'

        v = v[:-1].strip()

        # v is an int/float
        v = numberifyIfIsNumber(v)

        # v is interpreted as a tuple
        if v_delim != '':
            v_split = v.split(v_delim)
            v_split_int = []
            for substr in v_split:
                if substr != '':
                    v_split_int.append(int(substr.strip()))
            v = tuple(v_split_int)

        # count indent level
        line_idt = countLeadingSpaces(line) // spaces

        # from change of indent level, determine trace
        if line_idt > indent:
            # indent advanced
            trace.append(k)
        elif line_idt == indent:
            # indent unchanged
            trace.pop()
            trace.append(k)
        elif line_idt < indent:
            # indent backed
            for _ in range(indent - line_idt + 1):
                trace.pop()
            trace.append(k)
        root = setProperty(root, trace, v)

        # update indent
        indent = line_idt

    return root


