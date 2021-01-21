# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    refresh_time_seconds = fields.Integer("Refresh Time")
    
    @api.constrains('refresh_time_seconds')
    def check_value(self):
        for record in self:
            if record.refresh_time_seconds:
                if record.refresh_time_seconds < 10:
                    raise ValidationError('Refresh time must be greater than or equal to 10')
