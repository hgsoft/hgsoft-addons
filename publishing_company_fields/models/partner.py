# -*- coding: utf-8 -*-
    
    #Documentation
    #This 'model' adds new fields to 'res.partner'.
    #'res.partner' is the main Partner model.

from odoo import fields, models, api

class PartnerFields(models.Model):
    
    #Class inheritance
    
    _inherit = 'res.partner'

    #New fields
    
    is_author = fields.Boolean("Is an Author", default=False)
    
    is_publisher = fields.Boolean("Is a Publisher", default=False)
    
    royalties_to_pay = fields.Float(digits=(6,2), store=True, compute='_royalties_to_pay')
    
    royalties_percentage = fields.Float(digits=(6,2))
    
    royalties_report = fields.Many2one('royalties.report', string='Royalties Report')
    
    @api.one
    #@api.onchange('royalties_percentage')
    @api.constrains('royalties_percentage')
    def _royalties_to_pay(self):
        #self.royalties_to_pay = self.env['royalties.report']._compute_royalties(self)
        #self.royalties_report._compute_royalties()
        self.royalties_to_pay = self.royalties_report.price_total
        print('---------------------------------')
        print(self.royalties_report.price_total)
        print('---------------------------------')