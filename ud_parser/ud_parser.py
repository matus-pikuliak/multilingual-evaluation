from html.parser import HTMLParser
from pathlib import Path

import requests

from language_utils.utils import tb_code_to_language
from ud_parser.perf import Perf


class UDScores(HTMLParser):

    def __init__(self, metric):
        super().__init__()
        self.state = None
        self.current_tb_code = None
        self.data = list()
        self.metric = metric

    def get_data(self):
        html = self.maybe_download()
        self.feed(html)
        return self.data

    def cache_file(self):
        parent_path = Path(__file__).absolute().parent
        return parent_path.joinpath('cache').joinpath(self.metric)

    def maybe_download(self):
        path = self.cache_file()
        if not Path.exists(path):
            html = requests.get(f'https://universaldependencies.org/conll18/results-{self.metric}.html').text
            open(path, 'w', encoding='utf-8').write(html)
        return open(path, encoding='utf-8').read()

    def handle_starttag(self, tag, attrs):
        self.state = {
            'h3': 'title',
            'h2': 'title',
            'pre': 'table'
        }.get(tag, None)

    def handle_endtag(self, tag):
        self.state = None

    def handle_data(self, data):
        if self.state == 'title':
            self.current_tb_code = data
        if self.state == 'table':
            for system, perf in self.parse_table(data):
                tb_code = self.current_tb_code
                self.data.append(
                    Perf(
                        tb_code=tb_code,
                        aggregate='_' not in tb_code,
                        language=tb_code_to_language(tb_code),
                        system=system,
                        perf=perf
                    )
                )

    @staticmethod
    def parse_table(table):
        for line in table.split('\n'):
            if line:
                yield line[5:40].rstrip(), float(line[-5:])
