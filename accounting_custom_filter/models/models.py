# -*- coding: utf-8 -*-

from odoo import models, fields, api

class customAccountInvoice(models.Model):
    
    _inherit = 'account.invoice.line'
        
    #code = fields.Char('CFOP', default='CFOP')
    
    #fiscal_position = fields.Char('Fiscal Position', related='invoice_id.fiscal_position_id.name', readonly=True) 
    
    #####
    
    code = fields.Char('CFOP', compute='_compute_group_by_vars', store=True)
    
    fiscal_position = fields.Char('Fiscal Position', compute='_compute_group_by_vars', store=True) 
    
    @api.one
    def _compute_group_by_vars(self):
        print ("##### _compute_group_by_vars [START] #####")
        
        self.code = self.cfop_id.code
        
        self.fiscal_position = self.invoice_id.fiscal_position_id.name
        
        print ("##### _compute_group_by_vars [END] #####")


    """
    #@api.model
    @api.depends('code')
    def test(self):
        print ("##### depends [START] #####")
        
        print ("##### depends [END] #####")
        
    @api.onchange('code')
    def test(self):
        print ("##### onchange [START] #####")
        
        print ("##### onchange [END] #####")
    """