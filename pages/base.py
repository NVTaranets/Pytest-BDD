# from abc import ABC, abstractmethod
from abc import abstractmethod
from time import sleep

# from selenium.webdriver.common.by import By


class BasePage():

    SCROLL_PAUSE_TIME = 0.5
    PAUSE_TIME = 5
    BASE_URL = 'https://ya.ru'
    MARKET_URL = 'https://market.yandex.ru'

    PAGE_URLS = {
        'home': BASE_URL,
        'маркет': MARKET_URL,
    }

    @property
    @abstractmethod
    def PAGE_TITLE(self):
        pass

    @abstractmethod
    def get_page_title_text(self):
        pass

    def __init__(self, browser):
        self.browser = browser

    def scroll_down(self):

        # Get scroll height
        last_height = self.browser.execute_script(
            "return document.body.scrollHeight"
        )

        while True:
            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Wait to load page
            sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height

    def pause(self, time_pause=PAUSE_TIME):
        sleep(time_pause)
