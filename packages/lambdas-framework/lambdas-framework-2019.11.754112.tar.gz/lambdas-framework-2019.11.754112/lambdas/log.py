import textwrap


def _base(level: str, msg: str):
    msg = str(msg).strip('\n')
    if '\n' in msg:
        print(level, ':')
        print(textwrap.indent(msg, '  '))
    else:
        print(level, ':', msg)


def info(msg: str):
    _base('INFO', msg)
