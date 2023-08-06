import re
import shutil
import os

from pathlib import Path, PosixPath

from foliant.preprocessors.base import BasePreprocessor

IMG_DIR_NAME = '_mdtopdf_images'


def unique_name(dest_dir: str or PosixPath, old_name: str) -> str:
    """
    Check if file with old_name exists in dest_dir. If it does —
    add incremental numbers until it doesn't.
    """
    counter = 1
    dest_path = Path(dest_dir)
    name = old_name
    while (dest_path / name).exists():
        counter += 1
        name = f'_{counter}'.join(os.path.splitext(old_name))
    return name


class Preprocessor(BasePreprocessor):
    # defaults = {'project_dir_name': 'slate'}

    def _process_images(self, source: str, target_dir: str or PosixPath) -> str:
        """
        Cleanup target_dir. Copy local images to `target_dir` with unique names, replace their HTML
        definitions in `source` with confluence definitions.

        `source` — string with HTML source code to search images in;
        `rel_dir` — path relative to which image paths are determined.

        Returns a tuple: (new_source, attachments)

        new_source — a modified source with correct image paths
        """

        def _sub(image):
            image_caption = image.group('caption')
            image_path = image.group('path')

            # leave external images as is
            if image_path.startswith('http'):
                return image.group(0)

            image_path = Path(image_path)

            self.logger.debug(f'Found image: {image.group(0)}')

            new_name = unique_name(target_dir, image_path.name)
            new_path = Path(target_dir) / new_name

            self.logger.debug(f'Copying image into: {new_path}')
            shutil.copy(image_path, new_path)

            img_ref = f'![{image_caption}]({IMG_DIR_NAME}/{new_name})'

            self.logger.debug(f'Converted image ref: {img_ref}')
            return img_ref

        shutil.rmtree(target_dir, ignore_errors=True)
        Path(target_dir).mkdir()
        image_pattern = re.compile(r'!\[(?P<caption>.*?)\]\((?P<path>.+?)\)')
        self.logger.debug('Processing images')

        return image_pattern.sub(_sub, source)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('mdtopdf')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def apply(self):
        for markdown_file_path in self.working_dir.rglob('*.md'):
            with open(markdown_file_path, encoding='utf8') as markdown_file:
                content = markdown_file.read()

            processed_content = self._process_images(content, self.working_dir / IMG_DIR_NAME)

            with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                markdown_file.write(processed_content)

        self.logger.debug('Preprocessor applied.')
