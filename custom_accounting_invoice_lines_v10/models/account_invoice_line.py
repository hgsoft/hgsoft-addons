# -*- coding: utf-8 -*-

from odoo import models, fields, api

class customInvoiceEletronic(models.Model):
    _inherit = 'invoice.eletronic'
    
    @api.multi
    def create(self, vals):
        #print ("##### create [START] #####")
        
        new_invoice_eletronic = super(customInvoiceEletronic, self).create(vals)
        
        ail = self.env['account.invoice.line'].search([('invoice_id','=', new_invoice_eletronic.invoice_id.id)])
        
        ail._update_values()
        
        aml = self.env['account.move.line'].search([('invoice_id','=', new_invoice_eletronic.invoice_id.id)])
        
        aml._update_values()
        
        #print ("##### create [END] #####")
        
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
        #print ("##### _compute_inicial_fields [AI START] #####")
        
        ail = self.env['account.invoice.line'].search([('id','!=', False)])
        
        update = True
        
        for line in ail:
            #print(line.on_install)
            if line.on_install == 'done':
                update = False
        
        if update:
            #print('##########################')
            #print('### ## ## UPDATE ## ## ###')
            #print('##########################')
            self._update_values()
        
        self.on_install = 'done'
        
        #print ("##### _compute_inicial_fields [AI END] #####")
    
    @api.multi
    def create(self, vals):
        #print ("##### create [AI START] #####")
        
        new_ail = super(customAccountInvoice, self).create(vals)
        
        new_ail._update_dict(vals)
                
        new_ail._update_values()

        super(customAccountInvoice, new_ail).write(vals)
        
        #print ("##### create [AI END] #####")
        
        return new_ail
    
    @api.one
    def _update_dict(self, vals):
        #print ("##### _update_dict [AI START] #####")
        
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
               
        #print ("##### _update_dict [AI END] #####")
    
    @api.one
    def _update_values(self):
        #print ("##### _update_values [AI START] #####")
               
        ail = self.env['account.invoice.line'].search([('id','!=', False)])
        
        #print(len(ail))
        
        for line in ail:
            
            vals = {};
            
            line._update_dict(vals)
            
            super(customAccountInvoice, line).write(vals)
               
        #print ("##### _update_values [AI END] #####")
    
class customAccountMove(models.Model):
    
    _inherit = 'account.move.line'
    
    numberNF = fields.Char('Number NF')
    
    on_install = fields.Char('On Install', compute='_compute_inicial_fields', store=True)
    
    @api.one
    def _compute_inicial_fields(self):
        #print ("##### _compute_inicial_fields [AM START] #####")
        
        aml = self.env['account.move.line'].search([('id','!=', False)])
        
        update = True
        
        for line in aml:
            #print(line.on_install)
            if line.on_install == 'done':
                update = False
        
        if update:
            #print('##########################')
            #print('### ## ## UPDATE ## ## ###')
            #print('##########################')
            self._update_values()
        
        self.on_install = 'done'
        
        #print ("##### _compute_inicial_fields [AM END] #####")
    
    @api.multi
    def create(self, vals):
        #print ("##### create [AM START] #####")
        
        new_aml = super(customAccountMove, self).create(vals)
        
        new_aml._update_dict(vals)
        
        new_aml._update_values()
                
        super(customAccountMove, new_aml).write(vals)
        
        #print ("##### create [AM END] #####")
        
        return new_aml
    
    @api.one
    def _update_dict(self, vals):
        #print ("##### _update_dict [AM START] #####")
               
        eletronic_invoice = self.env['invoice.eletronic'].search([('invoice_id','=', self.invoice_id.id)])
        
        if eletronic_invoice.numero == 0 or eletronic_invoice.numero == '0':
            vals['numberNF'] = "S/NF"
        else:
            vals['numberNF'] = eletronic_invoice.numero
        
        #print ("##### _update_dict [AM END] #####")
    
    @api.one
    def _update_values(self):
        #print ("##### _update_values [AM START] #####")
               
        aml = self.env['account.move.line'].search([('id','!=', self.id)])
        
        #print(len(aml))
        
        for line in aml:
            vals = {};
            
            line._update_dict(vals)
            
            super(customAccountMove, line).write(vals)
               
        #print ("##### _update_values [AM END] #####")

'''
class customAccountMoveB(models.Model):
    
    _inherit = 'account.move'

    @api.multi
    def assert_balanced(self):
        print ("##### assert_balanced [START] #####")
        
        if not self.ids:
            return True
        prec = self.env['decimal.precision'].precision_get('Account')

        self._cr.execute("""\
            SELECT      move_id
            FROM        account_move_line
            WHERE       move_id in %s
            GROUP BY    move_id
            HAVING      abs(sum(debit) - sum(credit)) > %s
            """, (tuple(self.ids), 10 ** (-max(5, prec))))
        if len(self._cr.fetchall()) != 0:
            raise UserError(_("Cannot create unbalanced journal entry."))
        return True
'''