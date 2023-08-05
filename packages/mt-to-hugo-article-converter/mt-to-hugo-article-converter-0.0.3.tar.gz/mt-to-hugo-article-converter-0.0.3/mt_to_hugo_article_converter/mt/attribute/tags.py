import re
from .single_line_attribute import SingleLineAttribute


class Tags(SingleLineAttribute):
    regex = re.compile(r'^\s*TAGS:\s*(.*)\s*$')

    def value(self):
        str_value = super(Tags, self).value()
        if not str_value:
            return []
        unquoted_str = str_value.replace('"', '')
        comma_splited_values = unquoted_str.split(",")
        whitespace_splited_values = []
        for v in comma_splited_values:
            whitespace_splited_values += v.split(" ")
        trimed_values = list(filter(None, whitespace_splited_values))
        sorted_values = sorted(list(set(trimed_values)))
        return sorted_values


if __name__ == '__main__':
    import doctest
    doctest.testmod()
