# -*- coding: utf-8 -*-
from odoo import fields, models

class CustomSurvey(models.Model):
    _inherit = 'survey.survey'
    
    auth_required = fields.Boolean('Login required', help="Users with a public link will be requested to login before taking part to the survey",
        oldname="authenticate", default=True)
    
    users_can_go_back = fields.Boolean('Users can go back', help="If checked, users can go back to previous pages.", default=True)