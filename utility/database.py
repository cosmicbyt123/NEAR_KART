import sqlite3
import os
import uuid

upload_root='static/products'

conn=sqlite3.connect('seller.db')
conn.execute("PRAGMA foreign_keys = ON;")
c=conn.cursor()

c.execute('''
CREATE TABLE  IF NOT EXISTS productsinfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        gender TEXT NOT NULL,
        price REAL NOT NULL,
        image_path TEXT NOT NULL,
        seller_id INTEGER,
        FOREIGN KEY (seller_id) REFERENCES customerinfo(id)
          
        )''')

c.execute('''
CREATE TABLE IF NOT EXISTS customerinfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
        
     
        )''')

conn.commit()
conn.close()

def get_db():
    conn = sqlite3.connect("seller.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def save_product_data_db(products,image_name):
    image_name=image_name
    conn=get_db()
    c=conn.cursor()

    c.execute(
        """
        INSERT INTO productsinfo (description, category,gender,price,image_path,seller_id) 
        VALUES (?,?,?,?,?,?)
        """,
        (products["description"],
         products["category"],
         products["gender"],
         products["price"],
         image_name,
         products["seller_id"]
         )
    )
    
    conn.commit()
    conn.close()
    

def save_product_image(products):
    
    image=products.get("image")
    ext=image.filename.rsplit('.',1)[1].lower()
    folder_path=os.path.join(upload_root, products["category"])
    if not os.path.exists(folder_path):
         
         os.makedirs(folder_path)
    
    safename=uuid.uuid4().hex + '.' + ext
    image.filename=safename
    image_path=os.path.join(folder_path, image.filename)
    image.save(image_path) 

    return image_path

def check_email_exists(userdata):
     conn=get_db()
     c=conn.cursor()
     c.execute(
        """
        SELECT id FROM customerinfo WHERE email=?
        """,
        (userdata["email"],)
    )
     seller=c.fetchone()
     if seller:
        return True

     return False

def Seller_signup(userdata):
    conn=get_db()
    c=conn.cursor()

          
    c.execute(
            """
            INSERT INTO customerinfo (name,email,password_hash,role) 
            VALUES (?,?,?,?)"""
            ,
            (userdata["username"],
             userdata["email"],
             userdata["password"],
             userdata["role"]
             )
        )
    conn.commit()
    conn.close()
    return {"success":"Seller registered successfully"}


def seller_login(userdata):
    conn=get_db()
    c=conn.cursor()

    c.execute(
        """
        SELECT password_hash,id,role FROM customerinfo WHERE email=?
        """,
        (userdata["email"],)
    )
    seller=c.fetchone()
    if seller:
        return seller
    return False

def coustomer_login(userdata):
    conn=get_db()
    c=conn.cursor()
    c.execute(
        """
        SELECT id,password_hash,email,role FROM customerinfo WHERE email=?
        """,
        (userdata["email"],)
    )
    customer=c.fetchone()
    if customer:
        return customer
    return False

def customer_signup(userdata):
    conn=get_db()
    c=conn.cursor()
          
    c.execute(
            """
            INSERT INTO customerinfo (name,email,password_hash,role) 
            VALUES (?,?,?,?)"""
            ,
            (userdata["username"],
             userdata["email"],
             userdata["password"],
             userdata["role"]
             )
        )
    conn.commit()
    conn.close()
    return {"success":"Customer registered successfully"}


def get_all_products():
    conn=get_db()
    c=conn.cursor()

    c.execute(
        """
        SELECT * FROM productsinfo
        """
    )
    products=c.fetchall()
    conn.close()
    return products


def delete_record_from_db(product):
    conn=get_db()
    c=conn.cursor()

    c.execute(
        """
        DELETE FROM productsinfo WHERE image_path=?
        """,
        (product,)
    )
    conn.commit()
    conn.close()



def get_seller_products(seller_id):
    conn=get_db()
    c=conn.cursor()
    conn.row_factory = sqlite3.Row

    c.execute(
        """
        SELECT image_path,price FROM productsinfo WHERE seller_id=?
        """,
        (seller_id,)
    )
    products=c.fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = sqlite3.connect("seller.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute(
        "SELECT * FROM productsinfo WHERE id = ?",
        (product_id,)
    )
    product = c.fetchone()
    conn.close()
    return product
