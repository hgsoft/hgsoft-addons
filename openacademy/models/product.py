# -*- coding: utf-8 -*-
from odoo import models, fields

class Product(models.Model):
    _inherit = 'product.template'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    
    #instructor = fields.Boolean("Is an Author?", default=False)
    author_id = fields.Many2one('res.partner', string="author_id",
        domain=[('author', '=', True)])
    
    publisher_id = fields.Many2one('res.partner', string="publisher_id",
        domain=[('publisher', '=', True)])
    
    
    #   instructor_id = fields.Many2one('res.partner', string="Instructor",
    #   domain=[('instructor', '=', True)])

    
    #session_ids = fields.Many2many('openacademy.session',
    #    string="Attended Sessions", readonly=True)
