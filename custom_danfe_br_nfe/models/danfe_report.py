# © 2017 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# © 2018 HGSOFT - www.hgsoft.com.br 
# * - Realizadas modificações para utilizar classe danfe interna ao invés da danfe contida no pytrust.
# * - Demais aspectos, não foram alterados.

import pytz
import base64
import logging
from lxml import etree
from io import BytesIO
from odoo import models

_logger = logging.getLogger(__name__)

try:
    #Update Module - Start
    from odoo.addons.custom_danfe_br_nfe.models.danfe import danfe
    #from pytrustnfe.nfe.danfe import danfe
    #Update Module - End
    from pytrustnfe.nfe.danfce import danfce
except ImportError:
    _logger.warning('Cannot import pytrustnfe', exc_info=True)


class CustomIrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def render_qweb_pdf(self, res_ids, data=None):
        if self.report_name != 'br_nfe.main_template_br_nfe_danfe':
            return super(CustomIrActionsReport, self).render_qweb_pdf(
                res_ids, data=data)

        nfe = self.env['invoice.eletronic'].search([('id', 'in', res_ids)])

        nfe_xml = base64.decodestring(nfe.nfe_processada)

        cce_xml_element = []
        cce_list = self.env['ir.attachment'].search([
            ('res_model', '=', 'invoice.eletronic'),
            ('res_id', '=', nfe.id),
            ('name', 'like', 'cce-')
        ])

        if cce_list:
            for cce in cce_list:
                cce_xml = base64.decodestring(cce.datas)
                cce_xml_element.append(etree.fromstring(cce_xml))

        logo = False
        if nfe.invoice_id.company_id.logo:
            logo = base64.decodestring(nfe.invoice_id.company_id.logo)
        elif nfe.invoice_id.company_id.logo_web:
            logo = base64.decodestring(nfe.invoice_id.company_id.logo_web)

        if logo:
            tmpLogo = BytesIO()
            tmpLogo.write(logo)
            tmpLogo.seek(0)
        else:
            tmpLogo = False

        timezone = pytz.timezone(self.env.context.get('tz')) or pytz.utc

        xml_element = etree.fromstring(nfe_xml)
        obj_danfe = danfe
        if nfe.model == '65':
            obj_danfe = danfce
        oDanfe = obj_danfe(list_xml=[xml_element], logo=tmpLogo,
                           cce_xml=cce_xml_element, timezone=timezone)

        tmpDanfe = BytesIO()
        oDanfe.writeto_pdf(tmpDanfe)
        danfe_file = tmpDanfe.getvalue()
        tmpDanfe.close()
        
        return danfe_file, 'pdf'
