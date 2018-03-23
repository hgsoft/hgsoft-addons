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
        
        print(" ##### CONTROLLER OVERRIDE #####")

        if isinstance(product_id, int):
            request.website.sale_get_order(force_create=1)._cart_update(
                product_id=int(product_id),
                add_qty=add_qty,
                set_qty=set_qty,
                attributes=self._filter_attributes(**kw),
            )
        else:
            product_ids = re.sub('[^0-9,]','', product_id).split(",")
            
            for x in product_ids:
                print(x)
                request.website.sale_get_order(force_create=1)._cart_update(
                    product_id=int(x),
                    add_qty=add_qty,
                    set_qty=set_qty,
                    attributes=self._filter_attributes(**kw),
                )
        
        
        return request.redirect("/shop/cart")

    def _filter_attributes(self, **kw):
        return {k: v for k, v in kw.items() if "attribute" in k}
