import perplexity
import pytest

class TestRunner:
    @pytest.fixture
    def runner(self):
        return perplexity.Runner()

    def test_create_test_and_training_set(self):
        test, training = self.runner().create_test_and_training_sets([1,2,3,4,5,6,7,8,9,10])
        assert test == [1]
        assert training == [2,3,4,5,6,7,8,9,10]

    def test_create_test_and_training_set_modulo(self):
        test, training = self.runner().create_test_and_training_sets([1,2,3,4,5,6,7,8,9,10,11])
        assert test == [1, 11]
        assert training == [2,3,4,5,6,7,8,9,10]

    def test_create_test_and_training_set_randomly(self):
        input = [1,2,3,4,5,6,7,8,9,10,11,12]
        test, training = self.runner().create_test_and_training_sets_randomly(input)
        assert len(test) == 2
        assert len(training) == 10
        for e in input:
            ok = ((e in test) or (e in training))
            assert ok

    def test_get_articles(self):
        assert len(self.runner().get_articles('GENIA_treebank_v1/')) > 0




