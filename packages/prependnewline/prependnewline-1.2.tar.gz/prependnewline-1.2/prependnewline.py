
"""
====================================
Markdown PrependNewLine Extension
====================================
:copyright: Copyright 2019 Ayobami Adewale
:license: MIT, see LICENSE for details.

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class PrependNewLineExtension(Extension):
    """ PrependNewLine Extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Insert PrependNewLinePreprocessor before ReferencePreprocessor. """
        md.preprocessors.register(PrependNewLinePreprocessor(md), 'prependnewline', 12)


class PrependNewLinePreprocessor(Preprocessor):
    """ PrependNewLine Preprocessor - finds list in a document and prepends a newline. """

    def run(self, lines):
        '''
        Find all list from the text.
        Each reference is prepended with a new line.
        '''
        new_text = []
        for line in lines:
            if len(line) > 0:
                if (line[0].isdigit() or line[0] == '*') and line[len(line) - 1] != '*':
                    line = '\n' + line
            new_text.append(line)
        return new_text


def makeExtension(**kwargs):  # pragma: no cover
    return PrependNewLineExtension(**kwargs)
