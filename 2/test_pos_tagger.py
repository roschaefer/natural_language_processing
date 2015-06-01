import pos_tagger
import pytest
from IPython import embed

class TestPosTagger:
    @pytest.fixture
    def path(self):
        return "./GENIA_test/"

    @pytest.fixture
    def tagger(self):
        return pos_tagger.PosTagger(self.path())

    def test_random_partitions(self):
        tagger = self.tagger()
        input = [1,2,3,4,5,6,7,8,9,0]
        rp = tagger.random_partitions(10, input)
        assert sorted(rp) == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9] ]


