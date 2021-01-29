# -*- coding: utf-8 -*-
from odoo import http

# class ShopBatchSales(http.Controller):
#     @http.route('/shop_batch_sales/shop_batch_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shop_batch_sales/shop_batch_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('shop_batch_sales.listing', {
#             'root': '/shop_batch_sales/shop_batch_sales',
#             'objects': http.request.env['shop_batch_sales.shop_batch_sales'].search([]),
#         })

#     @http.route('/shop_batch_sales/shop_batch_sales/objects/<model("shop_batch_sales.shop_batch_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shop_batch_sales.object', {
#             'object': obj
#         })