import pathlib
import os
import urllib.request
from ..config import Config


class AssetDownloader:
    def create_asset_download_dir_path(self, base_path, fmt, date, basename):
        download_path = os.path.join(
            base_path,
            date.strftime(fmt),
            basename
        )
        pathlib.Path(download_path).mkdir(parents=True, exist_ok=True)
        return download_path

    def download_assets_in_article(self, config, date, basename, article):
        if not config.is_download_assets():
            return

        dir_path = self.create_asset_download_dir_path(
            config.get_output_directory_path(),
            config.get_output_static_path_fmt(),
            date,
            basename
        )
        asset_tags = article.get_assets_info()
        for asset_tag in asset_tags:
            url = asset_tags[asset_tag]["src"]
            if not url.startswith("http"):
                url = "{}/{}".format(config.get_assets_download_base_url(), url)
            file_name = os.path.basename(url)
            file_name = urllib.parse.unquote(file_name)
            file_path = os.path.join(dir_path, file_name)
            try:
                print("🌏 downloading the asset: {}".format(url))
                urllib.request.urlretrieve(url, file_path)
            except Exception as error:
                print("❗️ cannot download the asset: {}\n{}".format(url, error))
