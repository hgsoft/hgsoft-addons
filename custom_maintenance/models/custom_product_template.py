# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ConfinmentProductTemplate(models.Model):
    _inherit = 'product.template'
    
    type = fields.Selection(selection_add=[('equipment', 'Equipment')], tracking=True)