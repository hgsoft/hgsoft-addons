# -*- coding: utf-8 -*-

from odoo import models, fields, api


class customInvoiceEletronic(models.Model):
    _inherit = 'invoice.eletronic'
    
    cfop_code = fields.Char('cfop_code')    

    @api.multi
    def create(self, vals):    
        invoice_eletronic_list = self.env['invoice.eletronic'].search([('cfop_code','=', None)])
        
        for invoice_eletronic in invoice_eletronic_list:
            icms_rules_update = invoice_eletronic.fiscal_position_id.icms_tax_rule_ids
            vals_update = {}
            if len(icms_rules_update) > 1:
                rules_cfop_update = []
                for rule_update in icms_rules_update:
                    rules_cfop_update.append(rule_update.cfop_id.code)
                vals_update['cfop_code'] = str(rules_cfop_update).replace('[', '').replace(']', '').replace('\'', '')
            else:
                vals_update['cfop_code'] = icms_rules_update.cfop_id.code
                                    
            super(customInvoiceEletronic, invoice_eletronic).write(vals_update)
            
        fiscal_position = self.env['account.fiscal.position'].search([('id','=', vals['fiscal_position_id'])])                
                
        icms_rules = fiscal_position.icms_tax_rule_ids
        
        if len(icms_rules) > 1:
            rules_cfop = []
            for rule in icms_rules:
                rules_cfop.append(rule.cfop_id.code)
            vals['cfop_code'] = str(rules_cfop).replace('[', '').replace(']', '').replace('\'', '')
        else:
            vals['cfop_code'] = icms_rules.cfop_id.code
                                
        new_invoice_eletronic = super(customInvoiceEletronic, self).create(vals)                
        
        return new_invoice_eletronic