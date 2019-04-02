# -*- coding: utf-8 -*-

from odoo import models, fields, api


class customAccountPayment(models.Model):
    _inherit = 'account.payment'            
    
    @api.model
    def default_get(self, fields):
        rec = super(customAccountPayment, self).default_get(fields)
        invoice_defaults = self.resolve_2many_commands('invoice_ids', rec.get('invoice_ids'))
        #
        #print(rec)
        #print(invoice_defaults)
        #
        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]
            rec['communication'] = invoice['origin'] or invoice['reference'] or invoice['name'] or invoice['number']                                
        return rec
