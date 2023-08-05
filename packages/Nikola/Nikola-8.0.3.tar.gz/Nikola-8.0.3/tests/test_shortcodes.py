# -*- coding: utf-8 -*-
# vim: set wrap textwidth=300

u"""Test shortcodes."""


import pytest
from nikola import shortcodes
from .base import FakeSite


def noargs(site, data='', lang=''):
    return "noargs {0} success!".format(data)


def arg(*args, **kwargs):
    # don’t clutter the kwargs dict
    kwargs.pop('site')
    data = kwargs.pop('data')
    kwargs.pop('lang')
    return "arg {0}/{1}/{2}".format(args, sorted(kwargs.items()), data)


def _fakesite():
    s = FakeSite()
    s.register_shortcode('noargs', noargs)
    s.register_shortcode('arg', arg)
    return s


fakesite = pytest.fixture(scope="module")(_fakesite)


def test_noargs(fakesite):
    assert shortcodes.apply_shortcodes(
        'test({{% noargs %}})', fakesite.shortcode_registry)[0] == 'test(noargs  success!)'
    assert shortcodes.apply_shortcodes(
        'test({{% noargs %}}\\hello world/{{% /noargs %}})', fakesite.
        shortcode_registry)[0] == 'test(noargs \\hello world/ success!)'


def test_arg_pos(fakesite):
    assert shortcodes.apply_shortcodes(
        'test({{% arg 1 %}})', fakesite.shortcode_registry)[0] == "test(arg ('1',)/[]/)"
    assert shortcodes.apply_shortcodes(
        'test({{% arg 1 2aa %}})', fakesite.shortcode_registry)[0] == "test(arg ('1', '2aa')/[]/)"
    assert shortcodes.apply_shortcodes(
        'test({{% arg "hello world" %}})', fakesite.shortcode_registry)[0] == "test(arg ('hello world',)/[]/)"
    assert shortcodes.apply_shortcodes(
        'test({{% arg back\\ slash arg2 %}})', fakesite.shortcode_registry)[0] == "test(arg ('back slash', 'arg2')/[]/)"
    assert shortcodes.apply_shortcodes(
        'test({{% arg "%}}" %}})', fakesite.shortcode_registry)[0] == "test(arg ('%}}',)/[]/)"


def test_arg_keyword(fakesite):
    assert shortcodes.apply_shortcodes(
        'test({{% arg 1a=2b %}})', fakesite.shortcode_registry)[0] == "test(arg ()/[('1a', '2b')]/)"
    assert shortcodes.apply_shortcodes(
        'test({{% arg 1a="2b 3c" 4d=5f %}})', fakesite.shortcode_registry)[0] == "test(arg ()/[('1a', '2b 3c'), ('4d', '5f')]/)"
    assert shortcodes.apply_shortcodes('test({{% arg 1a="2b 3c" 4d=5f back=slash\\ slash %}})',
                                       fakesite.shortcode_registry)[0] == "test(arg ()/[('1a', '2b 3c'), ('4d', '5f'), ('back', 'slash slash')]/)"


def test_data(fakesite):
    assert shortcodes.apply_shortcodes(
        'test({{% arg 123 %}}Hello!{{% /arg %}})', fakesite.shortcode_registry)[0] == "test(arg ('123',)/[]/Hello!)"
    assert shortcodes.apply_shortcodes('test({{% arg 123 456 foo=bar %}}Hello world!{{% /arg %}})',
                                       fakesite.shortcode_registry)[0] == "test(arg ('123', '456')/[('foo', 'bar')]/Hello world!)"
    assert shortcodes.apply_shortcodes('test({{% arg 123 456 foo=bar baz="quotes rock." %}}Hello test suite!{{% /arg %}})',
                                       fakesite.shortcode_registry)[0] == "test(arg ('123', '456')/[('baz', 'quotes rock.'), ('foo', 'bar')]/Hello test suite!)"
    assert shortcodes.apply_shortcodes('test({{% arg "123 foo" foobar foo=bar baz="quotes rock." %}}Hello test suite!!{{% /arg %}})',
                                       fakesite.shortcode_registry)[0] == "test(arg ('123 foo', 'foobar')/[('baz', 'quotes rock.'), ('foo', 'bar')]/Hello test suite!!)"


