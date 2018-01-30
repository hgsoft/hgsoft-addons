# -*- coding: utf-8 -*-

from odoo import models, fields, api

class customAccountInvoice(models.Model):
    
    _inherit = 'account.invoice'
#     _name = 'accounting_custom_filter.accounting_custom_filter'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100