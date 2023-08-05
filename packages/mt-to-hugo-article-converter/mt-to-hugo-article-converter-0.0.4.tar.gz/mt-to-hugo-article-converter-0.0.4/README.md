# MT to Hugo Article Converter

## Requirements

- Python3

## Installation

```shellsession
pip3 install mt-to-hugo-article-converter
```

## How to use

```shellsession
mt-to-hugo-article-converter --output-directory=/path/to/out --input-file=/path/to/your-exported-articles.txt
```

You can use the configuration file that YAML format.

```shellsession
mt-to-hugo-article-converter --config-file=/path/to/config.yml
```

```yaml
version: "2019.10.0"
output:
  base_path: tmp/output/
  content_path_fmt: "content/posts/%Y.%m"
  static_path_fmt: "static/posts/%Y.%m"
input:
  path: tmp/example-articles.txt
  start_at: 2018/02/01 00:00:00
  stop_at: 2018/03/01 23:00:00
asset_download:
  enabled: true
  base_url: "https://cdn-ak.f.st-hatena.com"
  filter:
    - regex: 'https?://cdn-ak\.f\.st-hatena\.com'
attribute_map:
  tags:
    from:
      - TAGS
      - CATEGORY
    values:
      news:
        - info
        - お知らせ
```
