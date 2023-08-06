import logging
import sys
import random

import pytest

from azureml.studio.core.logger import logger, time_profile, _LoggerContext, LOGGER_TAG, LogHandler, get_logger
from azureml.studio.core.logger import log_dict_values, log_list_values, module_host_logger


def test_logging_level(caplog):
    logger.debug("Module debug is allowed")

    root_logger = logging.getLogger()
    root_logger.debug("Debug is disabled")
    root_logger.info("Info is disabled")
    root_logger.warning("Warning is expected")

    other_logger = logging.getLogger("other_logger")
    other_logger.debug("Debug is disabled")
    other_logger.info("Info is disabled")
    other_logger.warning("Warning is expected")

    assert "Module debug is allowed" in caplog.text
    assert 'Debug is disabled' not in caplog.text
    assert 'Info is disabled' not in caplog.text


@time_profile
def func1():
    return


@time_profile
def func2():
    return func1()


def test_logging_context(capsys):
    hdl = LogHandler(sys.stdout)
    logger.addHandler(hdl)
    func2()
    out, err = capsys.readouterr()
    lines = out.split('\n')[:-1]
    func2_pos = lines[0].find('func2')

    assert all((LOGGER_TAG in line for line in lines))
    assert func2_pos > 0
    assert func2_pos == lines[-1].find('func2')
    func1_pos = lines[1].find('func1')
    assert func1_pos > 0
    assert func1_pos == lines[-2].find('func1')
    assert func1_pos == func2_pos + _LoggerContext.INDENT_SIZE
    logger.removeHandler(hdl)


def test_get_logger():
    from azureml.studio.core.logger import root_logger
    assert get_logger() == root_logger

    with pytest.raises(ValueError, match="Invalid log name 'Uppercase'. Should only contains lowercase letters"):
        assert get_logger('Uppercase')

    valid_logger = get_logger('valid')
    assert valid_logger is not None


def test_log_list_values(capsys):
    hdl = LogHandler(sys.stdout)
    logger.addHandler(hdl)
    list_value = ['aaa', 'bbb', 'ccc']
    list_name = 'A List'
    log_list_values(list_name, list_value)
    out, err = capsys.readouterr()
    lines = out.split('\n')
    assert list_name in lines[0]
    for i, (val, line) in enumerate(zip(list_value, lines[1:])):
        assert f'|   [{i}] = {val}' in line
        assert 'omitted' not in line


def test_log_list_values_empty(capsys):
    hdl = LogHandler(sys.stdout)
    logger.addHandler(hdl)
    log_list_values('Empty', None)
    out, err = capsys.readouterr()
    assert '(empty)' in out


def test_log_list_values_truncate_log(capsys):
    hdl = LogHandler(sys.stdout)
    logger.addHandler(hdl)
    long_list = [[1]*1000, [2]]
    log_list_values('long_list', long_list, truncate_long_item_text=True)
    out, err = capsys.readouterr()
    assert f'omitted 2500 chars' in out


def test_log_dict_values(capsys):
    hdl = LogHandler(sys.stdout)
    logger.addHandler(hdl)
    dict_value = {'k1': 'aaa', 'k2': 'bbb'}
    dict_name = 'A Dict'
    log_dict_values(dict_name, dict_value)
    out, err = capsys.readouterr()
    lines = out.split('\n')
    assert dict_name in lines[0]
    for (key, val), line in zip(dict_value.items(), lines[1:]):
        assert f'|   {key} = {val}' in line
        assert 'omitted' not in line


def test_log_dict_values_truncate_log(capsys):
    hdl = LogHandler(sys.stdout)
    logger.addHandler(hdl)
    long_dct = {"long": [1]*1000}
    log_dict_values('long_list', long_dct, truncate_long_item_text=True)
    out, err = capsys.readouterr()
    assert f'omitted 2500 chars' in out


def test_log_dict_values_empty(capsys):
    hdl = LogHandler(sys.stdout)
    logger.addHandler(hdl)
    log_dict_values('Empty', None)
    out, err = capsys.readouterr()
    assert '(empty)' in out


def test_large_exception_msg(capsys):
    estimated_log_limit = 2000
    hdl = LogHandler(sys.stderr)
    module_host_logger.addHandler(hdl)
    array_size = 1000
    try:
        large_array = [random.randint(10, 100)] * array_size
        large_array[array_size+1] = 'abc'
    except BaseException as bex:
        module_host_logger.exception(f"Expected exception: {bex}")
    out, err = capsys.readouterr()
    assert "large_array" in err
    assert "IndexError: list assignment index out of range" in err
    assert "omitted" in err
    assert len(err) < estimated_log_limit


def test_small_exception_msg(capsys):
    hdl = LogHandler(sys.stderr)
    module_host_logger.addHandler(hdl)
    array_size = 1
    try:
        small_array = [random.randint(10, 100)] * array_size
        small_array[array_size+1] = 'abc'
    except BaseException as bex:
        module_host_logger.exception(f"Expected exception: {bex}")
    out, err = capsys.readouterr()
    assert "small_array" in err
    assert "IndexError: list assignment index out of range" in err
    assert "omitted" not in err
