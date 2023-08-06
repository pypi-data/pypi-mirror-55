# pylint: disable=missing-docstring

import os

from polarion_tools_common import configuration, utils

EXPECTED_CONFIG = {
    "blacklisted_tests": ["\\[.*rhev", "cfme/tests/containers/", "test_.*blacklisted"],
    "whitelisted_tests": [
        "cfme/tests/infrastructure/test_quota_tagging.py::test_.*\\[.*rhe?v",
        "cfme/tests/v2v",
        "test_.*whitelisted",
        "test_tenant_quota.py",
    ],
    "docstrings": {"required_fields": ["assignee", "initialEstimate", "status"]},
}


def test_get_config(data_dir):
    config_files = configuration.get_config_files(project_root=data_dir)
    config = configuration.get_config(config_files=config_files)
    assert config == EXPECTED_CONFIG


def test_merge_dict():
    dict_a = {
        "key1": "value1",
        "key2": {
            "subkey1": "subvalue1",
            "subkey2": {"subsubkey1": "subsubvalue1", "subsubkey2": "subsubvalue2"},
        },
        "key4": {"subkey1": "subvalue1", "subkey2": ["subsubvalue1", "subsubvalue2"]},
    }
    dict_b = {
        "key2": {
            "subkey2": {"subsubkey2": "newsubsubvalue2", "subsubkey3": "subsubvalue3"},
            "subkey3": "subvalue3",
        },
        "key3": "value3",
        "key4": {"subkey1": "subvalue2", "subkey2": ["subsubvalue2", "subsubvalue3"]},
    }
    result_dict = {
        "key1": "value1",
        "key2": {
            "subkey1": "subvalue1",
            "subkey2": {
                "subsubkey1": "subsubvalue1",
                "subsubkey2": "newsubsubvalue2",
                "subsubkey3": "subsubvalue3",
            },
            "subkey3": "subvalue3",
        },
        "key3": "value3",
        "key4": {
            "subkey1": "subvalue2",
            "subkey2": ["subsubvalue1", "subsubvalue2", "subsubvalue3"],
        },
    }

    assert utils.merge_dicts(dict_a, dict_b) == result_dict
    assert utils.merge_dicts("foo", {"bar": "baz"}) == "foo"
    assert utils.merge_dicts({"foo": ["foo", "baz"]}, {"foo": ["bar"]}) == {
        "foo": ["bar", "baz", "foo"]
    }
    assert utils.merge_dicts({"foo": {"foo", "baz"}}, {"foo": ["bar"]}) == {
        "foo": ["bar", "baz", "foo"]
    }
    assert utils.merge_dicts({"foo": ["foo", "baz"]}, {"foo": "bar"}) == {"foo": "bar"}


def test_find_vcs_root(root_dir):
    abs_root_dir = os.path.abspath(root_dir)
    vcs_root = utils.find_vcs_root("./")
    assert abs_root_dir == vcs_root


def test_find_in_parent_dir_1(root_dir):
    abs_root_dir = os.path.abspath(root_dir)
    search_path = os.path.join(abs_root_dir, "tests", "data", "stopdir")
    found = utils.find_in_parent_dirs(search_path, ("conftest.py",), stop_in=("stopdir",))
    assert found is None


def test_find_in_parent_dir_2(root_dir):
    abs_root_dir = os.path.abspath(root_dir)
    search_path = os.path.join(abs_root_dir, "tests", "data", "stopdir")
    found = utils.find_in_parent_dirs(search_path, ("conftest.py",))
    assert found.endswith("tests")


def test_unicode_str():
    assert isinstance(utils.get_unicode_str(b"foo"), str)
    ustr = "foo"
    assert ustr is utils.get_unicode_str(ustr)
    assert utils.get_unicode_str(("foo",)) == "('foo',)"
