"""List of Wikia sources to scape."""

SOURCES = [
    {
        "author": "Tolkien",
        "dump_url": "http://s3.amazonaws.com/wikia_xml_dumps/l/lo/lotr_pages_current.xml.7z",
        "root": "/n:mediawiki/n:page",
        "xpath": "./n:title/text()",
        "where": {
            "xpath": "./n:revision/n:text/text()",
            "contains": r'''\{\{Infobox Person'''
        },
        "ignore": [r"^.+:", r"\(.+\)$"],
        "strip": []
    },
    {
        "author": "George Martin",
        "dump_url": "http://s3.amazonaws.com/wikia_xml_dumps/i/ic/iceandfire_pages_current.xml.7z",
        "root": "/n:mediawiki/n:page",
        "xpath": "./n:title/text()",
        "where": {
            "xpath": "./n:revision/n:text/text()",
            "contains": r'''\[\[Category:Characters'''
        },
        "ignore": [r"^.+:", r"\(.+\)$"],
        "strip": []
    },
    {
        "author": "Robert Jordan",
        "dump_url": "http://s3.amazonaws.com/wikia_xml_dumps/w/wo/wot_pages_current.xml.7z",
        "root": "/n:mediawiki/n:page",
        "xpath": "./n:title/text()",
        "where": {
            "xpath": "./n:revision/n:text/text()",
            "contains": r'''\{\{ character'''
        },
        "ignore": [r"^.+:", r"\(.+\)$"],
        "strip": []
    },
    {
        "author": "Steven Erikson",
        "dump_url": "http://s3.amazonaws.com/wikia_xml_dumps/m/ma/malazan_pages_current.xml.7z",
        "root": "/n:mediawiki/n:page",
        "xpath": "./n:title/text()",
        "where": {
            "xpath": "./n:revision/n:text/text()",
            "contains": r'''\[\[Category:(Males|Females)'''
        },
        "ignore": [r"^.+:", r"\(.+\)$"],
        "strip": []
    },
    {
        "author": "Brian Jacques",
        "dump_url": "http://s3.amazonaws.com/wikia_xml_dumps/r/re/redwall_pages_current.xml.7z",
        "root": "/n:mediawiki/n:page",
        "xpath": "./n:title/text()",
        "where": {
            "xpath": "./n:revision/n:text/text()",
            "contains": r'''\{\{Character\|'''
        },
        "ignore": [r"^.+:", r"\(.+\)$"],
        "strip": []
    },
    {
        "author": "Frank Herbert",
        "dump_url": "http://s3.amazonaws.com/wikia_xml_dumps/d/du/dune_pages_current.xml.7z",
        "root": "/n:mediawiki/n:page",
        "xpath": "./n:title/text()",
        "where": {
            "xpath": "./n:revision/n:text/text()",
            "contains": r'''\[\[Category:(Males|Females)'''
        },
        "ignore": [r"^.+:", r"\(.+\)$"],
        "strip": [r"/XD$", r"/ED$", r"/Featured$"]
    },
    {
        "author": "Andrzej Sapkowski",
        "dump_url": "http://s3.amazonaws.com/wikia_xml_dumps/w/wi/witcher_pages_current.xml.7z",
        "root": "/n:mediawiki/n:page",
        "xpath": "./n:title/text()",
        "where": {
            "xpath": "./n:revision/n:text/text()",
            "contains": r'''\[\[Category:Characters in the (short stories|novels)'''
        },
        "ignore": [r"^.+:", r"\(.+\)$"],
        "strip": []
    },
]
