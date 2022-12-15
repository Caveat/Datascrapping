def insert_new_products(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO products_table"
             "( product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)"
             "VALUES (%s, %s, %s,%s, %s, %s)")
    data = (product['product_asin'], product['product_name'], product['product_price'], product['product_ratings'],
            product['product_ratings_num'], product['product_link'])
    cursor.execute(query, data)
    connection.commit()
    print(cursor.lastrowid)


def insert_reviews(connection, review):
    cursor = connection.cursor()
    query = ("INSERT INTO review_table"
             "( product_asin, product_name,product_price,product_rating, product_ratings_num,product_review)"
             "VALUES (%s, %s, %s,%s, %s, %s)")
    data = (review['product_asin'], review['product_name'], review['product_price'], review['product_rating'],
            review['product_rating_num'], str(review['product_review']))
    cursor.execute(query, data)
    connection.commit()
    print(cursor.lastrowid)
