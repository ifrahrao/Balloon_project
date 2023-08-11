import mysql.connector
from datetime import datetime

connection = mysql.connector.connect(host='localhost',
                                     database='balloons_world',
                                     user='root',
                                     password='ifrah123')
cursor = connection.cursor()


def insert_brands(brands_list):
    for brand in brands_list:

        cursor.execute('SELECT brand_name FROM brands WHERE brand_name = %s',
                       (brand,))
        brand_name = cursor.fetchone()
        if not brand_name and not brand=="":
            sql_insert_blob_query = """ INSERT INTO brands
                                      (brand_name) VALUES (%s)"""
            # Convert data into tuple format
            insert_brand = (brand,)
            result = cursor.execute(sql_insert_blob_query, insert_brand)
            connection.commit()

def insert_colors(colors_list):
    for color in colors_list:

        cursor.execute('SELECT name FROM colors WHERE name = %s',
                       (color,))
        color_name = cursor.fetchone()
        if not color_name and not color=="":
            sql_insert_blob_query = """ INSERT INTO colors
                                      (name) VALUES (%s)"""
            # Convert data into tuple format
            insert_color = (color,)
            result = cursor.execute(sql_insert_blob_query, insert_color)
            connection.commit()

def insert_categories(categories):
    for category in categories:
        cursor.execute('SELECT name FROM categories WHERE name = %s',
                       (category["name"],))
        category_name = cursor.fetchone()
        if not category_name and not category["name"] == None:
            sql_insert_blob_query = """ INSERT INTO categories
                                                  (name,slug,description) VALUES (%s,%s,%s)"""
            # Convert data into tuple format
            insert_color = (category["name"],category["slug"],category["description"])
            result = cursor.execute(sql_insert_blob_query, insert_color)
            connection.commit()
def get_all_colors():
    cursor.execute('SELECT name FROM colors')
    colors = cursor.fetchall()
    return colors

def get_all_brands():
    cursor.execute('SELECT brand_name FROM brands')
    brands = cursor.fetchall()
    return brands

def get_all_categories():
    cursor.execute('SELECT name,slug,description FROM categories')
    categories = cursor.fetchall()
    return categories

def get_color_id(name):
    cursor.execute('SELECT id FROM colors WHERE name = %s',
                   (name,))
    color_id = cursor.fetchone()
    if color_id:
        return color_id[0]
    else:
        return None

def get_brand_id(name):
    cursor.execute('SELECT id FROM brands WHERE brand_name = %s',
                   (name,))
    brand_id = cursor.fetchone()
    if brand_id:
        return brand_id[0]
    else:
        return None


def get_category_id(name):
    cursor.execute('SELECT id FROM categories WHERE name = %s',
                   (name,))
    category_id = cursor.fetchone()
    if category_id:
        return category_id[0]
    else:
        return None

def get_product_id(name,category_id):
    cursor.execute('SELECT id FROM products WHERE name = %s and category_id',
                   (name,category_id))
    product_id = cursor.fetchone()
    if product_id:
        return product_id[0]
    else:
        return None

def insert_product(name,category_id,original_price,image,purchase_link,color,brand):
    cursor.execute('SELECT name FROM products WHERE name = %s and category_id=%s',
                   (name,category_id,))
    product_name= cursor.fetchone()
    if not product_name and not name == "" and "balloon" in name.lower() and (color != None or brand != None):
        sql_insert_blob_query = """ INSERT INTO products(name,category_id,original_price,image,purchase_link,color,brand) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        # Convert data into tuple format
        insert_product = (name,category_id,original_price,image,purchase_link,color,brand)
        result = cursor.execute(sql_insert_blob_query, insert_product)
        connection.commit()
    elif product_name and "balloon" in name.lower() and (color != None or brand != None):
        update_blob_query =""" Update products set `original_price`=%s,`image`=%s,`purchase_link`=%s,`color`=%s,`brand`=%s,`updated_at`=%s"""
        update_product = ( original_price, image, purchase_link, color, brand,datetime.now())
        result = cursor.execute(update_blob_query, update_product)
        connection.commit()

def insert_product_categories(product_id,category_id):
    cursor.execute('SELECT id FROM products WHERE product_id = %s and category_id=%s',
                   (product_id, category_id,))
    product_category = cursor.fetchone()
    if not product_category:
        sql_insert_blob_query = """ INSERT INTO product_categories(product_id,category_id) VALUES (%s,%s)"""
        # Convert data into tuple format
        insert_product = (product_id, category_id)
        result = cursor.execute(sql_insert_blob_query, insert_product)
        connection.commit()

def insert_balloons_products(products,category):
    color_list=get_all_colors()
    brands_list=get_all_brands()
    category_list=get_all_categories()
    for product in products:


        if not [col for col in color_list if product['color'] in col[0]]:
            insert_colors([product['color']])

        if not [brand for brand in brands_list if product['brand'] in brand[0]]:
            insert_brands([product['brand']])

        matching = [cat for cat in category_list if category["name"] in cat[0]]
        if not matching:
            insert_categories([category])

        color_id=get_color_id(product["color"])
        brand_id=get_brand_id(product["brand"])
        category_id=get_category_id(category["name"])
        insert_product(product["title"],category_id,product["price"],product["image_link"],product["purchase_link"],color_id,brand_id)
        product_id=get_product_id(product["title"],category_id)
        insert_product_categories(product_id,category_id)

color="Blue"
brand=None
print(color != None or brand != None)
# brands_list=["Betallatex", "Decomex", "Gemar", "Kalisan", "Qualatex", "Tuftex","Anagram","Balloonia"]
# insert_brands(brands_list)
# insert_balloons_products([
#   {
#     "title": "5\"E Blue Balloon Pastel (100 count)",
#     "price": "Login Required",
#     "purchase_link": "https://havinaparty.com/5e-blue-mist-100-count/",
#     "image_link": "https://cdn11.bigcommerce.com/s-63aliku04p/images/stencil/350x350/products/44683/27689/Blue_Mist_Ellies_Brand__98160.1643316721.1280.1280__73118.1643316785.1280.1280__04070.1669741715.jpg?c=2",
#     "color": "Blue",
#     "brand": ""
#   }],{'name':"havina party",
#       'slug':"havina_party",
#       'description':"This is havina party balloons"})