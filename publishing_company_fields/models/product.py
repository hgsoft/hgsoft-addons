# -*- coding: utf-8 -*-
    
    #Documentation
    #This 'model' adds new fields to 'product.template'.
    #'product.template' is the main Product model.

from odoo import models, fields, api

class ProductFields(models.Model):
    
    #Class inheritance
    
    _inherit = 'product.template'

    #New fields with 'True' filter.
    #These fields come from the 'res.partner' model.
    
    author = fields.Many2one('res.partner', string="Author",
        domain=[('is_author', '=', True)])
    
    publisher = fields.Many2one('res.partner', string="Publisher",
        domain=[('is_publisher', '=', True)])
    
    royalties_percentage = fields.Float(digits=(6,2), default=0.0)
    
    #@api.one
    @api.onchange('author')
    def _onchange_royalties_percentage(self):
        #self.env['res.partner'].royalties_percentage = self.royalties_percentage
        #self.royalties_percentage = self.env['res.partner'].royalties_percentage
        self.royalties_percentage = self.author.royalties_percentage
        
        #return {
        #    'warning': {
        #        'title': "Something bad happened",
        #        'message': "It was very bad indeed",
        #    }
        #}