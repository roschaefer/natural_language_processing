import perplexity
import pytest

class TestLanguageModel:
    @pytest.fixture
    def model(self):
        return perplexity.LanguageModel()

    def test_raw_bigrams(self):
        sentences = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        expected = [ ("My", "name"), ("name","is"), ("is", "Sam"), ("My", "name"), ("name", "is"), ("is", "Bob")]
        assert expected == self.model().raw_bigrams(sentences)

    def test_counted_bigrams(self):
        sentences = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
