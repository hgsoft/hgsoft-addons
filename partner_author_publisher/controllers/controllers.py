# -*- coding: utf-8 -*-
from odoo import http

# class PartnerAuthorPublisher(http.Controller):
#     @http.route('/partner_author_publisher/partner_author_publisher/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner_author_publisher/partner_author_publisher/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner_author_publisher.listing', {
#             'root': '/partner_author_publisher/partner_author_publisher',
#             'objects': http.request.env['partner_author_publisher.partner_author_publisher'].search([]),
#         })

#     @http.route('/partner_author_publisher/partner_author_publisher/objects/<model("partner_author_publisher.partner_author_publisher"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner_author_publisher.object', {
#             'object': obj
#         })