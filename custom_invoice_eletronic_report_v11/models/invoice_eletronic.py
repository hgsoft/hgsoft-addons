# -*- coding: utf-8 -*-

from odoo import models, fields, api


class customInvoiceEletronic(models.Model):
    _inherit = 'invoice.eletronic'
    
    cfop_code = fields.Char('cfop_code')    

    @api.multi
    def create(self, vals):    
        invoice_eletronic_list = self.env['invoice.eletronic'].search([('cfop_code','=', None)])
        if len(invoice_eletronic_list) >= 1:
            for invoice_eletronic in invoice_eletronic_list:            
                invoice_eletronic_item_list = self.env['invoice.eletronic.item'].search([('invoice_eletronic_id','=', invoice_eletronic.id)])
                invoice_eletronic.write(customInvoiceEletronic.format_cfop_list(invoice_eletronic_item_list))
        new_invoice_eletronic = super(customInvoiceEletronic, self).create(vals) 
        invoice_eletronic_item_list = self.env['invoice.eletronic.item'].search([('invoice_eletronic_id','=', new_invoice_eletronic.id)])
        new_invoice_eletronic.write(customInvoiceEletronic.format_cfop_list(invoice_eletronic_item_list))
        return new_invoice_eletronic
    
    @staticmethod
    def format_cfop_list(invoice_eletronic_item_list:list):
        item_cfop_list = []
        for invoice_eletronic_item in invoice_eletronic_item_list:
            item_cfop_list.append(invoice_eletronic_item.cfop)
        return {'cfop_code': str(sorted(set(item_cfop_list))).replace('[', '').replace(']', '').replace('\'', '')}