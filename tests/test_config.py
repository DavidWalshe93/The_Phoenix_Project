"""
Author:     David Walshe
Date:       10 May 2021
"""

import pytest

import config as sut


def test_dev_config_retrieval():
    """
    :GIVEN: The string "prod".
    :WHEN:  Requesting the DevelopmentConfig object.
    :THEN:  Verify the DevelopmentConfig object is returned.
    """
    assert sut.get_config("dev") == sut.DevelopmentConfig


def test_test_config_retrieval():
    """
    :GIVEN: The string "prod".
    :WHEN:  Requesting the TestConfig object.
    :THEN:  Verify the TestConfig object is returned.
    """
    assert sut.get_config("test") == sut.TestConfig


def test_prod_config_retrieval():
    """
    :GIVEN: The string "prod".
    :WHEN:  Requesting the ProductionConfig object.
    :THEN:  Verify the ProductionConfig object is returned.
    """
    assert sut.get_config("prod") == sut.ProductionConfig


def test_arbitrary_string_config_retrieval():
    """
    :GIVEN: The string "foobar".
    :WHEN:  Requesting the a configuration with a arbitrary string.
    :THEN:  Verify the DevelopmentConfig (default) object is returned.
    """
    assert sut.get_config("foobar") == sut.DevelopmentConfig


def test_default_config_retrieval():
    """
    :GIVEN: No string selector.
    :WHEN:  Requesting the a configuration without a selector.
    :THEN:  Verify the DevelopmentConfig (default) object is returned.
    """
    assert sut.get_config() == sut.DevelopmentConfig

