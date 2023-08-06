# -*- encoding: utf-8 -*-
import pytest
from liar.ijusthelp import rewrite_dict
from liar.iamaliar import IAmALiar

from liar.model.blurb import blurb


class TestClassIBlurb:

    small_number_records = 30
    blurb_maker = IAmALiar(small_number_records)
    test_blurb = rewrite_dict(
        blurb,
        {"name": "test_blurb", "language": "english", "min": 800, "max": 1000},
    )

    def test_plaintext_phrase(self):
        plaintext_phrase = rewrite_dict(
            self.test_blurb, {"method": "plaintext_phrase"}
        )
        d = self.blurb_maker.get_data([plaintext_phrase])
        assert len(d) == self.small_number_records
        assert "<" not in d[0]["test_blurb"]
        assert "\n" not in d[0]["test_blurb"]
        assert "." not in d[0]["test_blurb"]

    def test_plaintext_title(self):
        plaintext_title = rewrite_dict(
            self.test_blurb, {"method": "plaintext_title"}
        )
        d = self.blurb_maker.get_data([plaintext_title])
        assert len(d) == self.small_number_records
        assert "<" not in d[0]["test_blurb"]
        assert "\n" not in d[0]["test_blurb"]

    def test_plaintext_sentence(self):
        plaintext_sentence = rewrite_dict(
            self.test_blurb, {"method": "plaintext_sentence"}
        )
        d = self.blurb_maker.get_data([plaintext_sentence])
        assert len(d) == self.small_number_records
        assert "<" not in d[0]["test_blurb"]
        assert "\n" not in d[0]["test_blurb"]
        assert "." in d[0]["test_blurb"]

    def test_plaintext_sentences(self):
        plaintext_sentences = rewrite_dict(
            self.test_blurb, {"method": "plaintext_sentences"}
        )
        d = self.blurb_maker.get_data([plaintext_sentences])
        assert len(d) == self.small_number_records
        assert "<li>" not in d[0]["test_blurb"]
        assert "\n" not in d[0]["test_blurb"]
        assert "." in d[0]["test_blurb"]

    def test_plaintext_bullets(self):
        plaintext_bullets = rewrite_dict(
            self.test_blurb, {"method": "plaintext_bullets"}
        )
        d = self.blurb_maker.get_data([plaintext_bullets])
        assert len(d) == self.small_number_records
        assert "<li>" not in d[0]["test_blurb"]
        assert "\n" in d[0]["test_blurb"]

    def test_plaintext_paragraphs(self):
        plaintext_paragraphs = rewrite_dict(
            self.test_blurb, {"method": "plaintext_paragraphs"}
        )
        d = self.blurb_maker.get_data([plaintext_paragraphs])
        assert len(d) == self.small_number_records
        assert "<p>" not in d[0]["test_blurb"]
        assert "\n" in d[0]["test_blurb"]

    def test_html_paragraph(self):
        html_paragraph = rewrite_dict(
            self.test_blurb, {"method": "html_paragraph"}
        )
        d = self.blurb_maker.get_data([html_paragraph])
        assert len(d) == self.small_number_records
        assert "<p>" in d[0]["test_blurb"]

    def test_html_bullets(self):
        html_bullets = rewrite_dict(self.test_blurb, {"method": "html_bullets"})
        d = self.blurb_maker.get_data([html_bullets])
        assert len(d) == self.small_number_records
        assert "<li>" in d[0]["test_blurb"]

    def test_html_paragraphs(self):
        html_paragraphs = rewrite_dict(
            self.test_blurb, {"method": "html_paragraphs"}
        )
        d = self.blurb_maker.get_data([html_paragraphs])
        assert len(d) == self.small_number_records
        assert "<p>" in d[0]["test_blurb"]

    def test_html(self):
        html = rewrite_dict(self.test_blurb, {"method": "html"})
        d = self.blurb_maker.get_data([html])
        assert len(d) == self.small_number_records
        assert "<p>" in d[0]["test_blurb"]
