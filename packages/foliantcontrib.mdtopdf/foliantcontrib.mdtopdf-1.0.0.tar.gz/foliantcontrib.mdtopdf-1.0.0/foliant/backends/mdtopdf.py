import json
import shutil

from subprocess import run, PIPE, STDOUT, CalledProcessError
from pathlib import PosixPath

from foliant.utils import spinner
from foliant.backends.base import BaseBackend


class Backend(BaseBackend):
    _flat_src_file_name = '__all__.md'

    targets = ('pdf', 'site')

    required_preprocessors_after = [{
        'flatten': {
            'flat_src_file_name': _flat_src_file_name
        }},
        {'mdtopdf': {}}
    ]

    defaults = {
        'mdtopdf_path': 'md-to-pdf',
        'options': {},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._flat_src_file_path = self.working_dir / self._flat_src_file_name

        config = self.config.get('backend_config', {}).get('mdtopdf', {})
        self._mdtopdf_config = {**self.defaults, **config}
        self._slug = f'{self._mdtopdf_config.get("slug", self.get_slug())}'
        self._slug_for_commands = self._escape_control_characters(str(self._slug))

        self._cachedir = self.project_path / '.mdtopdfcache'
        shutil.rmtree(self._cachedir, ignore_errors=True)
        self._cachedir.mkdir()
        self.logger = self.logger.getChild('mdtopdf')

        self.logger.debug(f'Backend inited: {self.__dict__}')

    def _escape_control_characters(self, source_string: str) -> str:
        escaped_string = source_string.replace('"', "\\\"").replace('$', "\\$").replace('`', "\\`")

        return escaped_string

    def _generate_config_file(self, options: dict) -> PosixPath:
        config_path = self._cachedir / 'config.json'
        config = {}
        for key, value in options.items():
            config[key.replace('-', '_')] = value

        # md-to-pdf on unix requires --no-sandbox puppeteer flag to work properly
        launch_args = config.setdefault('launch_options', {}).setdefault('args', [])
        if '--no-sandbox' not in launch_args:
            launch_args.append('--no-sandbox')

        with open(config_path, 'w') as f:
            json.dump(config, f)
        return config_path

    def _get_html_command(self) -> str:
        pass

    def _get_pdf_command(self) -> str:
        components = [self._mdtopdf_config['mdtopdf_path']]

        config_path = self._generate_config_file(self._mdtopdf_config['options'])
        components.append(f'--config-file {config_path}')

        components.append(str(self._flat_src_file_path))
        components.append(f'"{self._slug_for_commands}.pdf"')

        command = ' '.join(components)

        self.logger.debug(f'PDF generation command: {command}')

        return command

    def make(self, target: str) -> str:
        with spinner(f'Making {target} with md-to-pdf', self.logger, self.quiet, self.debug):
            try:
                command = self._get_pdf_command()
                self.logger.debug('Running the command.')

                run(command, shell=True, check=True, stdout=PIPE, stderr=STDOUT)

                return f'{self._slug}.{target}'

            except CalledProcessError as exception:
                raise RuntimeError(f'Build failed: {exception.output.decode()}')

            except Exception as exception:
                raise type(exception)(f'Build failed: {exception}')
