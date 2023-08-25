from replica.chat.utils import remove_urls, replace_words_keeping_case


def test_urls_are_being_removed():
    urls = [
        "https://zoom.us/j/123456789",
        "https://meet.google.com/abcdefg",
        "https://www.youtube.com/watch?v=abcdefghijk",
        "https://www.instagram.com/p/abcd1234/",
        "https://www.tiktok.com/@username/video/12345678",
        "https://www.example.com",
        "https://en.wikipedia.org/wiki/Page_Title",
        "https://www.youtube.com/watch?v=lmnopqrstuv",
        "https://www.google.com/maps?q=latitude,longitude",
        "www.close.com.co",
        "close.com.co",
        "close.com",
        "https://www.close.com.co"
    ]
    for url in urls:
        empty = remove_urls(url)
        assert empty == ''


def text_in_messages_is_being_replaced():
    messages = [
        {
            "from": "Barack Obama",
            "text": [
                "You can find all my passwords in https://www.allmypasswords.com",
                "My name is Elmo",
                "I live in the middle of the Caribbean Sea"
            ]
        }
    ]


def test_replace_words_keeping_case():
    replacements = [
        ("barack", "donald"),
        ("this is a long message", "this is a short message"),
        ("this is a long message", "this is a short message"),
        ("this is a long message", "this is a short message"),
        ("barack", "donald"),
    ]

    texts = [
        ("BaRACK", "DoNALD"),
        ("I wanted to tell you that this is a long message", "I wanted to tell you that this is a short message"),
        ("I wanted to tell you that this is a LONG message", "I wanted to tell you that this is a SHORT message"),
        ("I wanted to tell you that this is a lonG message", "I wanted to tell you that this is a shoRT message"),
        ("I went to Barack's house", "I went to Donald's house")
    ]
    for text, replacement in zip(texts, replacements):
        assert text[1] == replace_words_keeping_case(text[0], replacement[0], replacement[1])
