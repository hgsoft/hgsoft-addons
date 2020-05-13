from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import models

class ProductConfigWebsiteSale(WebsiteSale):
    @http.route('/website_product_configurator/onchange',
                type='json', methods=['POST'], auth="public", website=True)
    def onchange(self, form_values, field_name, **post):
        """Capture onchange events in the website and forward data to backend
        onchange method"""
        # config session and product template
        product_configurator_obj = request.env['product.configurator']
        product_template_id = self.get_config_product_template(form_values)
        try:
            config_session_id = self.get_config_session(
                product_tmpl_id=product_template_id)
        except Exception as Ex:
            return {'error': Ex}

        # prepare dictionary in formate needed to pass in onchage
        form_values = self.get_orm_form_vals(
            form_values, config_session_id)
        config_vals = self._prepare_configurator_values(
            form_values, config_session_id)

        # call onchange
        specs = product_configurator_obj._onchange_spec()
        updates = {}
        try:
            updates = product_configurator_obj.sudo().onchange(
                config_vals, field_name, specs)
            updates['value'] = self.remove_recursive_list(updates['value'])
        except Exception as Ex:
            return {'error': Ex}

        # get open step lines according to current configuation
        
        ###
        
        # -> OLD
        #value_ids = updates['value'].get('value_ids')
        
        # -> NEW
        value_ids = [updates['value'].get(field_name)]
        
        ###
        
        if not value_ids:
            value_ids = self.get_current_configuration(
                form_values, config_session_id)
        try:
            open_cfg_step_line_ids = config_session_id.sudo()\
                .get_open_step_lines(value_ids).ids
        except Exception as Ex:
            return {'error': Ex}

        # if no step is defined or some attribute remains to add in a step
        open_cfg_step_line_ids = [
            '%s' % (step_id)
            for step_id in open_cfg_step_line_ids
        ]
        extra_attr_line_ids = self.get_extra_attribute_line_ids(
            product_template_id)
        if extra_attr_line_ids:
            open_cfg_step_line_ids.append('configure')

        # configuration images
        config_image_ids = config_session_id._get_config_image(
            value_ids=value_ids)
        if not config_image_ids:
            config_image_ids = product_template_id

        image_vals = self.get_image_vals(
            image_line_ids=config_image_ids,
            model_name=config_image_ids[:1]._name
        )
        pricelist = request.website.get_current_pricelist()
        updates['open_cfg_step_line_ids'] = open_cfg_step_line_ids
        updates['config_image_vals'] = image_vals
        decimal_prec_obj = request.env['decimal.precision']
        updates['decimal_precision'] = {
            'weight': decimal_prec_obj.precision_get('Stock Weight') or 2,
            'price': pricelist.currency_id.decimal_places or 2,
        }        
        return updates
