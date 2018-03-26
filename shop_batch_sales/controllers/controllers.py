# -*- coding: utf-8 -*-
import json
import logging
from werkzeug.exceptions import Forbidden
import re
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.base.ir.ir_qweb.fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import ValidationError
from odoo.addons.website_form.controllers.main import WebsiteForm
import odoo.addons.website_sale.controllers.main as WebsiteSale

class WebsiteSale(WebsiteSale.WebsiteSale):
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        
        print("##### WebsiteSale - [START] #####")
        
        print("Quantidade: " + str(add_qty))

        print("product_id: " + product_id)

        #product_id = int(product_id)

        if isinstance(product_id, int):
            request.website.sale_get_order(force_create=1)._cart_update(
                product_id=int(product_id),
                add_qty=add_qty,
                set_qty=set_qty,
                attributes=self._filter_attributes(**kw),
            )
        else:
            grid_values = product_id
            
            grid_values = grid_values.split("|");
            
            #product_list = re.sub('[^0-9,]','', grid_values[0]).split(",")
            
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
            
            for x in range(len(product_list)):
                if int(product_qty_list[x]) > 0:
                    request.website.sale_get_order(force_create=1)._cart_update(
                        product_id=int(product_list[x]),
                        add_qty=int(product_qty_list[x]),
                        #add_qty=int(final_list[x]) or int(product_qty_list[x]),
                        set_qty=set_qty,
                        attributes=self._filter_attributes(**kw),
                    )
                
            '''
            for x in product_list:
                print(x)
                request.website.sale_get_order(force_create=1)._cart_update(
                    product_id=int(x),
                    add_qty=add_qty,
                    set_qty=set_qty,
                    attributes=self._filter_attributes(**kw),
                )
            '''
        
        print("##### WebsiteSale - [END] #####")
        
        return request.redirect("/shop/cart")

    def _filter_attributes(self, **kw):
        return {k: v for k, v in kw.items() if "attribute" in k}
