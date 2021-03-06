import text_categorization
import pytest


class TestDataSet:
    @pytest.fixture
    def path(self):
        return "./ohsumed-test/"

    @pytest.fixture
    def data_set(self):
        return text_categorization.DataSet(self.path())

    def test_target(self):
        assert self.data_set().target == [0,0,0,1,1,1,1,1]

    def test_target_names(self):
        assert self.data_set().target_names == ["C01","C02"]


