# -*- coding: utf-8 -*-
import re
from odoo import http, tools, _
from odoo.http import request
import odoo.addons.website_sale.controllers.main as WebsiteSale

class WebsiteSale(WebsiteSale.WebsiteSale):
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        
        print("##### WebsiteSale - [START] #####")
        
        print("Quantidade: " + str(add_qty))

        print("product_id: " + product_id)

        try:
            product_id = int(product_id)
            request.website.sale_get_order(force_create=1)._cart_update(
                product_id=int(product_id),
                add_qty=add_qty,
                set_qty=set_qty,
                attributes=self._filter_attributes(**kw),
            )
        except Exception:
            grid_values = product_id
            
            grid_values = grid_values.split("|");
            
            product_list = grid_values[0].split("#")
            
            del product_list[0]
            
            product_qty_list = grid_values[1].split("#");
            
            del product_qty_list[0]
            
            for x in range(len(product_list)):
                if int(product_qty_list[x]) > 0:
                    request.website.sale_get_order(force_create=1)._cart_update(
                        product_id=int(product_list[x]),
                        add_qty=int(product_qty_list[x]),
                        set_qty=set_qty,
                        attributes=self._filter_attributes(**kw),
                    )
        
        print("##### WebsiteSale - [END] #####")
        
        return request.redirect("/shop/cart")

    def _filter_attributes(self, **kw):
        return {k: v for k, v in kw.items() if "attribute" in k}