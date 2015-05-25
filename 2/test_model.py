import markov
import pytest
from IPython import embed

class TestModel:
    @pytest.fixture

    @pytest.fixture
    def model(self, word_tag_sentences):
        return markov.Model(word_tag_sentences)

    def example_model(self):
        word_tag_sentences = [
                [("I", "NN"), ("am", "VB"), ("a", "DT"), ("sentence", "NN")],
                [("I", "NN"), ("love", "VB"), ("the", "DT"), ("sun", "NN")]
        ]
        return self.model(word_tag_sentences)

    def test_context(self):
        model = self.example_model()
        assert model.context['I'] == 2
        assert model.context['love'] == 1
        assert model.context['sun'] == 1
        assert model.context['<s>'] == 2
        assert model.context['</s>'] == 0 # okay, we transition the end of a sentence but don't count it, is that correct?

    def test_transition(self):
        model = self.example_model()
        assert model.transition[('<s>', 'NN')] == 2
        assert model.transition[('NN', '</s>')] == 2
        assert model.transition[('NN', 'VB')] == 2
        assert model.transition[('VB', 'NN')] == 0

    def test_emit(self):
        model = self.example_model()
        assert model.emit[('VB', 'am')] == 1
        assert model.emit[('NN', 'sentence')] == 1
        assert model.emit[('DT', 'the')] == 1
        assert model.emit[('NN', 'the')] == 0

    def test_possible_tags(self):
        model = self.example_model()
        assert model.possible_tags == set(["NN", "VB", "DT"])

