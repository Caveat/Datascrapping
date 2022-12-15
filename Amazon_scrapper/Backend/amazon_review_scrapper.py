import util
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from amazonsqllite import store_db
from sql_connection import get_sql_connection
from amazondao import insert_new_products, insert_reviews
from amazon_All_review_scrapper import scrape_all_reviews
from amazon_local_review_scrapper import scrape_local_reviews

next_page = ''
connections = get_sql_connection()


def scrape_amazon(keyword, max_pages):
    page_number = 1
    path = "C:/Users/Ansh/Desktop/Akshay/Python/Pycharm/Pycharm projects/chromedriver"
    url = "https://www.amazon.in/"
    browser = util.Chrome(executable_path=path)
    browser.implicitly_wait(7.5)
    browser.get(url)
    # Enter keyword
    product = keyword
    element_search_id = browser.find_element(by=By.ID, value="twotabsearchtextbox")
    element_search_id.clear()
    element_search_id.send_keys(product)
    element_search_id.send_keys(Keys.ENTER)
    browser.implicitly_wait(5)
    while page_number <= max_pages:
        scrape_page(browser)
        page_number += 1
        browser.get(next_page)
        browser.implicitly_wait(5)
    connections.close()
    browser.quit()


def scrape_page(browser):
    product_link = []
    items = util.WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    currenturl = browser.current_url
    for item in items:
        # find link
        link = item.find_element(By.XPATH, value='.//span[@class="rush-component"]/a').get_attribute("href")
        product_link.append(link)
    for link in product_link:
        reviews_text = scrape_local_reviews(link, browser)
        browser.get(currenturl)
        browser.implicitly_wait(5)
        print(reviews_text)
        insert_reviews(connections, reviews_text)
    global next_page
    next_page = browser.find_element(by=By.XPATH,
                                     value='//span[@class ="s-pagination-item s-pagination-selected"]/following-sibling::a').get_attribute(
        "href")


scrape_amazon("Monitor", 2)
