import sys
from optparse import OptionParser
from .config import Config
from .converter import Converter


def main():
    option_parser = OptionParser()
    option_parser.add_option("-c", "--config-file", dest="config_file_path",
                             help="config file path (YAML)", metavar="PATH")
    option_parser.add_option("-o", "--output-directory", dest="output_directory_path",
                             help="output base directory path (Hugo)", metavar="PATH")
    option_parser.add_option("-i", "--input-file", dest="input_file_path",
                             help="input file path (MovableType)", metavar="PATH")
    option_parser.add_option("-s", "--start-at", dest="start_at",
                             help="start date", metavar="DATE")
    option_parser.add_option("-e", "--stop-at", dest="stop_at",
                             help="stop date", metavar="DATE")
    option_parser.add_option("-d", "--asset-download-enabled", action="store_true",
                             dest="asset_download_enabled", default=True, help="download assets")
    option_parser.add_option("-D", "--asset-download-disabled", action="store_false",
                             dest="asset_download_enabled", default=True, help="download assets")
    (options, args) = option_parser.parse_args()

    config = Config(
        options.config_file_path
    ).set_output_directory_path(
        options.output_directory_path
    ).set_input_file_path(
        options.input_file_path
    ).set_start_at(
        options.start_at
    ).set_stop_at(
        options.stop_at
    ).set_download_assets(
        options.asset_download_enabled
    )

    errs = config.get_errors()
    if len(errs) > 0:
        for err in errs:
            print(err)
        sys.exit(1)

    converter = Converter()
    converter.convert(config)
