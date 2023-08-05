import os
import pathlib


class Validator:
    valid_vesions = ["2019.10.0"]

    def validate_config_file_path(self, a_path):
        an_abs_path = os.path.abspath(a_path)
        if os.path.isfile(an_abs_path):
            return []
        e = Exception("Config file path {} is not a file!".format(an_abs_path))
        return [e]

    def validate_version(self, v):
        if v in self.valid_vesions:
            return []
        e = Exception("Version \"{}\" is unknown!".format(v))
        return [e]

    def validate_output_base_path(self, a_path):
        an_abs_path = os.path.abspath(a_path)
        if os.path.isdir(an_abs_path):
            return []
        if not os.path.isdir(an_abs_path):
            print("Output base path {} does not exist. Creating...".format(an_abs_path))
            pathlib.Path(an_abs_path).mkdir(parents=True, exist_ok=True)
            return []
        e = Exception(
            "Output base path {} is not a directory!".format(an_abs_path))
        return [e]

    def validate_input_file_path(self, a_path):
        an_abs_path = os.path.abspath(a_path)
        if os.path.isfile(an_abs_path):
            return []
        e = Exception("Input file path {} is not a file!".format(an_abs_path))
        return [e]

    def validate_start_at(self, a_date):
        # TODO: impl
        return []

    def validate_stop_at(self, a_date):
        # TODO: impl
        return []
