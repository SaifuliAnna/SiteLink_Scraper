import json
import logging
import os
import time
# from unittest.mock import patch, mock_open, call

import pytest
from selenium import webdriver

from link_scraper import (get_additional_details, get_unique_links,
                          initialize_webdriver, main, read_json_data,
                          save_to_json)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@pytest.fixture
def driver_mock():
    # Initializing a custom driver for use in tests
    return webdriver.Chrome()


@pytest.fixture
def sample_data():
    return [{"key1": "value1", "key2": "value2"},
            {"key3": "value3", "key4": "value4"},
            ]


@pytest.fixture
def json_file_path(tmpdir):
    return tmpdir.join("test_data.json").strpath


#  ---------------------------------------------------
@pytest.fixture
def json_data():
    return read_json_data("json_data_for_link.json")


def test_read_json_data_fix(json_data):
    expected_json_data = json_data
    assert expected_json_data is not None

    # Checks if the nodeCssSelector key is present in the loaded data
    assert "nodeCssSelector" in expected_json_data

    # Checks if the "nodeCssSelector" key value is a string
    assert isinstance(expected_json_data["nodeCssSelector"], str)

#  ---------------------------------------------------


def test_read_json_data():
    json_data = read_json_data("json_data_for_link.json")
    assert json_data is not None

    # Checks if the nodeCssSelector key is present in the loaded data
    assert "nodeCssSelector" in json_data

    # Checks if the "nodeCssSelector" key value is a string
    assert isinstance(json_data["nodeCssSelector"], str)


def test_initialize_webdriver():
    driver = initialize_webdriver()
    assert driver is not None

    # Checks if the driver is an instance of the webdriver class. Chrome
    assert isinstance(driver, webdriver.Chrome)


def test_get_unique_link(driver_mock):
    # Test Case Parameters
    xpath = '//div[@id="divMainResult"]//div[@class="shell"]'
    json_data = {
        "nodeCssSelector": ".list-order > div:nth-child(1) > ul:nth-child(1) > li:nth-child(4) > a:nth-child(1)"
    }

    # Function call and runtime measurement
    result = get_unique_links(driver_mock, xpath, json_data)

    # Check the number of results obtained
    assert len(result) >= 0, f"Expected at least 0 links, but got {len(result)}"

    # Check the format of the results
    for ad in result:
        assert "link" in ad
        assert "title" in ad
        assert "region" in ad
        assert "address" in ad
        assert "price" in ad

    print("Test completed successfully!")


def test_get_additional_details(driver_mock):
    # Preparation of labeled data
    rent_data_list = [
        {"link": "https://example.com/property/1"},
        {"link": "https://example.com/property/2"},
    ]

    # Function call and runtime measurement
    result = get_additional_details(driver_mock, rent_data_list)

    # Checks if the function modifies the input list rent_data_list
    assert (
        result is rent_data_list
    ), "The function should modify the input list in-place"

    # Checks if each object has additional data installed
    for rent_data in rent_data_list:
        assert "description" in rent_data
        assert "update_date" in rent_data
        assert "images" in rent_data

    print("Test completed successfully!")


def test_save_to_json(sample_data, json_file_path):
    # Arrange
    expected_data = sample_data

    # Act
    save_to_json(sample_data, json_file_path)

    # Assert
    assert os.path.exists(json_file_path)

    with open(json_file_path, "r", encoding="utf-8") as json_file:
        actual_data = json.load(json_file)

    assert actual_data == expected_data
