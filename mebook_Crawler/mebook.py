import logging
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import zipfile
from glob import glob
import jiagu

logging.basicConfig(level=logging.DEBUG)

def unzip_daemon(watching_dir:str):
    glob(watching_dir)

def launch():
    current_dir = Path(__file__).resolve().parent
    options = Options()
    # options.add_argument('--headless')
    options.add_argument("--window-size=1366,768")
    options.add_experimental_option("prefs", {
        "download.default_directory": str(current_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    edge_web_driver_path = "{0}/Webdriver/{1}".format(
        current_dir, "chromedriver")
    chrome = webdriver.Chrome(edge_web_driver_path, chrome_options=options)

    chrome.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': str(current_dir)}}
    chrome.execute("send_command", params)
    return chrome


def book_page(chrome: WebDriver, target_url=''):
    PASSWORD_KEYWORD = "天翼云盘密码："
    if target_url != '':
        chrome.get(target_url)

    logging.info(chrome.title)
    chrome.find_element_by_partial_link_text("点击下载").click()

    all_handles = chrome.window_handles
    chrome.switch_to.window(all_handles[-1])

    download_password = chrome.find_element_by_xpath("/html/body/div[3]/p[6]")

    keyword_index = download_password.text.find(PASSWORD_KEYWORD)
    password = download_password.text[keyword_index +
                                      len(PASSWORD_KEYWORD):
                                      keyword_index + len(PASSWORD_KEYWORD) + 4]
    logging.info("Got password: {0}".format(password))
    chrome.find_element_by_partial_link_text("推荐").click()
    return password


def navigate_to_last_tab(chrome: WebDriver):
    all_handles = chrome.window_handles
    chrome.switch_to.window(all_handles[-1])
    logging.info("Swwiched to {0}".format(chrome.title))


def cloud189(chrome: WebDriver, url="", password=""):
    if url != '':
        chrome.get(url)

    while password != '':
        try:
            sleep(0.5)
            chrome.find_element_by_id("code_txt").send_keys(password)
            chrome.find_element_by_partial_link_text("访问").click()
            break
        except Exception:
            continue

    while True:
        try:
            sleep(0.5)
            download_button = chrome.find_element_by_class_name("btn-download")
            ActionChains(chrome).move_to_element(download_button).perform()
            download_button.click()
            break
        except Exception:
            continue

    for i in range(4):
        try:
            sleep(0.5)
            chrome.switch_to.frame("udb_login")
            chrome.find_element_by_xpath(
                '''//*[@id="userName"]''').send_keys("18953197117")
            sleep(1)
            chrome.find_element_by_xpath(
                '''//*[@id="password"]''').send_keys("Cb19985466")
            sleep(1)
            chrome.find_element_by_id("j-login").click()
            break
        except Exception:
            continue


def close_other_tabs(chrome: WebDriver):
    all_handles = chrome.window_handles
    while(len(all_handles) > 1):
        chrome.close()
        sleep(0.5)
        all_handles = chrome.window_handles
        chrome.switch_to.window(all_handles[-1])


def get_book_list(chrome: WebDriver, url):
    chrome.get(url)
    url_list = []
    blacklist = ["tag"]
    elements_list = chrome.find_elements_by_partial_link_text("epub")
    for element in elements_list:
        target_url = element.get_attribute("href")
        for word in blacklist:
            if not word in target_url:
                url_list.append(target_url)
    return url_list


def fetch_books(chrome: WebDriver, url_list):
    for book_url in url_list:
        logging.info("Going to {}".format(book_url))
        password = book_page(chrome, book_url)
        navigate_to_last_tab(chrome)
        cloud189(chrome, password=password)
        sleep(1)  # Wait for the download to start
        # close_other_tabs(chrome)


def main():
    chrome = launch()
    # url_list = get_book_list(chrome, "http://mebook.cc")
    fetch_books(chrome, ["http://www.shuwu.mobi/30015.html"])
    sleep(30)
    # chrome.quit()


if __name__ == '__main__':
    main()
