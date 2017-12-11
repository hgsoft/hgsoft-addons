# -*- coding: utf-8 -*-
from odoo import fields, models

class Product(models.Model):
    _inherit = 'product.product'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    
    #instructor = fields.Boolean("Is an Author?", default=False)
    author_id = fields.Many2one('res.partner', string="author_id")
    publisher_id = fields.Many2one('res.partner', string="publisher_id")
    
    session_ids = fields.Many2many('openacademy.session',
        string="Attended Sessions", readonly=True)
