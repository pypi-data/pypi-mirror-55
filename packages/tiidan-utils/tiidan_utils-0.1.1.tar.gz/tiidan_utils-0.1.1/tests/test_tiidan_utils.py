import logging
from click.testing import CliRunner
from tiidan_utils.cli import main
from tiidan_utils.util import log_function


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == "()\n"
    assert result.exit_code == 0
