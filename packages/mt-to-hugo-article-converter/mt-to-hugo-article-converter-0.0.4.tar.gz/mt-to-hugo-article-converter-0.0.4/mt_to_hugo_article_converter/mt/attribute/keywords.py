import re
from .multi_line_attribute import MultiLineAttribute


class Keywords(MultiLineAttribute):
    # TODO: split ',' and ' ', chomp \n and \"
    regex = re.compile(r'^\s*KEYWORDS:\s*$')

    def value(self):
        str_value = super(Keywords, self).value()
        if not str_value:
            return []
        comma_splited_values = str_value.split(",")
        whitespace_splited_values = []
        for v in comma_splited_values:
            whitespace_splited_values += v.split(" ")
        trimed_values = list(filter(None, whitespace_splited_values))
        sorted_values = sorted(list(set(trimed_values)))
        return sorted_values


if __name__ == '__main__':
    import doctest
    doctest.testmod()
