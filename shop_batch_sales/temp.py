import re

print(" ##### CONTROLLER OVERRIDE #####")

product_id = "aa56, 57"

try:
    x = int(product_id)
    
except Exception:
    product_id = re.sub('[^0-9,]','', product_id).split(",")
    
print(product_id)


product_id: product.product(56, 57, 58, 59, 60, 61)|123456
