import markov
import pytest

class TestModel:

    @pytest.fixture
    def model(self, word_tag_sentences):
        return markov.Model(word_tag_sentences)

    @pytest.fixture
    def example_model(self):
        word_tag_sentences = [
                [("I", "NN"), ("am", "VB"), ("a", "DT"), ("sentence", "NN")],
                [("I", "NN"), ("love", "VB"), ("the", "DT"), ("sun", "NN")],
                [("I", "NN"), ("love", "VB"), ("your", "PP"), ("love", "NN")]
        ]
        return self.model(word_tag_sentences)

    def test_context(self):
        model = self.example_model()
        assert model.context['I'] == 3
        assert model.context['love'] == 3
        assert model.context['sun'] == 1
        assert model.context['<s>'] == 3
        assert model.context['</s>'] == 0 # okay, we transition the end of a sentence but don't count it, is that correct?

    def test_transition(self):
        model = self.example_model()
        assert model.transition[('<s>', 'NN')] == 3
        assert model.transition[('NN', '</s>')] == 3
        assert model.transition[('NN', 'VB')] == 3
        assert model.transition[('VB', 'NN')] == 0

    def test_emit(self):
        model = self.example_model()
        assert model.emit[('VB', 'am')] == 1
        assert model.emit[('NN', 'sentence')] == 1
        assert model.emit[('DT', 'the')] == 1
        assert model.emit[('NN', 'the')] == 0

    def test_possible_tags(self):
        model = self.example_model()
        assert model.possible_tags == set(["NN", "VB", "DT", "PP"])

    def test_prob_t(self):
        model = self.example_model()
        assert model.prob_t("DT", "VB") == 0.5
        assert model.prob_t("VB", "NN") > 0.5
        assert model.prob_t("PP", "VB") == 0.4

    def test_prob_e(self):
        model = self.example_model()
        assert model.prob_e("love", "VB") == 0.25


    def test_tag(self):
        model = self.example_model()
        sentence = ["I", "am", "the", "sun"]
        assert model.tag(sentence) ==  [('I', 'NN'), ('am', 'VB'), ('the', 'DT'), ('sun', 'NN')]
