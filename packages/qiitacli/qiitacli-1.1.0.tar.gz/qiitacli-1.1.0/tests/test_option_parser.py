from pathlib import Path

import pytest

from qiitacli.exceptions import QiitaCliParseError
from qiitacli.option_parser import parse, parse_body, parse_option

dammy_article_text = '''---
title: dammy article
tags:
    - dammy
    - article
private: yes
---
# dammy article
'''


def text_convert_lines(text):
    lines = text.split('\n')
    return ['{}\n'.format(l) for l in lines]


def test_parse():
    dammy_article_path = 'dammy_article.md'
    dammy_article = Path(dammy_article_path)
    with dammy_article.open('w') as f:
        f.write(dammy_article_text)

    option_and_body = None
    with dammy_article.open('r') as f:
        option_and_body = parse(f)
    assert option_and_body is not None
    assert 'options' in option_and_body.keys()
    assert isinstance(option_and_body['options'], dict)
    assert 'body' in option_and_body.keys()
    assert isinstance(option_and_body['body'], str)


def test_parser_option():
    print(dammy_article_text.split('\n'))
    lines = text_convert_lines(dammy_article_text)
    options = parse_option(lines)
    assert isinstance(options, dict)
    assert options['title'] == 'dammy article'


def test_parse_option_error():
    # 少しYAMLの記述が入っていないとYAMLファイルと認識されず、
    # エラーを吐かなくなってしまう
    dammy_article_text_error = '''---
title: This is
invalid
yaml
header
;-)
---
'''
    lines = text_convert_lines(dammy_article_text_error)
    with pytest.raises(QiitaCliParseError):
        parse_option(lines)


def test_parser_option_require_options():
    dammy_article_text_error = '''---
title: dammy article
private: yes
---
# example
'''
    lines = text_convert_lines(dammy_article_text_error)
    with pytest.raises(QiitaCliParseError):
        parse_option(lines)


def test_parse_body():
    lines = text_convert_lines(dammy_article_text)
    body = parse_body(lines)
    assert isinstance(body, str)


def test_parse_body_error():
    dammy_article_text_error = '''---
title: dammy article
tags:
    - dammy
    - article
private: yes
# example
'''
    lines = text_convert_lines(dammy_article_text_error)
    with pytest.raises(QiitaCliParseError):
        parse_body(lines)
