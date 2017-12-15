# -*- coding: utf-8 -*-
    
    #Documentation
    #This 'model' adds new fields to 'product.template'.
    #'product.template' is the main Product model.

from odoo import models, fields

class RoyaltiesReport(models.Model):
    
    #Class inheritance
    
    _inherit = 'sale.report'