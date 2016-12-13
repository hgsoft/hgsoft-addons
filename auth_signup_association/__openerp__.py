# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2014 HGSOFT - www.hgsoft.com.br                         #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

{
    'name': 'Signup Association',
    'description': """
Allow users to sign up, reset their password and complete your personal data
============================================================================
    """,
    'author': 'HGSOFT',
    'license': 'AGPL-3',
    'website': 'http://www.hgsoft.com.br',
    'contributors': ['Alexsandro Haag <alex@hgsoft.com.br>'],
    'version': '8.0.1.0.0',
    'category': 'Authentication',
    'installable': True,
    'auto_install': True,
    'depends': [
        'base_setup',
        'email_template',
        'web',
        'association',
        'l10n_br_base',
    ],
    'data': [
        'auth_signup_data.xml',
        'res_config.xml',
        'res_users_view.xml',
        'views/auth_signup_login.xml',
    ],
    'bootstrap': True,
}
