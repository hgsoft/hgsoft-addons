# -*- encoding: utf-8 -*-
##############################################################################
#
#    This module allows Clients to view external content through iframes by accessing 
#    their personal account of the Odoo Virtual Office. This can be used to add content 
#    from sources such as external report servers.
#    Copyright (C) 2020- todooweb.com (https://www.todooweb.com)
#    @author ToDOO (https://www.linkedin.com/company/todooweb)
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Iframes Dashboard",
    'summary': """Extend the Odoo Virtual Office with the option to add external iFrames.""",
    'description': """
        Extend the Odoo Virtual Office with the option to add external iFrames.
    """,
    'version': '13.0.0.0.1',
    'category': 'Website',
    'license': 'LGPL-3',
    'author': "ToDOO (www.todooweb.com)",
    'website': "https://todooweb.com/",
    'contributors': [
        "Equipo Dev <devtodoo@gmail.com>",
        "Edgar Naranjo <edgarnaranjof@gmail.com>",
        "Tatiana Rosabal <tatianarosabal@gmail.com>",
    ],
    'support': 'devtodoo@gmail.com',
    'depends': ['base',
                'sale',
                'account',
                'mail',
                'website',
                'website_sale',
                'website_crm_partner_assign'
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/website_iframe.xml',
    ],
    'images': [
        'static/description/iframe_screenshot.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
