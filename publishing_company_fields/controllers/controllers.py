# -*- coding: utf-8 -*-
from odoo import http

# class PublishingCompanyFields(http.Controller):
#     @http.route('/publishing_company_fields/publishing_company_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/publishing_company_fields/publishing_company_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('publishing_company_fields.listing', {
#             'root': '/publishing_company_fields/publishing_company_fields',
#             'objects': http.request.env['publishing_company_fields.publishing_company_fields'].search([]),
#         })

#     @http.route('/publishing_company_fields/publishing_company_fields/objects/<model("publishing_company_fields.publishing_company_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('publishing_company_fields.object', {
#             'object': obj
#         })