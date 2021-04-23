from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
import time

PRODUCT_PAGE_URL = ''


class Parser:

    @staticmethod
    def get_images(url: str) -> None:
        """
        Fetch images from a source URL, and save them.

        Arguments:
            - url (str): url from where to gather information.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('../chromedriver', options=chrome_options)
        driver.get(url=url)
        driver.find_element_by_id('photo-view').click()

        images: List[str] = []

        check_next_image = True
        while check_next_image:
            image_link = driver \
                .find_element_by_class_name('lg-current') \
                .find_element_by_class_name('lg-image') \
                .get_attribute('src')

            if image_link not in images:
                images.append(image_link)

                driver.find_element_by_class_name('lg-next').click()
                time.sleep(2)
            else:
                check_next_image = False

        with open('images.txt', 'w') as file:
            file.write('\n'.join(images))

        for index, image_url in enumerate(images):
            perfect_image_url: str = image_url \
                .replace('&watermark=brand', '') \
                .replace('&mode=crop', '') \
                .replace('&quality=50', '&quality=100')
            response = requests.get(url=perfect_image_url)

            with open(f'product_photo[{index}].png', 'wb') as image_file:
                image_file.write(response.content)


if __name__ == '__main__':
    Parser.get_images(url=PRODUCT_PAGE_URL)
