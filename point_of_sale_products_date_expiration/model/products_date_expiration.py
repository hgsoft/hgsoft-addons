# -*- coding: utf-8 -*-
from odoo import fields, models, api

import pytz
from datetime import datetime, timedelta

class ProductDateExpiration(models.Model):
	_inherit = 'product.product'

	@api.onchange('type')
	def _def_state_type_product(self):
		if self.type =="product":
			self.state_type_product = True
		else:
			self.state_type_product = False

	@api.onchange('date')
	def _available(self):
		lima = pytz.timezone("America/Lima")
		ahora = datetime.now()
		horas_diferencia = lima.localize(ahora).utcoffset().total_seconds()/60/60
		fecha_actual_peru = ahora + timedelta(hours=horas_diferencia)
		date_now = fecha_actual_peru.strftime('%Y-%m-%d')
		#date_now = fecha_actual_peru.strftime('%Y-%m-%d %H:%M:%S')
		if self.date <= date_now:
			self.available_in_pos = False
		else:
			self.available_in_pos = True

	date = fields.Date(string="Expiration Date")
	state_type_product = fields.Boolean(string="state")



