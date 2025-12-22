from flask import Flask, jsonify,render_template,request,redirect,url_for,Blueprint,current_app
import os
from utility import services ,database
import logging

products_bp=Blueprint('products',__name__)
logging.basicConfig(filename="app.log", level=logging.INFO)

@products_bp.route('/',methods=['GET'])
def seller_dashboard():
    
    return render_template('seller_dash_board.html')
   



@products_bp.route('/login',methods=['GET'])
def login_info():
    return render_template('seller_login.html')

@products_bp.route('/signup',methods=['GET'])
def signup_info():
    return render_template('seller_signup.html')


@products_bp.route('/api/auth/signup',methods=['POST'])
def signup_api():

    sellerdata={
        "username":request.form.get('username'),
        "email":request.form.get('email'),
        "password":request.form.get('passwordhash')
    }
    try:
        result=services.validate_seller_data(sellerdata)
        current_app.logger.exception(result)
        print("validation completed")
        email_exsists=database.check_email_exists(sellerdata)
        if email_exsists:
            current_app.logger.exception("Email already exists")
            return {"message":"Email already exists"}
        save_status=database.insert_Seller_signup_data(sellerdata)
        current_app.logger.exception(save_status)
        print("signup successful",save_status)
        return {"message":"signup successful"}
    except Exception as e:
        current_app.logger.exception(e)
        print("this the exception occured during signup:",e)
        return {"message":"there is an error occured during signup "+str(e)}


@products_bp.route('/api/auth/login',methods=['POST'])
def login_api():
   
    userdata={
        "username":request.form.get('username'),
        "email":request.form.get('email'),
        "password":request.form.get('passwordhash')}
    

    try:
        
        save_status=services.validate_seller_data(userdata)
    
        if save_status:
            verifed_data=database.seller_login_verfication(userdata)
            print("verifed_data",verifed_data)
            if verifed_data:
                print("login successful")
                return {"message":"login successful"}
                
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
        "price":request.form.get('price')
    }
    error=services.validate_product_data(products)
    if error:
        print("error found",error)
        print("VALIDATION ERROR:", error, type(error))

        return render_template("seller_dash_board.html", error=error, old=products)
       
    try:
        image_path=database.save_product_image(products)
        database.save_product_data_db(products,image_path)
    
    except Exception as e:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        raise

    return redirect(url_for('products.seller_dashboard'))


    


