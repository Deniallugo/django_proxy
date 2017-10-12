from django.test import TestCase

from .helpers import replace_words


class HtmlReplaceTest(TestCase):

    def test_one_div(self):
        content = '<div> tester </div>'
        new_content = replace_words(
            content,
            replace=lambda word: word + 'tm',
            appropriate_word_func=lambda word: len(word) == 6
        )

        final_content = '<div> testertm </div>'
        self.assertNotEqual(content, new_content)
        self.assertEqual(new_content, final_content)

    def test_more_words_div(self):
        content = '<div> tester test testq testkkkk </div>'
        new_content = replace_words(
            content,
            replace=lambda word: word + 'tm',
            appropriate_word_func=lambda word: len(word) == 6
        )

        final_content = '<div> testertm test testq testkkkk </div>'
        self.assertNotEqual(content, new_content)
        self.assertEqual(new_content, final_content)

