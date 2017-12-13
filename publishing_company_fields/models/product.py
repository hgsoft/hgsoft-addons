# -*- coding: utf-8 -*-
    
    #Documentation
    #This 'model' adds new fields to 'product.template'.
    #'product.template' is the main Product model.

from odoo import models, fields

class ProductFields(models.Model):
    
    #Class inheritance
    
    _inherit = 'product.template'

    #New fields with 'True' filter.
    #These fields come from the 'res.partner' model.
    
    author = fields.Many2one('res.partner', string="author",
        domain=[('is_author', '=', True)])
    
    publisher = fields.Many2one('res.partner', string="publisher",
        domain=[('is_publisher', '=', True)])
