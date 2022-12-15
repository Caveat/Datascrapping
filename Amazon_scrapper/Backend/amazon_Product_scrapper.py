import util
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from amazonsqllite import store_db
from sql_connection import get_sql_connection
from amazondao import insert_new_products

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
        print(page_number)
        page_number += 1
        browser.get(next_page)
        browser.implicitly_wait(5)

    connections.close()
    browser.quit()


def scrape_page(browser):
    product_name = []
    product_asin = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []

    items = util.WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))

    for item in items:
        link = ''
        name = ''
        ratings_box = []
        name = item.find_element(by=By.XPATH, value='//span[@class="a-size-medium a-color-base a-text-normal"]')
        product_name.append(name.text)
        data_asin = item.get_attribute("data-asin")
        product_asin.append(data_asin)
        ratings_box = item.find_elements(By.XPATH, value='.//div[@class ="a-row a-size-small"]/span')
        if ratings_box:
            ratings = ratings_box[0].get_attribute('aria-label')
            ratings_num = ratings_box[1].get_attribute('aria-label')
        else:
            ratings, ratings_num = 0, 0
        product_ratings.append(ratings)
        product_ratings_num.append(str(ratings_num))

        # find price
        whole_price = item.find_elements(By.XPATH, value='.//span[@class="a-price-whole"]')
        if whole_price:
            price = whole_price[0].text
        else:
            price = 0
        product_price.append(price)

        # find link
        link = item.find_element(By.XPATH, value='.//span[@class="rush-component"]/a').get_attribute("href")
        product_link.append(link)
        product_dic = {
            "product_name": name.text,
            "product_asin": data_asin,
            "product_ratings": ratings,
            "product_ratings_num": ratings_num,
            "product_link": link,
            "product_price": price
        }
        # mysql database
        insert_new_products(connections, product_dic)
    print(product_name)
    print(product_asin)
    print(product_ratings)
    print(product_ratings_num)
    print(product_link)
    print(product_price)

    # Sqlite database
    store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)
    global next_page
    next_page = browser.find_element(by=By.XPATH,
                                     value='//span[@class ="s-pagination-item s-pagination-selected"]/following-sibling::a').get_attribute(
        "href")
    print(next_page)


scrape_amazon("Monitor", 4)
