from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def scrape_all_reviews(url, browser):
    browser.get(url)
    browser.implicitly_wait(7.5)
    prod_asign = browser.find_element(By.ID, value="title_feature_div").get_attribute("data-csa-c-asin")
    prod_name = browser.find_element(By.ID, value="productTitle")
    rating = 0
    star_str=""
    try:
        ratings = browser.find_element(By.ID, value="averageCustomerReviews")
        rating = ratings.find_element(By.XPATH, value='.//span[@id="acrCustomerReviewText"]').text
        star = ratings.find_element(By.XPATH,
                                    value='.//span[@class = "reviewCountTextLinkedHistogram noUnderline"]').get_attribute(
            "title")
        star_str = star[0:3]
    except NoSuchElementException:
        rating = 0
        star_str = ''
        pass
    whole_price = browser.find_elements(By.XPATH, value='.//span[@class="a-price-whole"]')
    if whole_price:
        price = whole_price[0].text
    else:
        price = 0
    review_list = browser.find_elements(By.XPATH, value='.//div[contains(@class,"review aok-relative")]')
    review_date = []
    review_text = []
    review = {}
    for review in review_list:
        date = ''
        rev_text = ''
        date = review.find_element(By.XPATH, value='.//span[contains(@class,"review-date")]')
        review_date.append(date.text)
        try:
            rev_text = review.find_element(By.XPATH,
                                           value='.//div[contains(@class,"reviewText review-text-content")]/span')
            review_text.append(rev_text.text)

        except NoSuchElementException:
            review_text.append("No text review")
            pass
    review = {
        "product_asign": prod_asign,
        "product_name": prod_name.text,
        "product_rating": star_str,
        "product_rating_num": rating,
        "Price": price,
        "review_date": review_date,
        "reviews_text": review_text
    }
    return review
