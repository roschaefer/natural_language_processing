import perplexity
import pytest

class TestLanguageModel:
    @pytest.fixture
    def model(self):
        return perplexity.LanguageModel()

    def test_raw_unigrams(self):
        sentences = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        expected = [ ("My"), ("name"), ("is"), ("Sam"), ("My"), ("name"), ("is"), ("Bob") ]
        assert self.model().raw_unigrams(sentences) == expected

    def test_counted_unigrams(self):
        sentences = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        expected = { ("My"):2, ("name"):2, ("is"):2, ("Sam"):1, ("Bob"):1 }
        assert self.model().counted_unigrams(sentences) == expected


    def test_raw_bigrams(self):
        sentences = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        expected = [ ("My", "name"), ("name","is"), ("is", "Sam"), ("My", "name"), ("name", "is"), ("is", "Bob")]
        assert expected == self.model().raw_bigrams(sentences)

    def test_counted_bigrams(self):
        sentences = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        expected = { ("My", "name"):2,
                     ("name","is"):2,
                     ("is", "Sam"):1,
                     ("is", "Bob"):1
                    }
        assert self.model().counted_bigrams(sentences) == expected
