import re

from html2text import HTML2Text


def replace_words(content, replace, appropriate_word_func, base_url=None,
                  port=8000):
    h = HTML2Text()
    h.ignore_links = True
    h.ignore_images = True

    text = re.sub('/W', ' ', h.handle(content))
    seen = set()
    seen_add = seen.add
    replace_fun = callable(replace)

    def replace_word(word):
        nonlocal content
        content = content.replace(word, replace(word)) if replace_fun \
            else content.replace(word, replace)
        return word

    if base_url:
        content = content.replace(base_url,
                                  'http://localhost:{port}/'.format(port=port))

    [replace_word(word) for word in text.split() if
     not (word in seen or seen_add(word)) and appropriate_word_func(word)]
    return content
