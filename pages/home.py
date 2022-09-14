from selenium.webdriver.common.by import By

from pages.base import BasePage

# from selenium.webdriver.common.keys import Keys


class HomePage(BasePage):

    ALL_SERVICE = (
        By.XPATH,
        '//a[@class="home-link2 services-pinned__item services-pinned__all"]'
    )
    MARKET = (
        By.XPATH,
        ('//div[@class="services-pinned__more-popup-item-title"'
         ' and contains(text(), "Маркет")]')
    )
    KATALOG = (By.CSS_SELECTOR, '[id="catalogPopupButton"]')
    SMARTPHONES = (
        By.XPATH,
        '//*[@id="catalogPopup"]//a[contains(text(), "Смартфоны")]'
    )
    ALL_FILTERS = (By.XPATH, '//span[contains(text(), "Все фильтры")]')
    FLF_PRICE_TO = (
        By.XPATH,
        '//*[@data-filter-id="glprice"]//div[@data-prefix="до"]//input'
    )
    FLT_DIAGONAL_EXPAND = (
        By.XPATH,
        '//button/h4[starts-with(text(), "Диагональ экрана (точно),")]'
    )
    FLF_DIAGONAL_FROM = (
        By.XPATH,
        ('//button/h4[starts-with(text(), "Диагональ экрана (точно),")]'
         '/../..//div[@data-prefix="от"]//input')
    )
    FLT_VENDORS = (
        By.XPATH,
        ('//div[./button/h4[contains(text(), "Производитель")]]'
         '//input[@type="checkbox"]//..')
    )
    FLT_VENDORS_ADD = (
        By.XPATH,
        '//button/span[starts-with(text(), "Показать ещё")]'
    )
    FLT_SHOW = (
        By.XPATH,
        '//a[starts-with(text(), "Показать")]'
    )
    ITEMS_SMARTPHONES = (
        By.XPATH,
        '//div[@data-index]'
    )
    SMARTPHONE_NAME = (
        By.XPATH,
        './/h3'
    )
    BY_PRICE = (
        By.XPATH,
        '//button[contains(text(), "по цене")]'
    )
    SHOW_MORE = (
        By.XPATH,
        '//button[.//span[contains(text(), "Показать ещё")]]'
    )
    RATING = (
        By.XPATH,
        '//span[@data-auto="rating-badge-value"]'
    )

    def __init__(self, browser):
        self.browser = browser
        self.smartphone_name = ''

    def get_page_title_text(self):
        return self.browser.title

    def get_current_url(self):
        return self.browser.current_url

    def click_or_send(self, selector, send=None, num_to_click=None):
        select = self.browser.find_elements(*selector)
        if num_to_click is None and len(select) != 1:
            return False
        if num_to_click is not None:
            if len(select) <= num_to_click:
                return False
            select[num_to_click].click()
            self.pause()
            return True
        if send is not None:
            select[0].send_keys(send)
            self.pause()
            return True
        select[0].click()
        self.pause()
        return True

    def get_count_elements(self, selector):
        self.scroll_down()
        return len(self.browser.find_elements(*selector))

    def get_smartfone_name(self, element):
        name = element.find_elements(*self.SMARTPHONE_NAME)
        assert len(name) == 1, (
            "Проверьте правильность представления имени телефона")
        return name[0].text

    def store_smartphone_name(self, name):
        self.smartphone_name = name

    def find_page_with_stored_name(self):
        while True:
            self.scroll_down()
            all_phones = self.browser.find_elements(*self.ITEMS_SMARTPHONES)
            if (self.smartphone_name not in
                    ([self.get_smartfone_name(now_phone)
                     for now_phone in all_phones])):
                assert self.click_or_send(self.SHOW_MORE), (
                    'Не удалось найти телефон с сохраненным '
                    f'именем{self.smartphone_name}')
                continue
            break

    def open_page_with_stored_name(self):
        self.scroll_down()
        all_phones = self.browser.find_elements(*self.ITEMS_SMARTPHONES)
        for now_phone in all_phones:
            if self.smartphone_name == self.get_smartfone_name(now_phone):
                chwd = self.browser.window_handles
                now_phone.find_element(*self.SMARTPHONE_NAME).click()
                assert chwd != self.browser.window_handles, (
                    'Ожидается отрытие новой вкладки'
                )
                self.browser.switch_to.window(self.browser.window_handles[-1])
                self.pause()
                return
        assert False, (
            'На текущей странице нет смартфона '
            f'с сохранненым именем{self.smartphone_name}!')

    def get_rating(self):
        ratings = self.browser.find_elements(*self.RATING)
        assert len(ratings) in (0, 2), (
            'Проверьте правильность формирования рейтинга товара'
        )
        if len(ratings) == 0:
            return None
        return ratings[1].text
