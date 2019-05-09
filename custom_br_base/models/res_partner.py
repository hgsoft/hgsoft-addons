# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re
import base64
import logging

from odoo import models, fields, api, _
from odoo.addons.br_base.tools import fiscal
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from pytrustnfe.nfe import consulta_cadastro
    from pytrustnfe.certificado import Certificado
except ImportError:
    _logger.debug('Cannot import pytrustnfe')

class CustomResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def action_check_sefaz(self):
        if self.cnpj_cpf and self.state_id:
            if self.state_id.code == 'AL':
                raise UserError(_(u'Alagoas doesn\'t have this service'))
            if self.state_id.code == 'RJ':
                raise UserError(_(
                    u'Rio de Janeiro doesn\'t have this service'))
            company = self.env.user.company_id
            if not company.nfe_a1_file and not company.nfe_a1_password:
                raise UserError(_(
                    u'Configure the company\'s certificate and password'))
            cert = company.with_context({'bin_size': False}).nfe_a1_file
            cert_pfx = base64.decodestring(cert)
            certificado = Certificado(cert_pfx, company.nfe_a1_password)
            cnpj = re.sub('[^0-9]', '', self.cnpj_cpf)
            obj = {'cnpj': cnpj, 'estado': self.state_id.code}
            resposta = consulta_cadastro(certificado, obj=obj, ambiente=1,
                                         estado=self.state_id.ibge_code)

            info = resposta['object'].getchildren()[0]

            if 'infCons' not in info.__dict__:                
                msg = u'{} não possui consulta de cadastro'.format(self.state_id.name)
                raise UserError(_(msg))
            
            info = info.infCons
            if info.cStat == 111 or info.cStat == 112:
                if not self.inscr_est:
                    self.inscr_est = info.infCad.IE.text
                if not self.cnpj_cpf:
                    self.cnpj_cpf = info.infCad.CNPJ.text

                def get_value(obj, prop):
                    if prop not in dir(obj):
                        return None
                    return getattr(obj, prop)
                self.legal_name = get_value(info.infCad, 'xNome')
                if "ender" not in dir(info.infCad):
                    return
                cep = get_value(info.infCad.ender, 'CEP') or ''
                self.zip = str(cep).zfill(8) if cep else ''
                self.street = get_value(info.infCad.ender, 'xLgr')
                self.number = get_value(info.infCad.ender, 'nro')
                self.street2 = get_value(info.infCad.ender, 'xCpl')
                self.district = get_value(info.infCad.ender, 'xBairro')
                cMun = get_value(info.infCad.ender, 'cMun')
                xMun = get_value(info.infCad.ender, 'xMun')
                city = None
                if cMun:
                    city = self.env['res.state.city'].search(
                        [('ibge_code', '=', str(cMun)[2:]),
                         ('state_id', '=', self.state_id.id)])
                if not city and xMun:
                    city = self.env['res.state.city'].search(
                        [('name', 'ilike', xMun),
                         ('state_id', '=', self.state_id.id)])
                if city:
                    self.city_id = city.id
            else:
                msg = "%s - %s" % (info.cStat, info.xMotivo)
                raise UserError(msg)
        else:
            raise UserError(_(u'Fill the State and CNPJ fields to search'))
