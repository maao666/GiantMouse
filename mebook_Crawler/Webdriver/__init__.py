from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
import logging
from pathlib import Path

__all__ = ['get_Edge_driver', 'get_Chrome_driver', 'get_Safari_driver']

logging.basicConfig(level=logging.DEBUG)


def get_Edge_driver(webdriver_executable="msedgedriver"):
    current_dir = Path(__file__).resolve().parent
    edge_web_driver_path = "{0}/{1}".format(
        current_dir, webdriver_executable)
    print(edge_web_driver_path)
    return webdriver.Edge(edge_web_driver_path, port=9515)


def get_Chrome_driver(webdriver_executable="chromedriver"):
    current_dir = Path(__file__).resolve().parent
    edge_web_driver_path = "{0}/{1}".format(
        current_dir, webdriver_executable)
    return webdriver.Chrome(edge_web_driver_path)


def get_Safari_driver(webdriver_executable="/usr/bin/safaridriver"):
    # $ safaridriver --enable
    return webdriver.Safari(webdriver_executable)
