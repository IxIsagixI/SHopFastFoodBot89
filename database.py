import sqlite3


def create_user_tables():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    telegram_id BIGINT NOT NULL UNIQUE,
    phone TEXT
    );
    ''')

#create_user_tables()


def create_cart_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carts(
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(user_id),
    total_price DECIMAL(12, 2) DEFAULT 0,
    total_products INTEGER DEFAULT 0
    );
    """)

#create_cart_table()



def create_cart_products_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart_products(
    cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    final_price DECIMAL(12, 2) NOT NULL,
    cart_id INTEGER REFERENCES carts(cart_id),
    UNIQUE(product_name, cart_id)
    );
    """)

#create_cart_products_table()

def create_categories_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE
    );
    """)

create_categories_table()

def insert_categories():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO categories(category_name) VALUES
    ('Лаваш'),
    ('Донар'),
    ('Бургеры'),
    ('Хот-Доги'),
    ('Напитки'),
    ('Соусы')
    ''')
    database.commit()
    database.close()

#insert_categories()

def create_products_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name VARCHAR(30) NOT NULL UNIQUE,
        price DECIMAL(12, 2) NOT NULL,        
        description VARCHAR(200),
        image TEXT,
        category_id INTEGER NOT NULL,
        
        FOREIGN KEY(category_id) REFERENCES categories(category_id)       
        );
        ''')

#create_products_table()


def insert_products_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO products(category_id, product_name, price, description, image) VALUES
    (1, 'Лаваш говяжий', 28000, 'Мясо, огурцы, чипсы, помидорки', 'media/lavash1.jpg'),
    (1, 'Лаваш куриный', 25000, 'Куриное мясо, огурцы, сыр, салат, майонез', 'media/lavash2.jpg'),
    (1, 'Лаваш овощной', 22000, 'Овощи, сыр, зелень, соус', 'media/lavash3.jpg'),
    (2, 'Донар с курицей', 30000, 'Куриное мясо, овощи, соус', 'media/donar1.jpg'),
    (2, 'Донар с говядиной', 32000, 'Говяжье мясо, овощи, соус', 'media/donar2.jpg'),
    (2, 'Донар с овощями', 35000, 'Свинина, овощи, соус', 'media/donar3.jpg'),
    (3, 'Классический бургер', 35000, 'Говяжье мясо, сыр, овощи, булочка, соус', 'media/burger1.jpeg'),
    (3, 'Чикенбургер', 30000, 'Куриное мясо, сыр, овощи, булочка, соус', 'media/burger2.png'),
    (3, 'Вегетарианский бургер', 28000, 'Овощи, сыр, булочка, соус', 'media/burger3.jpg'),
    (4, 'Классический хот-дог', 15000, 'Сосиска, булочка, горчица, кетчуп, лук, капуста', 'media/hotdog1.jpg'),
    (4, 'Хот-дог с сыром', 17000, 'Сосиска, булочка, сыр, горчица, кетчуп, лук, капуста', 'media/hotdog2.jpg'),
    (4, 'Хот-дог с овощами', 16000, 'Сосиска, булочка, овощи, горчица, кетчуп, лук, помидорки, капуста', 'media/hotdog3.png'),
    (5, 'Кола', 5000, 'Классическая газировка', 'media/cola.jpg'),
    (5, 'Фанта', 5000, 'Апельсиновая газировка', 'media/fanta.jpg'),
    (5, 'Сок', 7000, 'Фруктовый сок', 'media/juice.jpg'),
    (6, 'Кетчуп', 3000, 'Томатный соус', 'media/ketchup.jpg'),
    (6, 'Майонез', 3000, 'Маслянистый соус', 'media/mayonez.png'),
    (6, 'Горчица', 2000, 'Острый соус', 'media/gorchitsa.jpg')
    ''')
    database.commit()
    database.close()
#insert_products_table()

def first_select_user(chat_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE telegram_id = ?
    ''',(chat_id,))
    user = cursor.fetchone()
    database.close()
    return user

def first_register_user(chat_id,full_name):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name) VALUES(?,?)
    ''',(chat_id,full_name))
    database.commit()
    database.close()

def update_user_to_finish_register(chat_id,phone):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
        UPDATE users
        SET phone = ?
        WHERE telegram_id = ?
    ''',(chat_id,phone))
    database.commit()
    database.close()

def insert_to_cart(chat_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO carts(user_id) VALUES
    (
    (SELECT user_id FROM users WHERE telegram_id = ?)
    );
    ''',(chat_id,))
    database.commit()
    database.close()

