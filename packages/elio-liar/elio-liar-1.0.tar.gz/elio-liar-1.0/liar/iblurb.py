# -*- encoding: utf-8 -*-
""""""
from liar.itransform import ITransform
from liar.iamprimitive import IAmPrimitive
from random import randint
from liar.ijusthelp import rewrite_dict


class IBlurb(object):
    """IBlurb makes strings."""

    def __init__(self, dictionary_list, min, max):
        """Set me up with a list of words.

        :param dictionary_list: The entire data definition.
        :param min: The minimum number of words for your blurb.
        :param max: The maximnum number of words for your blurb.
        """

        self.words = IBlurb.Words(dictionary_list, min, max)

    def blurb_column(self, data_method, dataset_size):
        """This returns an entire column of data specified."""

        return [getattr(self, data_method) for _ in range(0, dataset_size)]

    @property
    def plaintext_phrase(self):
        """A plaintext phrase with no punctuation."""

        wrd_lst = self.words.word_list
        return " ".join(wrd_lst)

    @property
    def plaintext_title(self):
        """A plaintext phrase starting with a capital letter."""

        wrd_lst = self.words.word_list
        wrd_lst[0] = wrd_lst[0].capitalize()
        return " ".join(wrd_lst)

    @property
    def plaintext_sentence(self):
        """A plaintext sentence starting with a capital letter and ending with full stop."""

        return f"{self.plaintext_title}."

    @property
    def plaintext_sentences(self):
        """Plaintext sentences starting with a capital letter and ending with full stop."""

        return " ".join(self.words.sentence_groups)

    @property
    def plaintext_bullets(self):
        """A plaintext bullet list."""

        return "\n\n{}\n".format(" ".join(self.words.plaintext_bullet_groups))

    @property
    def plaintext_paragraphs(self):
        """A plaintext paragraphs list."""

        return " ".join(self.words.plaintext_paragraphs_groups)

    @property
    def html_paragraph(self):
        """An HTML rendered paragraph."""

        return f"<p>{self.plaintext_sentences}</p>"

    @property
    def html_bullets(self):
        """HTML rendered bullets."""

        return "<ul>{}</ul>".format(" ".join(self.words.html_bullet_groups))

    @property
    def html_paragraphs(self):
        """HTML rendered paragraphs."""

        return " ".join(self.words.html_paragraphs_groups)

    @property
    def html(self):
        """HTML rendered paragraphs and bullets."""

        rtn = ""
        paragraph_groups = self.words.paragraph_groups
        for sentence_groups in paragraph_groups:
            i = randint(1, 6)
            if i > 1:
                rtn += "<p>{}</p>".format(" ".join(sentence_groups))
            else:
                rtn += "<ul>{}</ul>".format(
                    " ".join(IBlurb.Words._make_bullet_groups(sentence_groups))
                )
        return rtn

    #
    class Words(object):
        """This class provide a mechanism for feeding and shuffling lists
        of words into the "blurb builder" methods above.
        """

        def __init__(self, dictionary_list, min, max):
            self.min = min
            self.max = max
            # is this a word list or dictionary list?
            if isinstance(dictionary_list[0], dict):
                dictionary_list = ITransform.Data.convert_2_simple_list(
                    dictionary_list, "word"
                )
            # store the original file
            self.dictionary_list = dictionary_list
            # start the words in a random order
            self.words = ITransform.Data.rand_sort(list(self.dictionary_list))

        @property
        def word_list(self):
            """Get a simple/perfect list of words - randomly sorted for every
            field to ensure they all look unique."""

            # make the word list a random size each time
            word_size = IAmPrimitive.Values.get_int(self.min, self.max)

            # make sure there are still enough words in the dictionary
            while len(self.words) < word_size:
                # repopulate the words list from the original source; resorted
                self.words += ITransform.Data.rand_sort(
                    list(self.dictionary_list)
                )

            # pop and fetch the size required
            words = [self.words.pop(0) for _ in range(0, word_size)]

            # return the required dataset_size
            return words

        @property
        def word_groups(self):
            """Group words into a list of word-lists, ideal for making sentences.
            e.g. [the, cat, sat, on, the, mat,] ==> # [the, cat], [sat, on], [the, mat]"""

            wrd_lst = self.word_list
            return [
                wrd_lst[n : n + randint(8, 11)]
                for n in range(0, len(wrd_lst), randint(8, 11))
            ]

        @property
        def sentence_groups(self):
            """Convert the lists of word-lists into list of sentences with capital
            letters and full stops."""

            return [
                "{}.".format(" ".join(words).capitalize())
                for words in self.word_groups
            ]

        @property
        def paragraph_groups(self):
            """Groups the list of sentences into a list of sentence lists."""

            sentence_groups = self.sentence_groups
            return [
                sentence_groups[n : n + randint(3, 7)]
                for n in range(0, len(sentence_groups), randint(3, 7))
            ]

        @property
        def plaintext_bullet_groups(self):
            """Instead of combining sentences into paragraphs, make them plaintext bullets."""

            return [
                " + {}\n".format(" ".join(words).capitalize())
                for words in self.word_groups
            ]

        @property
        def plaintext_paragraphs_groups(self):
            """Combine sentences into paragraphs."""

            return [
                "{}\n\n".format(" ".join(sentences))
                for sentences in self.paragraph_groups
            ]

        @property
        def html_bullet_groups(self):
            """Instead of combining sentences into paragraphs, make them html bullets."""

            return IBlurb.Words._make_bullet_groups(self.sentence_groups)

        @property
        def html_paragraphs_groups(self):
            """Make html paragraphs."""

            return [
                "<p>{}</p>".format(" ".join(sentences))
                for sentences in self.paragraph_groups
            ]

        def _make_bullet_groups(sentence_groups):
            """helper class reused"""

            return [f"<li>{sentence}.</li>" for sentence in sentence_groups]
