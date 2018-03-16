# -*- coding: utf-8 -*-

from odoo import models, fields, api

class customInvoiceEletronic(models.Model):
    _inherit = 'invoice.eletronic'
    
    @api.multi
    def create(self, vals):
        print ("##### create [START] #####")
        
        new_invoice_eletronic = super(customInvoiceEletronic, self).create(vals)
        
        ail = self.env['account.invoice.line'].search([('invoice_id','=', new_invoice_eletronic.invoice_id.id)])
        
        ail._update_values()
        
        aml = self.env['account.move.line'].search([('invoice_id','=', new_invoice_eletronic.invoice_id.id)])
        
        aml._update_values()
        
        print ("##### create [END] #####")
        
        return new_invoice_eletronic

class customAccountInvoice(models.Model):
    
    _inherit = 'account.invoice.line'
        
    code = fields.Char('CFOP')
    
    fiscal_position = fields.Char('Fiscal Position')
    
    numberNF = fields.Char('Number NF')
    
    modelNF = fields.Char('Model NF')
    
    on_install = fields.Char('On Install', compute='_compute_inicial_fields', store=True)
    
    @api.one
    def _compute_inicial_fields(self):
        print ("##### _compute_inicial_fields [START] #####")
        
        self._update_values()
        
        self.on_install = 'done'
        
        print ("##### _compute_inicial_fields [END] #####")
    
    @api.multi
    def create(self, vals):
        print ("##### create [START] #####")
        
        new_ail = super(customAccountInvoice, self).create(vals)
        
        new_ail._update_dict(vals)
                
        new_ail._update_values()

        super(customAccountInvoice, new_ail).write(vals)
        
        print ("##### create [END] #####")
        
        return new_ail
    
    @api.one
    def _update_dict(self, vals):
        print ("##### _update_dict [START] #####")
        
        eletronic_invoice = self.env['invoice.eletronic'].search([('invoice_id','=', self.invoice_id.id)])
        
        if eletronic_invoice.numero == 0 or eletronic_invoice.numero == '0':
            vals['numberNF'] = "S/NF"
        else:
            vals['numberNF'] = eletronic_invoice.numero
            vals['modelNF'] = eletronic_invoice.model
        
        invoice = self.env['account.invoice'].search([('id','=', self.invoice_id.id)])
        
        vals['fiscal_position'] = invoice.fiscal_position_id.name
        
        cfop = self.env['br_account.cfop'].search([('id','=', self.cfop_id.id)])
        
        vals['code'] = cfop.code
               
        print ("##### _update_dict [END] #####")
    
    @api.one
    def _update_values(self):
        print ("##### _update_values [START] #####")
               
        ail = self.env['account.invoice.line'].search([('id','!=', False)])
        
        for line in ail:
            vals = {};
            
            line._update_dict(vals)
            
            super(customAccountInvoice, line).write(vals)
               
        print ("##### _update_values [END] #####")
    
class customAccountMove(models.Model):
    
    _inherit = 'account.move.line'
    
    numberNF = fields.Char('Number NF')
    
    on_install = fields.Char('On Install', compute='_compute_inicial_fields', store=True)
    
    @api.one
    def _compute_inicial_fields(self):
        print ("##### _compute_inicial_fields [START] #####")
        
        self._update_values()
        
        self.on_install = 'done'
        
        print ("##### _compute_inicial_fields [END] #####")
    
    @api.multi
    def create(self, vals):
        print ("##### create [START] #####")
        
        new_aml = super(customAccountMove, self).create(vals)
        
        new_aml._update_dict(vals)
        
        new_aml._update_values()
                
        super(customAccountMove, new_aml).write(vals)
        
        print ("##### create [END] #####")
        
        return new_aml
    
    @api.one
    def _update_dict(self, vals):
        print ("##### _update_dict [START] #####")
               
        eletronic_invoice = self.env['invoice.eletronic'].search([('invoice_id','=', self.invoice_id.id)])
        
        if eletronic_invoice.numero == 0 or eletronic_invoice.numero == '0':
            vals['numberNF'] = "S/NF"
        else:
            vals['numberNF'] = eletronic_invoice.numero
        
        print ("##### _update_dict [END] #####")
    
    @api.one
    def _update_values(self):
        print ("##### _update_values [START] #####")
               
        aml = self.env['account.move.line'].search([('id','!=', self.id)])
        
        for line in aml:
            vals = {};
            
            line._update_dict(vals)
            
            super(customAccountMove, line).write(vals)
               
        print ("##### _update_values [END] #####")