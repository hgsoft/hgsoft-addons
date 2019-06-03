# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import base64
import re

try:
    from pytrustnfe.nfe import autorizar_nfe
    from pytrustnfe.nfe import xml_autorizar_nfe
    from pytrustnfe.certificado import Certificado
    from pytrustnfe.utils import ChaveNFe, gerar_chave
    from pytrustnfe.xml.validate import valida_nfe
except ImportError:
    _logger.error('Cannot import pytrustnfe', exc_info=True)

class customInvoiceEletronicTax(models.Model):
    _inherit = 'invoice.eletronic'
    
    @api.multi
    def action_post_validate(self):
        super(customInvoiceEletronicTax, self).action_post_validate()
        if self.model not in ('55', '65'):
            return
        chave_dict = {
            'cnpj': re.sub('[^0-9]', '', self.company_id.cnpj_cpf),
            'estado': self.company_id.state_id.ibge_code,
            'emissao': self.data_emissao[2:4] + self.data_emissao[5:7],
            'modelo': self.model,
            'numero': self.numero,
            'serie': self.serie.code.zfill(3),
            'tipo': int(self.tipo_emissao),
            'codigo': "%08d" % self.numero_controle
        }
        self.chave_nfe = gerar_chave(ChaveNFe(**chave_dict))

        cert = self.company_id.with_context(
            {'bin_size': False}).nfe_a1_file
        cert_pfx = base64.decodestring(cert)

        certificado = Certificado(
            cert_pfx, self.company_id.nfe_a1_password)

        nfe_values = self._prepare_eletronic_invoice_values()

        ###
        for value in nfe_values['detalhes']:
            if value['imposto']['ICMS']['CST'] == '500':
                value['imposto']['ICMS']['pST'] = '0.00'
                value['imposto']['ICMS']['vBCSTRet'] = '0.00'
                value['imposto']['ICMS']['vICMSSTRet'] = '0.00'
                value['imposto']['ICMS']['vICMSSubstituto'] = '0.00'
        ###

        lote = self._prepare_lote(self.id, nfe_values)

        xml_enviar = xml_autorizar_nfe(certificado, **lote)

        mensagens_erro = valida_nfe(xml_enviar)

        if mensagens_erro:
            raise UserError(mensagens_erro)

        self.xml_to_send = base64.encodestring(
            xml_enviar.encode('utf-8'))
        self.xml_to_send_name = 'nfse-enviar-%s.xml' % self.numero
