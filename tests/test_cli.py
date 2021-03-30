from unittest.mock import patch
import pytest

from dbtea.cli import main


@patch("sys.argv", new=["dbtea", "--help"])
def test_help():
    with pytest.raises(SystemExit) as cm:
        main()
        assert cm.value.code == 0
