import genia
import pytest
from IPython import embed

class TestArticle:
    @pytest.fixture
    def path(self):
        return "./GENIA_test/"

    @pytest.fixture
    def article(self, location):
        return genia.Article(self.path() + location + '.xml')

    def test_word_sentences(self):
        article = self.article('test1')
        assert article.word_sentences == [['A', 'sentence', 'for', 'the', 'testing', 'of', 'the', 'genia', 'class', '.']]

    def test_tag_sentences(self):
        article = self.article('test1')
        assert article.tag_sentences == [['DT', 'NN', 'IN', 'DT', 'NN', 'IN', 'DT', 'NN', 'NN', 'PERIOD']]
