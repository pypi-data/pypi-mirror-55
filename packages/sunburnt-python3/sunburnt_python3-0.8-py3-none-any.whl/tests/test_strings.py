from sunburnt.strings import RawString, WildcardString


def test_string_escape():
    """ Ensure that string characters are escaped correctly for Solr queries.
    """
    test_str = '+-&|!(){}[]^"~*?: \t\v\\/'
    escaped = RawString(test_str).escape_for_lqs_term()
    assert escaped == '\\+\\-\\&\\|\\!\\(\\)\\{\\}\\[\\]\\^\\"\\~\\*\\?\\:\\ \\\t\\\x0b\\\\\\/'


def test_wildcards():
    test_str = "\\\\**\\\\??\\"
    escaped = WildcardString(test_str)
    print(escaped)
    assert escaped == test_str
