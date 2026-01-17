from flask import Flask, jsonify,render_template,request,redirect,url_for,Blueprint,current_app,session
import os
from utility import services ,database,manage
import logging
from functools import wraps

def seller_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('role') != 'seller':
            return redirect(url_for('products.seller_login'))
        return fn(*args, **kwargs)
    return wrapper

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('role') != 'customer':
            return redirect(url_for('products.customer_login'))
        return fn(*args, **kwargs)
    return wrapper

products_bp=Blueprint('products',__name__)

@products_bp.route('/cart',methods=['GET'])
def cart():
    return render_template('cart.html')

@products_bp.route('/',methods=['GET'])
@login_required
def home():

    try:
        products=database.get_all_products()
        print(products)
        print("the data on products 0 is ")
        print(products[0][5])
        manage.check_image_exsist(products[0][5])

    except Exception as e:
        print("Error occurred while fetching products:", e)

    return render_template('home.html',products=products)
 
@products_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    product = database.get_product_by_id(product_id)
    print("product detail:",product)
    return render_template("product_detail.html", product=product)

@products_bp.route('/seller_dashboard',methods=['GET'])
@seller_required
def seller_dashboard():
    try:
        seller_id=session.get('id')
        print(seller_id)
        products=database.get_seller_products(seller_id)
        print("seller products",products)
    
    except Exception as e:
        print("Error occurred while fetching seller products:", e)

    return render_template('seller_dash_board.html', products=products)



@products_bp.route('/customer_login',methods=['GET'])
def customer_login():
    return render_template('customer_login.html')

@products_bp.route('/customer_signup',methods=['GET'])
def customer_signup():
    return render_template('customer_signup.html')



@products_bp.route('/seller_login',methods=['GET'])
def seller_login():
    return render_template('seller_login.html')

@products_bp.route('/seller_signup',methods=['GET'])
def seller_signup():
    return render_template('seller_signup.html')


@products_bp.route('/api/auth/seller/signup',methods=['POST'])
def seller_signup_api():

    sellerdata={
        "username":request.form.get('username'),
        "email":request.form.get('email'),
        "password":request.form.get('passwordhash'),
        "role":'seller'
    }
    try:
        result=services.validate_data(sellerdata)
        print("validation completed")
        email_exsists=database.check_email_exists(sellerdata)
        if email_exsists:
            return {"message":"Email already exists"}
        save_status=database.Seller_signup(sellerdata)
        print("signup successful",save_status)
        return redirect(url_for('products.seller_dashboard'))
    except Exception as e:
        print("this the exception occured during signup:",e)
        return {"message":"there is an error occured during signup "+str(e)}


@products_bp.route('/api/auth/seller/login',methods=['POST'])
def seller_login_api():
   
    userdata={
        "username":request.form.get('username'),
        "email":request.form.get('email'),
        "password":request.form.get('passwordhash'),
        "role":'seller'
        }
    

    try:
        
        save_status=services.validate_data(userdata)
    
        if save_status:
            verifed_data=database.seller_login(userdata)
            print("verifed_data",verifed_data)
            if verifed_data:
                print("login successful")
                if userdata["password"]== verifed_data[0]:
                    session["id"]=verifed_data[1]
                    session["role"]=verifed_data[2]
                    print("login successful")
                    return redirect(url_for('products.seller_dashboard'))

                else:
                    print("invalid credentials")
                    return redirect(url_for('products.seller_login'))
            
            else:
                print("error occured during login")
                return redirect(url_for('products.seller_login'))

    except Exception as e:
        print("there is an error occured during in login page:",e)
        return{"message":"there is an error occured during login "+str(e)}

    


@products_bp.route('/api/products',methods=['POST'])
def products_data():
    products={
        "image":request.files.get('image'),
        "description":request.form.get('description'),
        "category":request.form.get('cato'),
        "gender":request.form.get('gender'),
        "price":request.form.get('price'),
        "seller_id":session.get("id")
    }
    error=services.validate_product_data(products)
    if error:
        print("error found",error)
        print("VALIDATION ERROR:", error, type(error))

        return render_template("seller_dash_board.html", error=error, old=products)
       
    try:
        image_path=database.save_product_image(products)
        print(image_path)
        image_path = image_path.replace("\\", "/")   # Windows fix
        database.save_product_data_db(products,image_path)
    
    except Exception as e:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        raise

    return redirect(url_for('products.seller_dashboard'))

@products_bp.route("/me")
def me():
    return dict(session)


@products_bp.route('/api/auth/customer/login',methods=['POST'])
def customer_login_api():

   
    userdata={
        "username":request.form.get('username'),
        "email":request.form.get('email'),
        "password":request.form.get('passwordhash'),
        "role":'customer'
        }
    
    try:
        validate_data=services.validate_data(userdata)
        
        if validate_data:
            login_status=database.coustomer_login(userdata)
            print("login_status",login_status)
            print(login_status[1])
            if login_status:
                if userdata["password"]== login_status[1]:
                    session["user_id"]=login_status[0]
                    session["role"]=login_status[3]
                    print("login successfull")
                    return redirect(url_for('products.home'))

                else:
                    return redirect(url_for('products.customer_login'))

            else:
                print("error occured during login")
                return redirect(url_for('products.customer_login'))


    except Exception as e:
        return {"message":str(e)}
    


@products_bp.route('/api/auth/customer/signup',methods=['POST'])
def customer_signup_api():

   
    userdata={
        "username":request.form.get('username'),
        "email":request.form.get('email'),
        "password":request.form.get('passwordhash'),
        "role":'customer'
        }
    
    try:
        checkexists=database.check_email_exists(userdata)
        if checkexists:
            return {"message":"Email already exists"}
        validate_data=services.validate_data(userdata)
        if validate_data:
            signup_status=database.customer_signup(userdata)
            if signup_status:
                print("customer login successful")
                return redirect(url_for('products.home'))
            else:
                print("invalid credentials")
                return redirect(url_for('products.customer_signup'))

        
        

    except Exception as e:
        print(e)
        return {"message":str(e)}
    raise

@products_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('products.customer_login'))

