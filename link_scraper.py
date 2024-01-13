import json
import re
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def read_json_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def initialize_webdriver():
    return webdriver.Chrome()


def get_unique_links(driver, xpath, json_data):
    rent_data_list = []

    while len(rent_data_list) < 60:
        ads = driver.find_elements(By.XPATH, xpath)

        for index, ad in enumerate(ads):
            rent_data = {
                "link": ad.find_element(
                    By.XPATH, './/a[@class="a-more-detail"]'
                ).get_attribute("href"),
                "title": ad.find_element(
                    By.XPATH,
                    './/div[@class="location-container"]/span[@class="category"]/div',
                ).text,
                "region": ad.find_element(
                    By.XPATH,
                    './/div[@class="location-container"]/span[@class="address"]/div[2]',
                ).text,
                "address": ad.find_element(
                    By.XPATH,
                    './/div[@class="location-container"]/span[@class="address"]/div[1]',
                ).text,
                "price": ad.find_element(
                    By.XPATH, './/div[@class="price"]/span[1]'
                ).text,
            }

            rent_data_list.append(rent_data)
            print(rent_data)

        try:
            next_page_element = driver.find_element(
                By.CSS_SELECTOR, json_data["nodeCssSelector"]
            )
            next_page_element.click()
            time.sleep(6)
        except NoSuchElementException:
            break

    return rent_data_list


def get_additional_details(driver, rent_data_list):
    for rent_data in rent_data_list:
        link_in_data_rent = rent_data["link"]
        driver.get(link_in_data_rent)

        driver.implicitly_wait(5)

        try:
            description_list = driver.find_elements(
                By.XPATH, '//div[@class="grid_3"]//div[@itemprop="description"]'
            )
            rent_data["description"] = " ".join(
                element.text for element in description_list
            )
        except NoSuchElementException:
            rent_data["description"] = None

        try:
            rent_data["update_date"] = driver.find_element(
                By.XPATH,
                '//div[@class="grid_3"]//table[@class="table table-striped"]//tr[1]/td[1]',
            ).text
        except NoSuchElementException:
            rent_data["update_date"] = None

        try:
            image_script = driver.find_element(
                By.XPATH, '//script[contains(text(), "window.MosaicPhotoUrls")]'
            ).get_attribute("innerHTML")
            image_links = re.findall(r'"(https://[^"]+)"', image_script)
            rent_data["images"] = image_links
        except NoSuchElementException:
            rent_data["images"] = []

        print(f"\n{rent_data}")

    return rent_data_list


def main():
    json_data = read_json_data("json_data_for_link.json")
    driver = initialize_webdriver()

    url = "https://realtylink.org/en/properties~for-rent"
    driver.get(url)
    driver.implicitly_wait(10)

    xpath_ads = '//div[@id="divMainResult"]//div[@class="shell"]'
    rent_data_list = get_unique_links(driver, xpath_ads, json_data)

    rent_data_list = get_additional_details(driver, rent_data_list)

    with open("data_website.json", "w", encoding="utf-8") as json_file:
        json.dump(rent_data_list, json_file, ensure_ascii=False, indent=2)

    driver.quit()


if __name__ == "__main__":
    main()
