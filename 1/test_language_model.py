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
        expected = { ("My", "name"):2, ("name","is"):2, ("is", "Sam"):1, ("is", "Bob"):1 }
        assert self.model().counted_bigrams(sentences) == expected

    def test_number_of_unique_words(self):
        training_data = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        assert self.model().number_of_unique_words(training_data) == 5

    def test_likelihood(self):
        training_data = [["This", "makes", "no", "sense"],["something", "else"]]
        model = self.model()
        model.train(training_data)
        assert model.likelihood(("no","sense")) == 1
        assert model.likelihood(("no","fence")) == 0
