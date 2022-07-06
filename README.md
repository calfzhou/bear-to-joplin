# Bear to Joplin

Convert [Bear](https://bear.app/) exported markdown to [Joplin](https://joplinapp.org/) format.

## Background

[Joplin - Markdown with Front Matter Exporter/Importer](https://github.com/laurent22/joplin/blob/dev/readme/spec/interop_with_frontmatter.md)

Joplin supported metadata fields:

- `title`: Extract from the first line or first heading
- `updated`: File's modification time
- `created`: File's creation time
- `source`: N/A
- `author`: N/A
- `latitude`: N/A
- `longitude`: N/A
- `altitude`: N/A
- `completed?`: N/A
- `due`: N/A
- `tags`: Extract hashtags from the file content

## Setup

``` bash
pip install -r requirements.txt -c constraints.txt
```

## Usage

``` bash
python convert_bear_to_joplin.py --help
```
