import os 
from utility import database
def check_image_exsist(prodcut):
    image_path=prodcut
    if   os.path.exists(image_path):
        print("image exsists")
        return True
    else:
        print("image does not exist")
        database.delete_record_from_db(image_path)
        return False
    

    