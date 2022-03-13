# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, api, _
from odoo.exceptions import UserError, AccessError, ValidationError, AccessDenied


class PortalDashboard(models.Model):
    _name = 'portal.dashboard'
    _inherit = ['mail.thread']
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='Partner', track_visibility='onchange', required=True)
    url = fields.Char('URL', index=True, required=True)
    active = fields.Boolean('Active', default=True)

    @api.model
    def create(self, vals):
        request = super(PortalDashboard, self).create(vals)
        partner_dash = request.partner_id
        # adicionar seguidor al documento
        create_follower = self.env['mail.followers']
        if partner_dash:
            try:
                obj_follower = self.env['mail.followers'].search([('partner_id', '=', partner_dash.id), ('res_id', '=', request.id)])
                if not obj_follower:
                    create_follower.create({
                        'res_model': 'portal.dashboard',
                        'partner_id': partner_dash.id,
                        'res_id': request.id,
                    })
            except:
                raise UserError(_('No ha sido posible asociar un seguidor al documento de firma.'))
        return request
