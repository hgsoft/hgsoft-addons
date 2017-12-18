# -*- coding: utf-8 -*-
    
    #Documentation
    #This 'model' adds new fields to 'product.template'.
    #'product.template' is the main Product model.

from odoo import models, fields, api

class RoyaltiesReport(models.Model):
    
    #Class inheritance
    
    _inherit = 'sale.report'
    
    _name = 'royalties.report'
    
    royalties_percentage = fields.Many2one('res.partner', string="Percentage of Royalties")
    
    royalties_to_pay = fields.Float(digits=(6,2), default=0.0, compute='_compute_royalties', store=True, readonly=True, index=True)

    #royalties_to_pay = fields.Float(store=True, readonly=True)

    #@api.multi
    #def _compute_royalties(self):
    #    for record in self:
    #        record.name = str(random.randint(1, 1e6))

    @api.depends('price_total', 'royalties_percentage')
    def _compute_royalties(self):
        self.royalties_to_pay = self.price_total * (self.royalties_percentage / 100.0)
        #for r in self:
        #    if not r.royalties_percentage:
        #        r.royalties_to_pay = 0.0
        #    else:
        #        r.royalties_to_pay = price_total * (royalties_percentage / 100.0)