import os
import uuid
upload_root='static/products'



def validate_product_data(products):
    image=products.get("image")

    
    if len(products["category"])>10:
        return {
            "field": "category",
            "message": "Category is required"
            }
       
    
    if len(products["description"])>100:
        return "Description length should be less than 100 characters",400
    
    try:
        products["price"]=float(products["price"])

    except(TypeError, ValueError):
        return "Price should be a number",400
 
    if products["price"]<0:
        return "price must be greater then 0",400
    
    if products["price"]>1000000:
        return "price is unrealisticly high ",400
    
    if not image:
        return "Image is required",400
    
    allowed_extensions={'png','jpg','jpeg','gif'}

    if '.' not in image.filename:
        return "Invalid image file",400
    
    ext=image.filename.rsplit('.',1)[1].lower()

    if ext not in allowed_extensions:
        return "Unsupported image format",400
    
    if not image.mimetype.startswith('image/'):
        return "File is not an image",400
    
    image.seek(0,os.SEEK_END)
    image_size=image.tell()
    image.seek(0)

    if image_size>5*1024*1024:
        return "Image size exceeds 5MB limit",400
    
    
def validate_seller_data(sellerdata):

    if len(sellerdata["username"])<3:
        return {"error":"Name must be at least 3 characters long"},400
    
   
    
    if '@' not in sellerdata["email"] or '.' not in sellerdata["email"]:
        return {"error":"Invalid email address"},400
    
    if len(sellerdata["password"])<6:
        return {"error":"Password must be at least 6 characters long"},400
    
    return True







    
    

    


   
    
  

    