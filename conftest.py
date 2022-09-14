import json

import pytest
from pytest_bdd import given  # , parsers
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.home import HomePage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store")


@pytest.fixture
def config(request, scope='session'):

    BROWSERS = ['Chrome', 'Firefox']

    # Read config file
    with open('config.json') as config_file:
        config = json.load(config_file)

    browser = request.config.option.browser
    if browser is not None:
        config['browser'] = browser

    # Assert values are acceptable
    assert config['browser'] in BROWSERS
    assert isinstance(config['headless'], bool)
    assert isinstance(config['implicit_wait'], int)
    assert config['implicit_wait'] > 0

    # Return config so it can be used
    return config


@pytest.fixture
def browser(config):

    # Initialize the WebDriver instance
    if config['browser'] == 'Chrome':
        opts = webdriver.ChromeOptions()
        if config['headless']:
            opts.add_argument('headless')
        s = Service(ChromeDriverManager().install())
        b = webdriver.Chrome(service=s, options=opts)
    elif config['browser'] == 'Firefox':
        opts = webdriver.FirefoxOptions()
        if config['headless']:
            opts.headless = True
        b = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(), options=opts)
    else:
        raise Exception(f'Browser "{config["browser"]}" is not supported')

    # Make call wait up to 10 seconds for elements to appear
    b.implicitly_wait(config['implicit_wait'])

    # Return the WebDriver instance for the setup
    yield b

    # Quit the WebDriver instance for the teardown
    b.quit()


@pytest.fixture
def homepage(browser):
    return HomePage(browser)


@given('I open the browser and expand to the full screen')
def full_screen_browser(homepage):
    homepage.browser.maximize_window()


def write_line(request, when, line):
    """Write line instantly."""
    terminal_reporter = request.config.pluginmanager.get_plugin('terminalreporter')
    capture_manager = request.config.pluginmanager.get_plugin('capturemanager')
    with capture_manager.global_and_fixture_disabled():
        terminal_reporter.write(line+'\r\n')


@pytest.mark.trylast
def pytest_bdd_before_scenario(request, feature, scenario):
    write_line(request, 'setup', u'Scenario: {scenario.name}'.format(scenario=scenario))


@pytest.mark.trylast
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    write_line(request, 'call', u'Step: {step.name} FAILED'.format(step=step))


@pytest.mark.trylast
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    write_line(request, 'call', u'Step: {step.name} PASSED'.format(step=step))