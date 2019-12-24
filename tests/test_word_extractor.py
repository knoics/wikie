from word_extractor.wikie import parse_page

def test_parse_page():
  page = """
  <page>
      <title>free</title>
      <ns>0</ns>
      <id>19</id>
      <revision>
        <id>54930541</id>
        <parentid>54837032</parentid>
        <timestamp>2019-10-09T12:35:52Z</timestamp>
        <contributor>
          <username>WingerBot</username>
          <id>2024159</id>
        </contributor>
        <minor />
        <comment>move lang= to 1= in {{rfquotek}} (2)</comment>
        <model>wikitext</model>
        <format>text/x-wiki</format>
        <text xml:space="preserve">
        ==English==
        </text>
        <sha1>a27crxygaj92zlcfgeattj7pmfh7kxk</sha1>
      </revision>
    </page>
    """
  assert parse_page(page) == {'title': 'free', 'text': {}}

def test_parse_full_page():
  page = """
  <page>
      <title>free</title>
      <ns>0</ns>
      <id>19</id>
      <revision>
        <id>54930541</id>
        <parentid>54837032</parentid>
        <timestamp>2019-10-09T12:35:52Z</timestamp>
        <contributor>
          <username>WingerBot</username>
          <id>2024159</id>
        </contributor>
        <minor />
        <comment>move lang= to 1= in {{rfquotek}} (2)</comment>
        <model>wikitext</model>
        <format>text/x-wiki</format>
        <text xml:space="preserve">
        {{also|-free}}
        ==English==

        ===Pronunciation===
        * {{enPR|frē}}, {{IPA|en|/fɹiː/|[fɹɪi̯]}}
        * {{audio|en|en-us-free.ogg|Audio (US)}}
        * {{audio|en|En-uk-free.ogg|Audio (UK)}}
        * {{audio|en|LL-Q1860 (eng)-Nattes à chat-free.wav|Audio}}
        * {{rhymes|en|iː}}

        [[File:Free Beer.jpg|thumb|A sign advertising '''free''' beer (obtainable without payment), typically with some required purchase/catch.]]
        [[File:Buy one, get one free ^ - geograph.org.uk - 153952.jpg|thumb|A &quot;buy one get one '''free'''&quot; sign at a flower stand (obtainable without additional payment)]]
        [[File:Berkeley Farms Fat-Free Half &amp; Half.jpg|thumb|This food product is labelled &quot;fat '''free'''&quot;, meaning it contains no fat]]

        ===Adjective===
        {{en-adj|er}}

        # {{lb|en|social}} [[unconstrained|Unconstrained]].
    
        ====Translations====
        &lt;!-- Only abbreviated forms here (if they exist), please --&gt;
        </text>
        <sha1>a27crxygaj92zlcfgeattj7pmfh7kxk</sha1>
      </revision>
    </page>
    """
  expected = {
    'title': 'free',
    'text': {
      'IPA': 'fɹiː', 
      'ms': '84',
      'File': 'Free Beer.jpg',
      'pos': {
        'adjective': ['unconstrained.']
      }
    }
  }
  assert parse_page(page) == expected