def get_all_categories():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT * FROM categories;
        ''')
    categories = cursor.fetchall()
    database.close()
    return categories

def get_products_by_category_id(category_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_id, product_name FROM products
    WHERE category_id = ?
    ''',(category_id,))
    products = cursor.fetchall()
    database.close()
    return products

def get_product_detail(product_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT * FROM products
        WHERE product_id = ?
        ''', (product_id,))
    product = cursor.fetchone()
    database.close()
    return product

def get_user_cart_id(chat_id):
    try:
        database = sqlite3.connect('fastfood.db')
        cursor = database.cursor()
        cursor.execute('''
        SELECT cart_id FROM carts
        WHERE user_id = (
            SELECT user_id FROM users WHERE telegram_id = ?
        )
        ''', (chat_id,))
        result = cursor.fetchone()
        cart_id = result[0] if result is not None else None
        return cart_id
    except sqlite3.Error as e:
        print("Ошибка при доступе к базе данных:", e)
        return None
    finally:
        if database:
            database.close()

def get_quantity(cart_id, product):
    try:
        database = sqlite3.connect('fastfood.db')
        cursor = database.cursor()
        cursor.execute('''
           SELECT quantity FROM cart_products
           WHERE cart_id = ? and product_name = ?
           ''', (cart_id, product))
        quantity = cursor.fetchone()[0]
        return quantity
    except sqlite3.Error as e:
        print("Ошибка при доступе к базе данных:", e)
        return None
    finally:
        if database:
            database.close()

def insert_or_update_cart_product(cart_id, product_name, quantity, final_price):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    try:
        cursor.execute('''
            INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
            VALUES(?, ?, ?, ?)      
        ''',(cart_id, product_name, quantity, final_price))
        database.commit()
        return True
    except:
        cursor.execute('''
        UPDATE cart_products
        SET quantity = ?,
        final_price = ?
        WHERE product_name = ? AND cart_id = ?
        ''',(quantity, final_price, product_name, cart_id))
        database.commit()
        return False
    finally:
        database.close()



def update_product_total_price(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE carts
    SET total_products = (
    SELECT SEM(quantity) FROM cart_products
    WHERE cart_id = :cart_id
    ),
    total_price = (
    SELECT SEM(final_price) FROM cart_products
    WHERE cart_id = :cart_id
    )
    WHERE cart_id = :cart_id
    ''', {'cart_id': cart_id})
    database.commit()
    database.close()


def get_total_products_price(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT total_products, total_price FROM carts WHERE cart_id = ?
    ''', (cart_id, ))
    total_products, total_price = cursor.fetchone()
    database.close()
    return total_products, total_price


def get_cart_products_for_delete(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_product_id, product_name FROM
    cart_products
    Where cart_id = ?
    ''',(cart_id,))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products

def delete_Cart_product_from(cart_product_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products WHERE cart_product_id = ?
    ''',(cart_product_id,))
    database.commit()
    database.close()

def drop_cart_products_default(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products WHERE cart_id = ?
    ''',(cart_id,))
    database.commit()
    database.close()

def orders_total_price():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_total_price(
    orders_total_price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER REFERENCES carts(cart_id),
    total_price DECIMAL(12,2) DEFAULT 0,
    total_products INTEGER DEFAULT 0,
    time_now TEXT,
    new_date TEXT
    );
    ''')

def order():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    orders_total_price_id INTEGER REFERENCES orders_total_price(orders_total_price_id),
    product_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    final_price DECIMAL(12, 2) NOT NULL
    );
    ''')


# order()
# orders_total_price()


def save_order_total(cart_id,total_products,total_price,time_now,new_date):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO orders_total_price(cart_id,total_products,total_price,time_now,new_date)
    VALUES(?,?,?,?,?)
    ''',(cart_id,total_products,total_price,time_now,new_date))
    database.commit()
    database.close()

def orders_total_price_id(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT order_total_price_id FROM order_total_price
    WHERE cart_id = ?
    ''',(cart_id,))
    order_total_id = cursor.fetchall()[-1][0]
    database.close()
    return order_total_id


def save_order(order_total_id,product_name,quantity,total_price):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO orders(order_total_id,product_name,quantity,total_price)
    VALUES(?,?,?,?)
    ''',(order_total_id,product_name,quantity,total_price))
    database.commit()
    database.close()



def get_orders_total_price(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM orders_total_price
    WHERE cart_id = ?
    ''',(cart_id,))
    orders_total_price = cursor.fetchall()
    database.close()
    return orders_total_price

def get_detail_product(id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name, quantity, final_price FROM orders
    WHERE orders_total_price = ?
    ''', (id,))
    detail_product = cursor.fetchall()
    database.close()
    return detail_product








