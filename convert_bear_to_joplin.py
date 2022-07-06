from datetime import datetime, timezone
import os
import re
import shutil

import click
import yaml


class BearToJoplinConverter:
    def __init__(self, overwrite='yes'):
        self.overwrite = overwrite
        self.color_re = re.compile(r'^[0-9a-fA-F]{6}$')

    def convert(self, in_path, out_path):
        print(f'convert "{in_path}" to "{out_path}"')
        if os.path.exists(out_path):
            if self.overwrite == 'abort':
                print('Output file already exists, aborting.')
                raise click.Abort()
            elif self.overwrite == 'ask':
                overwrite = click.confirm('Output file exists, do you want to overwrite?', default=True)
            else:
                overwrite = self.overwrite == 'yes'

            if not overwrite:
                print('Output file already exists, skipping conversion.')
                return

        out_folder = os.path.dirname(out_path)
        os.makedirs(out_folder, exist_ok=True)

        if os.path.splitext(in_path)[1] != '.md':
            shutil.copyfile(in_path, out_path)
            return

        front_matter = self.extract_front_matter_info(in_path)
        with open(in_path) as in_file:
            with open(out_path, 'w') as out_file:
                yaml.dump(front_matter, out_file, sort_keys=False, explicit_start=True, allow_unicode=True)
                out_file.write('---\n\n')
                for line in in_file:
                    out_file.write(line)

        shutil.copymode(in_path, out_path)
        shutil.copystat(in_path, out_path)

    def extract_front_matter_info(self, md_path):
        """Parse Markdown content to extract title and hashtags.

        Here it is a simple solution: title is the first line, all tags comes from the last line.

        To extract all tags, try [Python-Markdown](https://python-markdown.github.io/).

        Read [python-markdown-hashtag-extension](https://github.com/Kongaloosh/python-markdown-hashtag-extension).
        """
        title = None
        prev_line = None
        with open(md_path) as f:
            for line in f:
                line = line.rstrip('\r\n')
                if not line:
                    continue

                if prev_line is None:
                    title = line.lstrip('#').strip()

                prev_line = line

        tags = self.extract_hashtags(prev_line)

        front_matter = {}
        if title:
            front_matter['title'] = title

        created = datetime.fromtimestamp(os.path.getctime(md_path), timezone.utc)
        updated = datetime.fromtimestamp(os.path.getmtime(md_path), timezone.utc)
        front_matter['created'] = f'{created:%Y-%m-%d %H:%M:%SZ}'
        front_matter['updated'] = f'{updated:%Y-%m-%d %H:%M:%SZ}'

        if tags:
            front_matter['tags'] = tags

        return front_matter

    def extract_hashtags(self, line):
        if not line or '#' not in line:
            return []

        tags = []
        start = 0
        end = 0
        in_hash = False
        multi_words = False
        prev = None
        for i, curr in enumerate(line):
            peek = line[i + 1] if i + 1 < len(line) else None

            if curr == '#' and (prev is None or prev == ' ') and not in_hash:
                # When a starting hashtag is found, initialize the starting point index.
                start = i + 1
                in_hash = True
                end = start
            elif curr == '#' and prev != ' ':
                # When the previous character isn't a space and the current is a hash,
                # then this must be the end of a multi-words hash.
                end = i
            elif curr == ' ' and in_hash and peek != '#':
                # If currently scanning a hash and a space is found without a subsequent
                # hash then this is either a multi-words hash or some unrelated text,
                # so store the current position as the possible end of the hash.
                end = i
                multi_words = True
            elif curr == ' ' and in_hash and peek == '#':
                # When a space is found followed by a hash, then this must be the end of
                # the current hash.
                in_hash = False
                multi_words = False
                tags.append(line[start:end])
            elif not multi_words:
                # If this isn't a potential multi-words hash, then keep incrementing the end index.
                end += 1

            prev = curr

        if in_hash:
            tags.append(line[start:end])

        # Remove non tag hashes.
        tags = list(filter(self.is_tag, tags))

        return tags

    def is_tag(self, hash):
        if self.color_re.match(hash):
            return False

        return True


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dst', type=click.Path())
@click.option('--overwrite', type=click.Choice(['yes', 'no', 'ask', 'abort']), default='yes',
              help='Whether overwrite existing destination file (default: yes).')
def main(src, dst, **kwargs):
    """Convert Bear exported markdown files to markdown + Front Matter formats which Joplin can import.

    SRC is the path of the input markdown file or directory.

    DST is the path of the output markdown file or directory.
    """
    print(locals())
    converter = BearToJoplinConverter(overwrite=kwargs['overwrite'])

    if os.path.isfile(src):
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))

        converter.convert(src, dst)
    else: # isdir
        if os.path.isfile(dst):
            raise click.BadArgumentUsage(f'`DST` cannot be a file when `SRC` is a directory.')

        for root, _, filenames in os.walk(src):
            for filename in filenames:
                print(os.path.join(root, filename))
                in_path = os.path.join(root, filename)
                relative_path = os.path.relpath(in_path, src)
                out_path = os.path.join(dst, relative_path)
                converter.convert(in_path, out_path)


if __name__ == '__main__':
    main()
