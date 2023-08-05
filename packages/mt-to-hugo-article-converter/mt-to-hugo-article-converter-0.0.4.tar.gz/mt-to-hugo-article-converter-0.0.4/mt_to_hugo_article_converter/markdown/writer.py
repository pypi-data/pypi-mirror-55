import pathlib
import os
import re
import urllib.request
from datetime import datetime
from ..config import Config
from .taxonomies_mapper import TaxonomiesMapper
from .asset_downloader import AssetDownloader


class Writer:
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.taxonomies_mapper = TaxonomiesMapper()
        self.asset_downloader = AssetDownloader()

    def merge_body(self, md):
        body = ""
        if md["body"][0] and md["body"][1]:
            body = "\n\n<!-- more -->\n\n".join(md["body"])
        else:
            body = "".join(md["body"])
        return body

    def create_article_path(self, base_path, fmt, date, basename, lang):
        article_dir = os.path.join(
            base_path,
            date.strftime(fmt)
        )
        article_path = os.path.join(
            article_dir,
            "{}.{}.md".format(basename, lang)
        )
        pathlib.Path(article_dir).mkdir(parents=True, exist_ok=True)
        return article_path

    def write_md(self, basename, md):
        content = []
        content.append("---")
        content.append("title: \"{}\"".format(md["title"].replace('"', '\\"')))
        content.append("authors: [\"{}\"]".format(md["author"]))
        # TODO: TZ
        content.append("date: {}".format(md["date"]))
        content.append("lastmod: {}".format(md["date"]))
        content.append("categories: [\"{}\"]".format(
            "\", \"".join(md["categories"])))
        content.append("tags: [\"{}\"]".format("\", \"".join(md["tags"])))
        content.append("draft: true")
        content.append("---")
        content.append(self.merge_body(md))

        article_path = self.create_article_path(
            self.config.get_output_directory_path(),
            self.config.get_output_content_path_fmt(),
            md["date"],
            basename,
            "ja"  # TODO: i18n
        )
        with open(article_path, "w") as out:
            out.write("\n".join(content))
        print("💾 wrote out to: {}".format(article_path))

    def replace_asset_urls(self, src_text, replacements):
        for tag in replacements:
            src = replacements[tag]["src"]
            src = os.path.basename(src)
            src = urllib.parse.unquote(src)

            # Apply the format like ' width="640"' if the width exists.
            width = " width=\"{}\"".format(
                replacements[tag]["width"]) if replacements[tag]["width"] else ''

            figure = "\n\n{{{{< figure src=\"{}\"{}>}}}}\n\n".format(
                src, width)
            src_text = src_text.replace(tag, figure)
        return src_text

    def is_not_target(self, date):
        start_at = self.config.get_start_at()
        stop_at = self.config.get_stop_at()

        if start_at and stop_at:
            if start_at <= date <= stop_at:
                return False
        elif start_at:
            if start_at <= date:
                return False
        elif stop_at:
            if date <= stop_at:
                return False
        return True

    def write(self,  article):
        md = {
            "title": None,
            "date": None,
            "categories": [],
            "tags": [],
            "body": (None, None)
        }
        date = None
        basename = None

        for attr in article.attributes:
            name = attr.name()
            value = attr.value()
            if name == "Basename":
                basename = value
            if name == "Title":
                md["title"] = value
            if name == "Date":
                md["date"] = value
                date = value
                if self.is_not_target(date):
                    print("skipped: {}, {}".format(basename, date))
                    return
            if name == "Author":
                md["author"] = value
            if name in ["PrimaryCategory", "Category", "Tags", "Keywords"]:
                mapped = self.taxonomies_mapper.map(self.config, name, value)
                for key in mapped:
                    md[key] += mapped[key]
            if name == "Body":
                value = self.replace_asset_urls(
                    value, article.get_assets_info())
                md["body"] = (value, md["body"][1])
            if attr.name() == "ExtendedBody":
                value = self.replace_asset_urls(
                    value, article.get_assets_info())
                md["body"] = (md["body"][0], value)

        md["categories"] = sorted(list(set(md["categories"])))
        md["tags"] = sorted(list(set(md["tags"])))

        self.asset_downloader.download_assets_in_article(
            self.config, date, basename, article)
        self.write_md(basename, md)
