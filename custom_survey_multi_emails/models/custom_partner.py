# -*- coding: utf-8 -*-
from odoo import fields, models

class CustomPartner(models.Model):
    _inherit = 'res.partner'
    
    send_survey = fields.Boolean("Send survey by email?", default=True)