# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ConfinmentManagement(models.Model):
    _name = "confinment.management"
    confinment_product_id = fields.Many2one('product.template', string='Confinment Product', required=True, domain="[('type', '=', 'product')]")
    
    stock_location_id = fields.Many2one('stock.location', string='Confinment Location', required=True)
    
    confinment_stage = fields.Selection([
        ('adaptation', 'Adaptation'),
        ('growth', 'Growth'),
        ('final', 'Final')
    ], string='Confinment Stage', required=True)
    
    number_of_treatments_or_wagons_per_day = fields.Integer(string='Number of treatments or wagons per day', default=0)
    
    number_of_animals = fields.Integer(string='Number of animals', default=0)
    
    kg_head_supplied_day = fields.Float(string='Kg / head supplied / day (MS)', default=0.0)
    
    confinement_days = fields.Integer(string='Confinement days', default=0)
    
    confinment_management_line = fields.One2many('confinment.management.line', 'confinment_management_id', string='Confinment Management Lines', copy=True, required=True)
    
    total_basal_diet = fields.Float(string='Total Basal Diet (Dry Matter)', default=0.0, compute='_compute_total_basal_diet')
    
    total_day_consumption = fields.Float(string='Total Day Consumption (kg MN)', default=0.0, compute='_compute_total_day_consumption')
    
    total_daily_cost = fields.Float(string='Total Daily Cost', default=0.0, compute='_compute_total_daily_cost')
    
    total_consumption = fields.Float(string='Total Consumption (total / day)', default=0.0, compute='_compute_total_consumption')
    
    total_weighing_by_tract = fields.Float(string='Total Weighing by tract', default=0, compute='_compute_total_weighing_by_tract')
    
    total_estimated_consumption_in_the_containment_period = fields.Float(string='Total Estimated consumption in the containment period', default=0.0, compute='_compute_total_estimated_consumption_period')
    
    total_cost_in_the_period = fields.Float(string='Cost in the Period', default=0.0, compute='_compute_total_cost_in_the_period')
    
    input_weight = fields.Float(string='Input Weight', default=0.0)
    
    output_weight = fields.Float(string='Output Weight', default=0.0)
    
    slaughter_weight = fields.Float(string='Slaughter Weight', default=0.0, compute='_compute_slaughter_weight')
    
    gmd = fields.Float(string='GMD', default=0.0, compute='_compute_gmd')

    carcass_yield = fields.Float(string='Carcass Yield', default=0.0)
    
    carcass_gain = fields.Float(string='Carcass gain', default=0.0, compute='_compute_carcass_gain')
    
    gain_in_at_sign = fields.Float(string='Gain in @', default=0.0, compute='_compute_gain_in_at_sign')
    
    price_at_sign_sale = fields.Float(string='Price @ Sale', default=0.0)
    
    sale_at_sign_produced_revenue = fields.Float(string='Sale @ produced revenue', default=0.0, compute='_compute_sale_at_sign_produced_revenue')
    
    total_revenue = fields.Float(string='Total revenue', default=0.0, compute='_compute_total_revenue')
    
    purchase_value_per_animal = fields.Float(string='Purchase value per animal', default=0.0)
    
    freight_charge_per_head = fields.Float(string='Freight charge per head', default=0.0)
    
    funrual = fields.Float(string='FunRual', default=0.0, compute='_compute_funrual')

    indea = fields.Float(string='INDEA', default=0.0)

    others = fields.Float(string='Medication - Vaccine - Earring, ETC', default=0.0)
    
    daily_cost_head = fields.Float(string='Daily Cost (management / treatment) / head', default=0.0)
    
    total_costs = fields.Float(string='Total Costs', default=0.0, compute='_compute_total_costs')
    
    net_profit_head = fields.Float(string='Net Profit / head', default=0.0, compute='_compute_net_profit_head')
        
    @api.depends('confinment_management_line.basal_diet')
    def _compute_total_basal_diet(self):
        total_basal_diet = 0.0
        for line in self.confinment_management_line:
            total_basal_diet += line.basal_diet
        self.total_basal_diet = total_basal_diet
    
    @api.depends('confinment_management_line.day_consumption')
    def _compute_total_day_consumption(self):
        total_day_consumption = 0.0
        for line in self.confinment_management_line:
            total_day_consumption += line.day_consumption
        self.total_day_consumption = total_day_consumption
        
    @api.depends('confinment_management_line.daily_cost')
    def _compute_total_daily_cost(self):
        total_daily_cost = 0.0
        for line in self.confinment_management_line:
            total_daily_cost += line.daily_cost
        self.total_daily_cost = total_daily_cost
        
    @api.depends('confinment_management_line.consumption')
    def _compute_total_consumption(self):
        total_consumption = 0.0
        for line in self.confinment_management_line:
            total_consumption += line.consumption
        self.total_consumption = total_consumption
        
    @api.depends('confinment_management_line.weighing_by_tract')
    def _compute_total_weighing_by_tract(self):
        total_weighing_by_tract = 0
        for line in self.confinment_management_line:
            total_weighing_by_tract += line.weighing_by_tract
        self.total_weighing_by_tract = total_weighing_by_tract
        
    @api.depends('confinment_management_line.estimated_consumption_in_the_containment_period')
    def _compute_total_estimated_consumption_period(self):
        total_estimated_consumption_in_the_containment_period = 0.0
        for line in self.confinment_management_line:
            total_estimated_consumption_in_the_containment_period += line.estimated_consumption_in_the_containment_period
        self.total_estimated_consumption_in_the_containment_period = total_estimated_consumption_in_the_containment_period
        
    @api.depends('confinement_days', 'total_daily_cost')
    def _compute_total_cost_in_the_period(self):
        self.total_cost_in_the_period = self.confinement_days * self.total_daily_cost

    @api.depends('output_weight', 'carcass_yield')
    def _compute_slaughter_weight(self):
        self.slaughter_weight = self.output_weight * self.carcass_yield / 15
        
    @api.depends('output_weight', 'input_weight', 'confinement_days')
    def _compute_gmd(self):
        if self.confinement_days > 0:
            self.gmd = ((self.output_weight - self.input_weight) / self.confinement_days)
        else:
            self.gmd = 0
        
    @api.depends('output_weight', 'carcass_yield', 'input_weight')
    def _compute_carcass_gain(self):
        self.carcass_gain = (self.output_weight * self.carcass_yield) - (self.input_weight / 2)
        
    @api.depends('carcass_gain')
    def _compute_gain_in_at_sign(self):
        self.gain_in_at_sign = self.carcass_gain / 15
        
    @api.depends('price_at_sign_sale', 'gain_in_at_sign')
    def _compute_sale_at_sign_produced_revenue(self):
        self.sale_at_sign_produced_revenue = self.price_at_sign_sale * self.gain_in_at_sign
        
    @api.depends('slaughter_weight', 'price_at_sign_sale')
    def _compute_total_revenue(self):
        self.total_revenue = self.slaughter_weight * self.price_at_sign_sale
        
    @api.depends('total_revenue')
    def _compute_funrual(self):
        self.funrual = self.total_revenue * 0.015
        
    @api.depends('daily_cost_head', 'confinement_days', 'total_cost_in_the_period', 'purchase_value_per_animal', 'freight_charge_per_head', 'funrual', 'indea', 'others')
    def _compute_total_costs(self):
        self.total_costs = (self.daily_cost_head * self.confinement_days) + self.purchase_value_per_animal + self.freight_charge_per_head + self.funrual + self.indea + self.others + self.total_cost_in_the_period
        
    @api.depends('total_revenue', 'total_costs')
    def _compute_net_profit_head(self):
        self.net_profit_head = self.total_revenue - self.total_costs


