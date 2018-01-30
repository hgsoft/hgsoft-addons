# -*- coding: utf-8 -*-

from odoo import models, fields, api

class customAccountInvoice(models.Model):
    
    _inherit = 'account.invoice.line'
        
    #cfop_code = fields.Char('CFOP', related='cfop_id.code', readonly=True)
    
    fiscal_position = fields.Char('Fiscal Position', related='invoice_id.fiscal_position_id.name', readonly=True) 
