# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class product_template(models.Model):
    _inherit = 'product.template'

    @api.one
    @api.constrains('ean13')
    def _check_seats_limit(self):
        all_eans = self.search_read([('id','!=', self.id)],['ean13'])
        if self.ean13 and self.ean13 in [each['ean13'] for each in all_eans]:
            raise Warning(_('You have already used this EAN before.'))

    ean13 = fields.Char('EAN13 Barcode', type='char')
    author_id = fields.Many2one('res.partner', 'Author', domain=[('is_author','=',True)])
    pages = fields.Integer('Pages')

    