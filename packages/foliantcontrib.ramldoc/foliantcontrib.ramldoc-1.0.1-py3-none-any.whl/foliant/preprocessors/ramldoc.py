'''
Preprocessor for Foliant documentation authoring tool.
Generates documentation from RAML spec file.
'''

import os
import json
import shutil

from pathlib import Path, PosixPath
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
from distutils.dir_util import remove_tree
from jinja2 import Environment, FileSystemLoader
from pkg_resources import resource_filename
from subprocess import run, PIPE, STDOUT, CalledProcessError

from foliant.preprocessors.utils.preprocessor_ext import (BasePreprocessorExt,
                                                          allow_fail)
from foliant.preprocessors.utils.combined_options import (Options,
                                                          CombinedOptions,
                                                          validate_exists,
                                                          validate_in,
                                                          rel_path_convertor)
from foliant.utils import output

RAML2HTML_TEMPLATE = 'raml2html-full-markdown-theme'


class Preprocessor(BasePreprocessorExt):
    tags = ('ramldoc',)

    defaults = {
        'spec_url': [],
        'spec_path': '',
        'raml2html_path': 'raml2html',
        'template_dir': ''
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('ramldoc')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

        self._raml_tmp = self.project_path / '.ramlcache/'
        shutil.rmtree(self._raml_tmp, ignore_errors=True)
        self._raml_tmp.mkdir()

        self._counter = 0
        self.options = Options(self.options,
                               validators={'json_path': validate_exists,
                                           'spec_path': validate_exists})

    def _gather_specs(self,
                      urls: list,
                      path_: str or PosixPath or None) -> PosixPath:
        """
        Download first raml spec from the url list; copy it into the
        temp dir and return path to it. If all urls fail — check path_ and
        return it.

        Return None if everything fails
        """
        self.logger.debug(f'Gathering specs. Got list of urls: {urls}, path: {path_}')
        if urls:
            for url in urls:
                try:
                    filename = self._raml_tmp / f'raml_spec'
                    urlretrieve(url, filename)
                    self.logger.debug(f'Using spec from {url} ({filename})')
                    return filename
                except (HTTPError, URLError) as e:
                    self._warning(f'\nCannot retrieve raml spec file from url {url}. Skipping.',
                                  error=e)

        if path_:
            dest = self._raml_tmp / f'raml_spec'
            if not Path(path_).exists():
                self._warning(f"Can't find file {path_}. Skipping.")
            else:  # file exists
                shutil.copyfile(str(path_), str(dest))
                return dest

    def _process_spec(self,
                      spec_path: PosixPath,
                      options: CombinedOptions) -> str:
        """
        Process raml spec file with raml2html and return the resulting string
        """

        out_path = self._raml_tmp / f'raml{self._counter}.md'
        template_dir = options.get('template_dir')
        cmd = f'{options["raml2html_path"]} --theme {RAML2HTML_TEMPLATE} -o {out_path} {spec_path}'

        if template_dir:
            cmd += f' --template-dir {template_dir}'

        self.logger.info(f'Constructed command: \n {cmd}')
        try:
            result = run(
                cmd,
                shell=True,
                check=True,
                stdout=PIPE,
                stderr=STDOUT
            )
        except CalledProcessError as e:
            raise RuntimeError(e.output.decode('utf8', errors='ignore'))
        command_output_decoded = result.stdout.decode('utf8', errors='ignore')
        output(command_output_decoded, self.quiet)
        with open(out_path) as f:
            return f.read()

    @allow_fail()
    def process_ramldoc_blocks(self, block) -> str:
        tag_options = Options(self.get_options(block.group('options')),
                              convertors={'spec_path': rel_path_convertor(self.current_filepath.parent),
                                          'template_dir': rel_path_convertor(self.current_filepath.parent)})
        options = CombinedOptions(options={'config': self.options,
                                           'tag': tag_options},
                                  priority='tag',
                                  required=[('spec_url',),
                                            ('spec_path',)])
        self.logger.debug(f'Processing ramldoc tag in {self.current_filepath}')

        spec_url = options['spec_url']
        if spec_url and isinstance(spec_url, str):
            spec_url = [spec_url]
        spec_path = options['spec_path']
        spec = self._gather_specs(spec_url, spec_path)

        if not spec:
            raise RuntimeError("No valid raml spec file specified")

        return self._process_spec(spec, options)

    def apply(self):
        self._process_tags_for_all_files(func=self.process_ramldoc_blocks)
        self.logger.info('Preprocessor applied')
