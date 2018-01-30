# -*- coding: utf-8 -*-
from odoo import http

# class AccountingCustomFilter(http.Controller):
#     @http.route('/accounting_custom_filter/accounting_custom_filter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/accounting_custom_filter/accounting_custom_filter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('accounting_custom_filter.listing', {
#             'root': '/accounting_custom_filter/accounting_custom_filter',
#             'objects': http.request.env['accounting_custom_filter.accounting_custom_filter'].search([]),
#         })

#     @http.route('/accounting_custom_filter/accounting_custom_filter/objects/<model("accounting_custom_filter.accounting_custom_filter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('accounting_custom_filter.object', {
#             'object': obj
#         })