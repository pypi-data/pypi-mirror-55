"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


from io import StringIO
import importlib
from typing import List, Dict
from .columns import AbstractColumn
from .hydrating import Hydrator


class RowDescriptor(Hydrator):

    def __init__(self, columns: List[AbstractColumn]):
        super(RowDescriptor, self).__init__()
        assert isinstance(columns, list), 'columns deve ser uma List'
        assert columns != [], 'columns deve ter ao menos 1 elemento'
        self.columns = columns
        last = None
        for column in columns:
            column.start = last.end + 1 if last is not None else 1
            last = column
        self.validate_positions()

    @property
    def line_size(self):
        return self.columns[len(self.columns)-1].end

    def validate_positions(self):
        prev = None
        for col in self.columns:
            if prev is None:
                assert col.start == 1, 'A coluna %s deve começar com 1' % col.name
            else:
                assert prev.end + 1 == col.start, 'A coluna %s (starts in %d) deve começar imediatamente após ' \
                                                  'a coluna %s (ends in %d)' % \
                                                  (col.name, col.start, prev.name, prev.end)
            prev = col

    def get_values(self, row):
        return {col.name: col.to_value(row[col.start-1:col.end]) for col in self.columns}


class HeaderRowDescriptor(RowDescriptor):
    pass


class FooterRowDescriptor(RowDescriptor):
    pass


class DetailRowDescriptor(RowDescriptor):
    pass


class FileDescriptor(Hydrator):
    def __init__(self,
                 details: List[DetailRowDescriptor],
                 header: HeaderRowDescriptor=None,
                 footer: FooterRowDescriptor=None):
        super(FileDescriptor, self).__init__()

        assert isinstance(details, list), \
            'details deve ser uma List'
        assert len(details) > 0, \
            'details deve ser uma List com ao menos 1 DetailRowDescriptor'
        for detail in details:
            assert isinstance(detail, DetailRowDescriptor), \
                'details deve ser uma List de DetailRowDescriptor'
        assert isinstance(header, HeaderRowDescriptor) or header is None, \
            'header deve ser um HeaderRowDescriptor'
        assert isinstance(footer, FooterRowDescriptor) or footer is None, \
            'footer_descriptor deve ser um FooterRowDescriptor'

        self.header = header
        self.footer = footer
        self.details = details
        self.validate_sizes()
        self.line_size = self.details[0].line_size

    def validate_sizes(self):
        h = self.header.line_size if self.header else 0
        f = self.footer.line_size if self.footer else 0
        d = self.details[0].line_size
        ln = [x.line_size for x in self.details]
        s = sum(ln)
        assert (s == d * len(self.details)) and (d == h or h == 0) and (d == f or f == 0), \
            'O tamanho das linhas header (%d), footer (%d) e das details (%s) devem ser iguais' % (h, f, ln)
