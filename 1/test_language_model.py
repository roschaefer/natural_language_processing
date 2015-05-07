import perplexity
import pytest

class TestLanguageModel:
    @pytest.fixture
    def model(self, training_data):
        return perplexity.LanguageModel(training_data)

    def test_raw_unigrams(self):
        training_data = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        expected = [ ("My"), ("name"), ("is"), ("Sam"), ("My"), ("name"), ("is"), ("Bob") ]
        model = self.model(training_data)
        assert model.raw_unigrams() == expected

    def test_counted_unigrams(self):
        training_data = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        expected = { ("My"):2, ("name"):2, ("is"):2, ("Sam"):1, ("Bob"):1 }
        model = self.model(training_data)
        assert model.counted_unigrams() == expected

    def test_raw_bigrams(self):
        training_data = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        expected = [ ("My", "name"), ("name","is"), ("is", "Sam"), ("My", "name"), ("name", "is"), ("is", "Bob")]
        model = self.model(training_data)
        assert expected == model.raw_bigrams()

    def test_counted_bigrams(self):
        training_data = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        expected = { ("My", "name"):2, ("name","is"):2, ("is", "Sam"):1, ("is", "Bob"):1 }
        model = self.model(training_data)
        assert model.counted_bigrams() == expected

    def test_number_of_unique_words(self):
        training_data = [["My", "name", "is", "Sam"], ["My", "name", "is", "Bob"]]
        model = self.model(training_data)
        assert model.number_of_unique_words() == 5

    def test_likelihood_bigram(self):
        training_data = [["This", "makes", "no", "sense"]]
        model = self.model(training_data)
        assert model.likelihood(("no","sense")) == 1
        assert model.likelihood(("no","fence")) == 0

    def test_likelihood_sentence(self):
        training_data = [["This", "makes", "no", "sense"]]
        test = ["no", "makes", "sense"]
        model = self.model(training_data)
        assert model.likelihood(training_data[0]) == 1
        assert model.likelihood(test) == 0