class ConfinmentManagement(models.Model):
    _name = "confinment.management.line"
    
    sequence = fields.Integer(string='Sequence', default=10)
    
    confinment_management_id = fields.Many2one('confinment.management', string='Confinment Management Reference', required=True, ondelete='cascade', index=True, copy=False)
    
    product_id = fields.Many2one('product.product', string='Product', change_default=True, ondelete='restrict', required=True, domain="[('type', '=', 'ingredient')]")
    
    product_template_id = fields.Many2one('product.template', string='Product Template', related="product_id.product_tmpl_id")
    
    basal_diet = fields.Float(string='Basal Diet (Dry Matter)', default=0.0)
    
    percent_ms = fields.Float(string='% MS', default=0.0)
    
    day_consumption = fields.Float(string='Day Consumption (kg MN)', default=0.0, compute='_compute_day_consumption')
    
    value_kg_mn = fields.Float(string='R$ / kg MN', default=0.0)
    
    daily_cost = fields.Float(string='Daily Cost', default=0.0, compute='_compute_daily_cost')
    
    consumption = fields.Float(string='Consumption (total / day)', default=0, compute='_compute_consumption')
    
    weighing_by_tract = fields.Float(string='Weighing by tract', default=0, compute='_compute_weighing_by_tract')
    
    estimated_consumption_in_the_containment_period = fields.Float(string='Estimated consumption in the containment period', default=0.0, compute='_compute_estimated_consumption_period')
    
    @api.depends('confinment_management_id.kg_head_supplied_day', 'basal_diet', 'percent_ms')
    def _compute_day_consumption(self):
        kg_head_supplied_day = self.confinment_management_id.kg_head_supplied_day
        for record in self:
            if record.percent_ms > 0:
                record.day_consumption = (kg_head_supplied_day * record.basal_diet / 100) / record.percent_ms
            else:
                record.day_consumption = 0

    @api.depends('day_consumption', 'value_kg_mn')
    def _compute_daily_cost(self):
        for record in self:
            record.daily_cost = record.day_consumption * record.value_kg_mn

    @api.depends('confinment_management_id.number_of_animals', 'day_consumption')
    def _compute_consumption(self):
        number_of_animals = self.confinment_management_id.number_of_animals
        for record in self:
            record.consumption = record.day_consumption * number_of_animals
    
    @api.depends('confinment_management_id.number_of_treatments_or_wagons_per_day', 'consumption')
    def _compute_weighing_by_tract(self):
        number_of_treatments_or_wagons_per_day = self.confinment_management_id.number_of_treatments_or_wagons_per_day
        for record in self:
            if number_of_treatments_or_wagons_per_day > 0:
                record.weighing_by_tract = record.consumption / number_of_treatments_or_wagons_per_day
            else:
                record.weighing_by_tract = 0
    
    @api.depends('confinment_management_id.confinement_days', 'consumption')
    def _compute_estimated_consumption_period(self):
        confinement_days = self.confinment_management_id.confinement_days
        for record in self:
            record.estimated_consumption_in_the_containment_period = record.consumption * confinement_days

class ConfinmentProductTemplate(models.Model):
    _inherit = 'product.template'
    
    type = fields.Selection(selection_add=[('ingredient', 'Ingredient')], tracking=True)
    
    confinment_product_ids = fields.One2many('confinment.management', 'confinment_product_id', 'Confinment Product')
    
    
    
class ConfinmentLocation(models.Model):
    _inherit = "stock.location"

    confinment_management_ids = fields.One2many('confinment.management', 'stock_location_id', 'Confinment Location')
    