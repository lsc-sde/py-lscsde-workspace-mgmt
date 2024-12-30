from ..models import KubernetesHelper
import pytest
from ..exceptions import InvalidLabelFormatException

class TestKubernetesHelper:
    def test_format_label_basic(self):
        helper = KubernetesHelper()
        test1 = helper.format_as_label("joe.blogs@someplace.co.uk")
        assert "joe.blogs___someplace.co.uk" == test1

    def test_format_label_apostrophe(self):
        helper = KubernetesHelper()
        test1 = helper.format_as_label("joe.o'keef@someplace.co.uk")
        assert "joe.o___keef___someplace.co.uk" == test1

    def test_format_label_apostrophe_ending_with_special(self):
        helper = KubernetesHelper()
        with pytest.raises(InvalidLabelFormatException):
            test1 = helper.format_as_label("joe.o'keef@someplace.co.uk!")
