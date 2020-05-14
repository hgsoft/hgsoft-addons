# -*- coding: utf-8 -*-

from odoo import models, fields, api

class customProductConfigSession(models.Model):
    _inherit = 'product.config.session'

    @api.model
    def get_variant_vals(self, value_ids=None, custom_vals=None, **kwargs):
        """ Hook to alter the values of the product variant before creation

            :param value_ids: list of product.attribute.values ids
            :param custom_vals: dict {product.attribute.id: custom_value}

            :returns: dictionary of values to pass to product.create() method
         """
        self.ensure_one()

        if value_ids is None:
            value_ids = self.value_ids.ids

        if custom_vals is None:
            custom_vals = self._get_custom_vals_dict()

        ###
        
        # -> OLD
        #image = self.get_config_image(value_ids)
        
        # -> NEW
        image = self.product_tmpl_id.image
        
        ###
        
        vals = {
            'product_tmpl_id': self.product_tmpl_id.id,
            'attribute_value_ids': [(6, 0, value_ids)],
            'taxes_id': [(6, 0, self.product_tmpl_id.taxes_id.ids)],
            'image': image,
        }

        if custom_vals:
            vals.update({
                'value_custom_ids': self.encode_custom_values(custom_vals)
            })
        return vals