def test_errors(fakesite):
    with pytest.raises(shortcodes.ParsingError, match="^Shortcode 'start' starting at .* is not terminated correctly with '%}}'!"):
        shortcodes.apply_shortcodes('{{% start', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Syntax error in shortcode 'wrong' at .*: expecting whitespace!"):
        shortcodes.apply_shortcodes('{{% wrong ending %%}', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Found shortcode ending '{{% /end %}}' which isn't closing a started shortcode"):
        shortcodes.apply_shortcodes('{{% start %}} {{% /end %}}', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Unexpected end of unquoted string"):
        shortcodes.apply_shortcodes('{{% start "asdf %}}', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^String starting at .* must be non-empty!"):
        shortcodes.apply_shortcodes('{{% start =b %}}', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Unexpected end of data while escaping"):
        shortcodes.apply_shortcodes('{{% start "a\\', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Unexpected end of data while escaping"):
        shortcodes.apply_shortcodes('{{% start a\\', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Unexpected quotation mark in unquoted string"):
        shortcodes.apply_shortcodes('{{% start a"b" %}}', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Syntax error in shortcode 'start' at .*: expecting whitespace!"):
        shortcodes.apply_shortcodes('{{% start "a"b %}}', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Syntax error: '{{%' must be followed by shortcode name"):
        shortcodes.apply_shortcodes('{{% %}}', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Syntax error: '{{%' must be followed by shortcode name"):
        shortcodes.apply_shortcodes('{{%', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Syntax error: '{{%' must be followed by shortcode name"):
        shortcodes.apply_shortcodes('{{% ', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Found shortcode ending '{{% / %}}' which isn't closing a started shortcode"):
        shortcodes.apply_shortcodes('{{% / %}}', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Syntax error: '{{% /' must be followed by ' %}}'"):
        shortcodes.apply_shortcodes('{{% / a %}}', fakesite.shortcode_registry, raise_exceptions=True)

    with pytest.raises(shortcodes.ParsingError, match="^Shortcode '<==' starting at .* is not terminated correctly with '%}}'!"):
        shortcodes.apply_shortcodes('==> {{% <==', fakesite.shortcode_registry, raise_exceptions=True)


@pytest.mark.parametrize(
    "input, expected",
    [('{{% foo %}}', (u'SC1', {u'SC1': u'{{% foo %}}'})),
     ('{{% foo %}} bar {{% /foo %}}',
      (u'SC1', {u'SC1': u'{{% foo %}} bar {{% /foo %}}'})),
     ('AAA{{% foo %}} bar {{% /foo %}}BBB',
      (u'AAASC1BBB', {u'SC1': u'{{% foo %}} bar {{% /foo %}}'})),
     ('AAA{{% foo %}} {{% bar %}} {{% /foo %}}BBB',
      (u'AAASC1BBB', {u'SC1': u'{{% foo %}} {{% bar %}} {{% /foo %}}'})),
     ('AAA{{% foo %}} {{% /bar %}} {{% /foo %}}BBB',
      (u'AAASC1BBB', {u'SC1': u'{{% foo %}} {{% /bar %}} {{% /foo %}}'})),
     ('AAA{{% foo %}} {{% bar %}} quux {{% /bar %}} {{% /foo %}}BBB',
      (u'AAASC1BBB',
       {u'SC1': u'{{% foo %}} {{% bar %}} quux {{% /bar %}} {{% /foo %}}'})),
     ('AAA{{% foo %}} BBB {{% bar %}} quux {{% /bar %}} CCC',
      (u'AAASC1 BBB SC2 CCC',
       {u'SC1': u'{{% foo %}}', u'SC2': u'{{% bar %}} quux {{% /bar %}}'})), ])
def test_extract_shortcodes(input, expected, monkeypatch):
    i = iter('SC%d' % i for i in range(1, 100))
    monkeypatch.setattr(shortcodes, '_new_sc_id', i.__next__)
    extracted = shortcodes.extract_shortcodes(input)
    assert extracted == expected
