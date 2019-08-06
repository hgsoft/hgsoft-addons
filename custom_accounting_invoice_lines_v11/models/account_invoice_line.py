# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo import api, fields, models, _


class customAccountInvoice(models.Model):
    
    _inherit = 'account.invoice.line'
        
    date_invoice = fields.Date(string='Date Invoice', related='invoice_id.date_invoice', store=True)
    
    cfop_code = fields.Char(string='CFOP', related='cfop_id.code', store=True)
        
    fiscal_position = fields.Char(string='Fiscal Position', related='invoice_id.fiscal_position_id.name', store=True)
    
    number_nf = fields.Integer(string='Number NF', related='invoice_id.invoice_eletronic_ids.numero', store=True)
    
    model_nf = fields.Selection(string='Model NF', related='invoice_id.invoice_eletronic_ids.model', store=True)
