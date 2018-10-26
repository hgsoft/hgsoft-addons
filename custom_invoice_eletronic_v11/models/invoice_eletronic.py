# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging


class customInvoiceEletronic(models.Model):
    _inherit = 'invoice.eletronic'
    
    cfop_code = fields.Char('cfop_code')    

    @api.multi
    def create(self, vals):    
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
    
    @api.model
    def process_no_cfop_code(self):        
        _logger = logging.getLogger(__name__)
        msg = 'Starting the module installation.'
        _logger.info(msg)
        invoice_eletronic_list = self.env['invoice.eletronic'].search([('cfop_code','=', None)])
        if len(invoice_eletronic_list) >= 1:
            msg = 'Processing {} documents without cfop_code...'
            _logger.info(msg.format(len(invoice_eletronic_list)))
            for invoice_eletronic in invoice_eletronic_list:            
                invoice_eletronic_item_list = self.env['invoice.eletronic.item'].search([('invoice_eletronic_id','=', invoice_eletronic.id)])
                invoice_eletronic.write(customInvoiceEletronic.format_cfop_list(invoice_eletronic_item_list))
            msg = 'All documents were processed.'
            _logger.info(msg)
