import sqlite3
import os
import uuid

upload_root='static/products'

conn=sqlite3.connect('seller.db')
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
        FOREIGN KEY (SELLER_ID) REFERENCES sellerinfo(id)
          
        )''')

c.execute('''
CREATE TABLE IF NOT EXISTS sellerinfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL
        
     
        )''')

conn.commit()
conn.close()


def save_product_data_db(products,image_name):
    image_name=image_name
    conn=sqlite3.connect('seller.db')
    c=conn.cursor()
    c.execute(
        """
        INSERT INTO productsinfo (description, category,gender,price,image_path) 
        VALUES (?,?,?,?,?)
        """,
        (products["description"],
         products["category"],
         products["gender"],
         products["price"],
         image_name
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
     conn=sqlite3.connect('seller.db')
     c=conn.cursor()
     c.execute(
        """
        SELECT id FROM sellerinfo WHERE email=?
        """,
        (userdata["email"],)
    )
     seller=c.fetchone()
     if seller:
        return True

     return False

def insert_Seller_signup_data(userdata):
    conn=sqlite3.connect('seller.db')
    c=conn.cursor()
          
    c.execute(
            """
            INSERT INTO sellerinfo (name,email,password_hash) 
            VALUES (?,?,?)"""
            ,
            (userdata["name"],
             userdata["email"],
             userdata["password"]
             )
        )
    conn.commit()
    conn.close()
    return {"success":"Seller registered successfully"}


def seller_login_verfication(userdata):
    conn=sqlite3.connect('seller.db')
    c=conn.cursor()
    c.execute(
        """
        SELECT password_hash,email FROM sellerinfo WHERE email=?
        """,
        (userdata["email"],)
    )
    seller=c.fetchone()
    if seller:
        return True
    return False