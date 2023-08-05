import os
import pathlib
import yaml
import re
from dateutil.parser import parse as dateutil_parser_parse
from .validator import Validator


class Config:
    data = {
        'version': '2019.10.0',
        'output': {
            'base_path': '.',
            'content_path_fmt': 'content/posts/%Y.%m',
            'static_path_fmt': 'static/posts/%Y.%m'
        },
        'input': {},
        'asset_download': {
            'enabled': True,
            'base_url': None,
            'filter': []
        },
        'attribute_map': {
            'tags': {
                'restrict': False,
                'from': ['TAGS', 'CATEGORY'],
                'values': {}
            }
        }
    }

    def __init__(self, config_file_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validator = Validator()
        self.errors = []
        self.version = None
        self.output_directory_path = None
        self.output_content_path_fmt = None
        self.output_static_path_fmt = None
        self.input_file_path = None
        self.start_at = None
        self.stop_at = None
        self.download_assets = False
        self.assets_download_base_url = None
        self.assets_download_filter_patterns = []
        self.attribute_map = {}

        self.load_config_file(config_file_path)
        self.apply_config_valus()

    def load_config_file(self, a_path=None):
        if a_path:
            errs = self.validator.validate_config_file_path(a_path)
            self.errors += errs
            an_abs_path = os.path.abspath(a_path)
            loaded_data = {}
            with open(an_abs_path, "r") as fp:
                loaded_data = yaml.load(fp, Loader=yaml.BaseLoader)
            self.data.update(loaded_data)

    def apply_config_valus(self):
        self.set_version(self.data["version"])
        self.set_output_directory_path(self.data["output"]["base_path"])
        self.set_output_content_path_fmt(
            self.data["output"]["content_path_fmt"])
        self.set_output_static_path_fmt(self.data["output"]["static_path_fmt"])
        if self.data["input"]:
            if self.data["input"]["path"]:
                self.set_input_file_path(self.data["input"]["path"])
            if self.data["input"]["start_at"]:
                self.set_start_at(self.data["input"]["start_at"])
            if self.data["input"]["stop_at"]:
                self.set_stop_at(self.data["input"]["stop_at"])
        self.set_download_assets(self.data["asset_download"]["enabled"])
        self.set_assets_download_base_url(
            self.data["asset_download"]["base_url"])
        self.set_assets_download_filter_patterns(
            self.data["asset_download"]["filter"])
        self.set_attribute_map(self.data["attribute_map"])

    def get_version(self):
        return self.version

    def set_version(self, str):
        errs = self.validator.validate_version(str)
        self.errors += errs
        if len(errs) == 0:
            self.version = str
        return self

    def get_output_directory_path(self):
        return self.output_directory_path

    def set_output_directory_path(self, a_path):
        if a_path == None:
            return self

        errs = self.validator.validate_output_base_path(a_path)
        self.errors += errs
        if len(errs) == 0:
            an_abs_path = os.path.abspath(a_path)
            self.output_directory_path = an_abs_path
        return self

    def get_output_content_path_fmt(self):
        return self.output_content_path_fmt

    def set_output_content_path_fmt(self, a_path):
        if a_path == None:
            return self

        self.output_content_path_fmt = a_path
        return self

    def get_output_static_path_fmt(self):
        return self.output_static_path_fmt

    def set_output_static_path_fmt(self, a_path):
        if a_path == None:
            return self

        self.output_static_path_fmt = a_path
        return self

    def get_input_file_path(self):
        return self.input_file_path

    def set_input_file_path(self, a_path):
        if a_path == None:
            return self

        errs = self.validator.validate_input_file_path(a_path)
        self.errors += errs
        if len(errs) == 0:
            an_abs_path = os.path.abspath(a_path)
            self.input_file_path = an_abs_path
        return self

    def get_start_at(self):
        return self.start_at

    def set_start_at(self, a_date):
        if a_date == None:
            return self

        errs = self.validator.validate_start_at(a_date)
        self.errors += errs
        if len(errs) == 0:
            d = dateutil_parser_parse(a_date)
            self.start_at = d
        return self

    def get_stop_at(self):
        return self.stop_at

    def set_stop_at(self, a_date):
        if a_date == None:
            return self

        errs = self.validator.validate_stop_at(a_date)
        self.errors += errs
        if len(errs) == 0:
            d = dateutil_parser_parse(a_date)
            self.stop_at = d
        return self

    def set_download_assets(self, yes):
        self.download_assets = bool(yes)
        return self

    def is_download_assets(self):
        return self.download_assets

    def set_assets_download_base_url(self, base_url):
        self.assets_download_base_url = base_url
        return self

    def get_assets_download_base_url(self):
        return self.assets_download_base_url

    def set_assets_download_filter_patterns(self, filters):
        for filter in filters:
            if filter["regex"]:
                self.assets_download_filter_patterns.append(filter["regex"])
        return self

    def get_assets_download_filter_patterns(self):
        return self.assets_download_filter_patterns

    def set_attribute_map(self, values):
        self.attribute_map = values
        return self

    def get_attribute_map(self):
        return self.attribute_map

    def get_errors(self):
        return self.errors
