# -*- coding: utf-8 -*-
from odoo import fields, models

class CustomUser(models.Model):
    _inherit = 'res.users'
    
    send_survey = fields.Boolean("Send survey by email?", default=True)