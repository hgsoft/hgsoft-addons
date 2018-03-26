####################################################################
import re

print(" ##### CONTROLLER OVERRIDE #####")

#grid_values = "product.product(56, 57, 58, 59, 60, 61, 64, 65, 66)|#1#4#7#2#5#8#3#6#9|3|3"
grid_values = "#56#60#64#67#68#69#70#71#72|#1#2#3#4#5#6#7#8#9|0|0"

try:
    x = int(product_id)
    
except Exception:
    grid_values = grid_values.split("|");

    #product_list = re.sub('[^0-9,]','', grid_values[0]).split(",")
    
    #product_list = re.sub('[^0-9,]','', grid_values[0]).split("#")

    product_list = grid_values[0].split("#")

    del product_list[0]

    product_qty_list = grid_values[1].split("#");
    
    del product_qty_list[0]
    
    #####
    print("##### NEW LOGIC #####")
    '''
    qty_col = int(grid_values[2])
    qty_row = int(grid_values[3])

    size=qty_col
    custom_list = [product_qty_list[i:i+size] for i  in range(0, len(product_qty_list), size)]
    print(custom_list)
    #print(custom_list[0][1])
    #for x in custom_list:

    final_list = []

    for y in range(0, qty_col):
        for x in custom_list:
            print(x[y])
            final_list.append(int(x[y]))
            #print(y)
            
    print(final_list)
    '''
    print("##### NEW LOGIC #####")
    #####
    
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