"""Test configuration use.
"""

import pathlib
import shutil

from click.testing import CliRunner
import pytest

from arbory import arb, const


@pytest.fixture
def temp_config(tmpdir):
    cfg_perm = pathlib.Path('arbory') / 'config.ini'
    cfg_temp = pathlib.Path(tmpdir) / 'config.ini'
    shutil.copyfile(cfg_perm, cfg_temp)
    yield
    shutil.copyfile(cfg_temp, cfg_perm)


def test_show_config():
    runner = CliRunner()
    result = runner.invoke(arb, ['config'])
    assert result.output == 'Current configuration: DEFAULT\n'


@pytest.mark.usefixtures('temp_config')
def test_use():
    runner = CliRunner()
    result = runner.invoke(arb, ['config', 'use', 'yo'])
    assert result.output == "'yo' does not exist.\n"
    result = runner.invoke(arb, ['config', 'use', 'cobalt'])
    assert result.output == 'Configuration selected: cobalt\n'


@pytest.mark.usefixtures('temp_config')
def test_available():
    runner = CliRunner()
    result = runner.invoke(arb, ['config', 'available'])
    assert result.output == 'DEFAULT\ncobalt\n'


@pytest.mark.usefixtures('temp_config')
def test_options():
    runner = CliRunner()
    result = runner.invoke(arb, ['config', 'options'])
    for opt in ('dir_color_fg', 'dir_color_bg', 'file_color_fg'):
        assert opt in result.output
    assert const.KW_CONF_SEL not in result.output
