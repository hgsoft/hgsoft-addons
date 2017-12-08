# -*- coding: utf-8 -*-
from odoo import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    
    #instructor = fields.Boolean("Is an Author?", default=False)
    author = fields.Boolean("Is an Author?", default=False)
    publisher = fields.Boolean("Is a Publisher?", default=False)
    
    session_ids = fields.Many2many('openacademy.session',
        string="Attended Sessions", readonly=True)
