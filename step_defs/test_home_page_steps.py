# from pytest_bdd import given, parsers, scenarios, then, when
from pytest_bdd import parsers, scenarios, then, when
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base import BasePage

# from pages.home import HomePage

scenarios('../features/home_page.feature')


@when(parsers.parse(
    'I have navigated to the \'ya\' "{page_name}" page')
)
def navigate_to(homepage, page_name):
    url = BasePage.PAGE_URLS.get(page_name.lower())
    homepage.browser.get(url)


@then(parsers.parse('the page "{name}"  page opens'))
def verify_page_title(homepage, name):
    assert BasePage.PAGE_URLS[name] in homepage.get_current_url()


@then('the if i click popup "all service" contains a "маркет"')
def verify_content_all_service(homepage):
    assert homepage.click_or_send(homepage.ALL_SERVICE), (
        'Не обнаружен блок "Все сервисы"')


@when('I click the "маркет" opens a tab with the "маркет"  and go to it')
def change_tabs(homepage):
    assert homepage.click_or_send(homepage.MARKET), (
        'Не обнаружена ссыылка "маркет"')
    p = homepage.browser.current_window_handle
    chwd = homepage.browser.window_handles
    for w in chwd:
        # switch focus to child window
        homepage.browser.switch_to.window(w)
        if BasePage.PAGE_URLS['маркет'] in homepage.get_current_url():
            return

    homepage.browser.switch_to.window(p)
    assert False, 'Not found tabs "market"'


@then(parsers.parse('the "{page}" page opens'))
def verify_page_opens(homepage, page):
    assert BasePage.PAGE_URLS.get(page.lower()) == homepage.get_current_url()


@then('element "каталог" found of page')
def found_katalog(homepage):
    assert len(homepage.browser.find_elements(*homepage.KATALOG)) == 1, (
        'Проверьте правильность ссылки на "каталог"')


@when('I click "каталог"')
def click_katalog(homepage):
    assert homepage.click_or_send(homepage.KATALOG), 'Не обнаружен "каталог"'


@then('select "smartphones"')
def select_smartphones(homepage):
    assert homepage.click_or_send(homepage.SMARTPHONES), (
        'Проверьте наличиее ссылки на "смартфоны"')


@when('Go to All Filters')
def go_all_filters(homepage):
    assert homepage.click_or_send(homepage.ALL_FILTERS), (
        'Не найдена кнопка "Все фильтры"')


@then(parsers.parse('Search parameter \'price\' to and set "{price}" rubles'))
def set_price_to(homepage, price):
    to_send = price + Keys.PAGE_DOWN
    assert homepage.click_or_send(homepage.FLF_PRICE_TO, to_send), (
        'Не найдено поле "Цена до"')


@then(parsers.parse('Screen diagonal from "{diagonal}" inches'))
def set_diagonal_from(homepage, diagonal):
    homepage.scroll_down()
    assert homepage.click_or_send(homepage.FLT_DIAGONAL_EXPAND), (
        'Не найдено поле "Диагональ точно"')
    to_send = diagonal + Keys.PAGE_DOWN
    assert homepage.click_or_send(homepage.FLF_DIAGONAL_FROM, to_send), (
        'Не найдено поле "Диагональ от"')


@then(parsers.parse('Select at least "{count:d}" of any manufacturers'))
def select_vendors(homepage, count):
    while homepage.get_count_elements(homepage.FLT_VENDORS) < count:
        assert homepage.click_or_send(homepage.FLT_VENDORS_ADD), (
            'Недостаточно производителей для выбора')
    for i in range(count):
        assert homepage.click_or_send(homepage.FLT_VENDORS, num_to_click=i), (
            'Ошибка выбора производителей')


@when('Click "Show..." (on filters)')
def show(homepage):
    assert homepage.click_or_send(homepage.FLT_SHOW), (
        'Не найдена кнопка "Показать ..."')


@then(parsers.parse('Count the smartphones on one page and great "{total:d}"'))
def count_phones_per_page(homepage, total):
    total_smartphones_count = homepage.get_count_elements(
        homepage.ITEMS_SMARTPHONES
    )
    assert total_smartphones_count > total
    print(f'Смартфонов на странице всего {total_smartphones_count}!')


@then('Remember name the last smartphones of the list')
def remember_name_last_smartphones(homepage):
    smartphones = homepage.browser.find_elements(*homepage.ITEMS_SMARTPHONES)
    assert len(smartphones) > 0, (
        'Проверьте правильность представления карточек товара')
    last_smartphone = smartphones[-1]
    last_smartphones_name = homepage.get_smartfone_name(last_smartphone)
    homepage.store_smartphone_name(last_smartphones_name)


@when('Change Sort to another (by price)')
def change_sort_to_price(homepage):
    assert homepage.click_or_send(homepage.BY_PRICE), (
        'Не найдена сортировка "по цене"')


@then('Find the page of exist the stored object')
def find_page_exist_name(homepage):
    homepage.find_page_with_stored_name()


@then('Click on the name of the stored object')
def open_by_store_name(homepage):
    homepage.open_page_with_stored_name()


@then('Display the rating of the selected item')
def display_rating(homepage):
    print(f'Рейтиг открытого товара: {homepage.get_rating()}!')
