import re
from dateutil.parser import parse
from dateutil.tz import gettz
from .single_line_attribute import SingleLineAttribute


class Date(SingleLineAttribute):
    regex = re.compile(r'^\s*DATE:\s*(.*)\s*$')

    def value(self):
        v = super(Date, self).value()
        if v:
            # TODO: TZ
            tzinfos = {"JST": gettz('Asia/Tokyo')}
            return parse(v, tzinfos=tzinfos)
        return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
