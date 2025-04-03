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

``` text
Usage: convert_bear_to_joplin.py [OPTIONS] SRC DST

  Convert Bear exported markdown files to markdown + Front Matter formats
  which Joplin can import.

  SRC is the path of the input markdown file or directory.

  DST is the path of the output markdown file or directory.

Options:
  --overwrite [yes|no|ask|abort]  Whether overwrite existing destination file
                                  (default: yes).
  --reverse                       Set file creation and modification time to
                                  the time in the front matter.
  --help                          Show this message and exit.
```
