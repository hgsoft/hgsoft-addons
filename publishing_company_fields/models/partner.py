# -*- coding: utf-8 -*-
    
    #Documentation
    #This 'model' adds new fields to 'res.partner'.
    #'res.partner' is the main Partner model.

from odoo import fields, models

class PartnerFields(models.Model):
    
    #Class inheritance
    
    _inherit = 'res.partner'

    #New fields
    
    is_author = fields.Boolean("Is an Author", default=False)
    
    is_publisher = fields.Boolean("Is a Publisher", default=False)
    
    royalties_to_pay = fields.Float(digits=(6,2), default=0.0)
    
    royalties_percentage = fields.Float(digits=(6,2), default=0.0)