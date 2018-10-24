# -*- coding: utf-8 -*-

from odoo import models, fields, api

class customAccountMove(models.Model):
    
    _inherit = 'account.move.line'
    
    #ail = fields.Many2one('account.invoice.line', string="Account Invoice Line")

    #numberNF = fields.Char(related='ail.numberNF',store=True)
    
    #numberNF = fields.Char('Number NF', compute='_compute_fiscal_fields', store=True)
    
    #participant_nick = fields.Char(string='Nick name', related='partner_id.name')
    numberNF = fields.Char(string='Account Invoice', related='invoice_id.name')
    
    #ail_id = fields.Many2one('account.invoice.line', string='Account Invoice Line', default=lambda self: self.env.user.company_id )
    #company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env['res.company'].search([]))

    #numberNF = fields.Char(related='ail_id.numberNF', store=True)

    #order_line = fields.One2many('consignment.order.line','order_id','Order Lines')
    
    #company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id )

    #sicil_no = fields.Char(related='company_id.company_sicilno',store=True)
    
    @api.one
    def _compute_fiscal_fields(self):
        #print ("##### _compute_fiscal_fields [START] #####")
        
        eletronic_invoice = self.env['invoice.eletronic'].search([('invoice_id','=', self.invoice_id.id)])
        
        if eletronic_invoice.numero == 0:
            self.numberNF = "S/NF"
        else:
            self.numberNF = eletronic_invoice.numero
        
        #print ("##### _compute_fiscal_fields [END] #####")