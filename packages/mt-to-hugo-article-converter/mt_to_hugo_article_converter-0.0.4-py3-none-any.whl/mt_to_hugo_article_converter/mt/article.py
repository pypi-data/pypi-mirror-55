import re
from functools import reduce
from ..config import Config
from .attribute import Author, Title, Basename, Status, PrimaryCategory, Category, Date, Tags, Body, ExtendedBody, Keywords


class Article:
    image_tag_regex = re.compile(r'(<img.*?>)')
    image_tag_src_regex = re.compile(r'\s+src\s*=\s*"(.*?)"\s*')
    image_tag_width_regex = re.compile(r'\s+width\s*=\s*"?([0-9]+)[px]?"?\s*')

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.is_end = False
        self.assets_info = {}
        self.first_attr = Author()
        self.attributes = [
            self.first_attr,
            Title(),
            Basename(),
            Status(),
            PrimaryCategory(),
            Category(),
            Date(),  # TODO: date fmt
            Tags(),
            Body(self.extract_asset_url),
            ExtendedBody(self.extract_asset_url),
            Keywords()
        ]
        pats = config.get_assets_download_filter_patterns()
        self.extract_target_url_patterns = list(
            map(lambda pat: re.compile(pat), pats))

    def extract_asset_url_src(self, el):
        match = self.image_tag_src_regex.search(el)
        if match:
            groups = match.groups()
            for group in groups:
                # return first group
                return str(group)
        return None

    def extract_asset_url_width(self, el):
        match = self.image_tag_width_regex.search(el)
        if match:
            groups = match.groups()
            for group in groups:
                # return first group
                return int(group)
        return None

    def is_extract_target(self, url):
        for pat in self.extract_target_url_patterns:
            match = pat.search(url)
            if match:
                return True
        return False

    def extract_asset_url(self, line):
        match = self.image_tag_regex.search(line)
        if match:
            groups = match.groups()
            for group in groups:
                src = self.extract_asset_url_src(group)
                if not self.is_extract_target(src):
                    continue
                width = self.extract_asset_url_width(group)
                self.assets_info[str(group)] = {
                    "src": src,
                    "width": width
                }
        return line

    def get_assets_info(self):
        urls = self.assets_info
        # TODO: filter
        return urls

    def will_end(self, line):
        if not self.first_attr.is_empty() and self.first_attr.test(line):
            return True
        return False

    def fullfilled(self):
        filterd = filter(lambda attr: attr.is_open()
                         or attr.is_empty(), self.attributes)
        not_filled = list(filterd)
        return len(not_filled) == 0

    def append_line(self, line):
        instance = self
        if self.will_end(line):
            instance = Article(self.config)
        instance.attributes = list(
            map(lambda record: record.set(line), instance.attributes))
        return instance
