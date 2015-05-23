import markov
import pytest
from IPython import embed

class TestModel:
    @pytest.fixture

    @pytest.fixture
    def model(self, word_tag_sentences):
        return markov.Model(word_tag_sentences)

    def test_word_sentence(self):
        word_tag_sentences = [
                [("I", "NN"), ("am", "VB"), ("a", "DT"), ("sentence", "NN")],
                [("I", "NN"), ("love", "VB"), ("the", "DT"), ("sun", "NN")]
        ]
        model = self.model(word_tag_sentences)
        assert model.context['I'] == 2
        assert model.context['love'] == 1
        assert model.context['sun'] == 1

