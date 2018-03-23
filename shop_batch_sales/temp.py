####################################################################
import re

print(" ##### CONTROLLER OVERRIDE #####")

grid_values = "product.product(56, 57, 58, 59, 60, 61)|#1#0#3#4#5#0"

try:
    x = int(product_id)
    
except Exception:
    grid_values = grid_values.split("|");

    product_list = re.sub('[^0-9,]','', grid_values[0]).split(",")

    product_qty_list = grid_values[1].split("#");
    
    del product_qty_list[0]

print(product_list)
print(product_qty_list)

for x in range(len(product_list)):
    if int(product_qty_list[x]) > 0:
        print(product_list[x])
        print(product_qty_list[x])
        

    

###################################################################

#1 4     1 2
#2 5     3 4
#3 6     5 6