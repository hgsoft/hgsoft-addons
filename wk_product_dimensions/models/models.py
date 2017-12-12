# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from odoo import models, fields, api, _
ComputeVolume = [
    ('manual','Manual'),
    ('auto','Auto'),
]

class Product(models.Model):
    _inherit = 'product.template'
    # compute_volume = fields.Selection(
    #     selection = ComputeVolume,
    #     string='Compute Volume ',
    #     default='manual'
    # )

    length = fields.Char(
        string='Length',
    )
    width = fields.Char(
        string='Width',
    )
    height = fields.Char(
        string='Height',
    )
    dimensions_uom_id = fields.Many2one(
        'product.uom', 
        'Unit of Measure', 
        help="Default Unit of Measure used for dimension."
    )
