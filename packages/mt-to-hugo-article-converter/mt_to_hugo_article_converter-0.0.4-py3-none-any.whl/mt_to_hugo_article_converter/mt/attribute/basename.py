import re
from .single_line_attribute import SingleLineAttribute


class Basename(SingleLineAttribute):
    regex = re.compile(r'^\s*BASENAME:\s*(.*)\s*$')
    replacements = [
        ("_", "-"),
        ("/", "-"),
        ("#", "")
    ]

    def value(self):
        v = super(Basename, self).value()
        if not v:
            return None

        for replacement_tuple in self.replacements:
            v = v.replace(replacement_tuple[0], replacement_tuple[1])
        v = v.lower()
        return v


if __name__ == '__main__':
    import doctest
    doctest.testmod()
