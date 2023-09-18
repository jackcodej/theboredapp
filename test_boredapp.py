import pytest
import flask
import server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# setting path

# """Tests to create
# UI
# -All unique elements for each HTML template
# -AJAX generated elements (note edge case for activities chosen by other users when database is freshly seeded)
# 
# Internal Query
# -Ensure query returns a result
# -Ensure adding a new activity exists
# -Test login
# -Test registration
# Test Server/CRUD/model operations
# """

# Create a test Flask app instance
@pytest.fixture
def client():
    server.app.config['TESTING'] = True

    with server.app.test_client() as client:
        yield client




def test_render_homepage(client):
    """/ should render the homepage."""

    response = client.get("/")

    assert b"Welcome to the bored application!" in response.data









# TODO: COMPLETE HTML TESTING

# @pytest.fixture
# def browser():
#     chromedriver = '/chromedriver-win64/chromedriver.exe'
#     driver = webdriver.Chrome(chromedriver)
#     chrome_options = Options()
#     print("PATRICK",chrome_options)
#     yield driver
#     driver.close()


# def test_home_page_has_title(browser):
#     browser.get('http://localhost:5000/')
#     assert "The Bored App" in browser.title

# def test_home_page_has_button(browser):
#     browser.get('http://localhost:5000/')
#     button = browser.find_element(By.ID, 'home-button')
#     assert button.is_displayed()