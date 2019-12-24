from xml_parser.simple_xml_parser import xml_to_dict

def test_xml_parser_empty():
    xml = "<page></page>"
    assert xml_to_dict(xml) == {'page': ''}

def test_xml_parser_empty_simpler():
    assert xml_to_dict("<page/>") == {'page': ''}
    assert xml_to_dict("<page />") == {'page': ''}

def test_xml_parser_one_level():
    xml = "<page>hello</page>"
    assert xml_to_dict(xml) == {'page': 'hello'}

def test_xml_parser_one_level_with_attr():
    xml = "<page some=prop>hello</page>"
    assert xml_to_dict(xml) == {'page': 'hello'}

def test_xml_parser_two_levels():
    xml = """
        <page>
            <title>free</title>
            <revision>
                rev
            </revision>
        </page>
    """
    expected = {
        'page': {
            'title': 'free',
            'revision': 'rev'
        }
    }   
    assert xml_to_dict(xml) == expected

def test_xml_parser_three_levels():
    xml = """
        <page>
            <revision>
                <text xml:space="preserve">
                    this is text.
                </text>
            </revision>
        </page>
    """
    expected = {
        'page': {
            'revision': {
                'text': 'this is text.'
            }
        }
    }   
    assert xml_to_dict(xml) == expected

def test_xml_parser_more_levels():
    xml = """
        <page>
            <title>free</title>
            <revision>
                <text xml:space="preserve">
                    a free text
                </text>
            </revision>
        </page>
    """
    expected = {
        'page': {
            'title': 'free',
            'revision': {
                'text': 'a free text'
            }
        }
    }
    assert xml_to_dict(xml) == expected

def test_xml_parser_more_levels_empty_text():
    xml = """
        <page>
            <title>free</title>
            <revision>
                <text xml:space="preserve" />
            </revision>
        </page>
    """
    expected = {
        'page': {
            'title': 'free',
            'revision': {
                'text': ''
            }
        }
    }
    assert xml_to_dict(xml) == expected

def test_more_complicated_page():
    xml = """
<page>
    <title>free</title>
    <id>19</id>
    <revision>
      <id>54930541</id>
      <minor />
      <comment>move lang= to 1= in {{rfquotek}} (2)</comment>
      <text xml:space="preserve">{{also|-free}}
      </text>
      <sha1>a27crxygaj92zlcfgeattj7pmfh7kxk</sha1>
    </revision>
  </page>
  """
    expected = {
        'page': {
            'title': 'free',
            'id': '19',
            'revision': {
                'id': '54930541',
                'minor': '',
                'comment': 'move lang= to 1= in {{rfquotek}} (2)',
                'text': '{{also|-free}}',
                'sha1': 'a27crxygaj92zlcfgeattj7pmfh7kxk'
            }
        }
    }
    assert xml_to_dict(xml) == expected