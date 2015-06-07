import pos_tagger
import pytest

class TestPosTagger:
    @pytest.fixture
    def path(self):
        return "./GENIA_test2/"

    @pytest.fixture
    def tagger(self):
        return pos_tagger.PosTagger(self.path())

    def test_random_partitions(self):
        tagger = self.tagger()
        input = [1,2,3,4,5,6,7,8,9,0]
        rp = tagger.random_partitions(10, input)
        assert sorted(rp) == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9] ]

    def test_compare(self):
        tagger = self.tagger()
        actual = [("I", "NN"), ("am", "VB"), ("a", "DT"), ("sentence", "NN")]
        expected = [("I", "NN"), ("am", "VB"), ("a", "DT"), ("sentence", "VB")]
        assert tagger.compare(actual, expected) == (3, 1)

    def test_run(self):
        tagger = self.tagger()
        tagger.run(10)
        assert tagger.precision() == 1.0



