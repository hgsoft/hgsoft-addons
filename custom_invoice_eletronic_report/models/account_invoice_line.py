# -*- coding: utf-8 -*-

from odoo import models, fields, api


class customInvoiceEletronic(models.Model):
    _inherit = 'invoice.eletronic'
    
    cfop_code = fields.Char('cfop_code')    

    @api.multi
    def create(self, vals):
    
        print ("###########################")
        print ("###### create [START] #####")
        print ("###########################")
        
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
        
        print ("###########################")
        print ("####### create [END] ######")    
        print ("###########################")
        
        return new_invoice_eletronic