# -*- coding: utf-8 -*-

###############################################################################
#                                                                             #
# Copyright (C) 2019 HGSOFT - www.hgsoft.com.br                               #
#                                                                             #
#This program is free software: you can redistribute it and/or modify         #
#it under the terms of the GNU Affero General Public License as published by  #
#the Free Software Foundation, either version 3 of the License, or            #
#(at your option) any later version.                                          #
#                                                                             #
#This program is distributed in the hope that it will be useful,              #
#but WITHOUT ANY WARRANTY; without even the implied warranty of               #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
#GNU General Public License for more details.                                 #
#                                                                             #
#You should have received a copy of the GNU General Public License            #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
###############################################################################
    
{
    'name': "Custom Survey To Evaluate Ideas",

    'summary': """Custom Survey To Evaluate Ideas""",

    'author': "HGSoft - Soluções Criativas e Inteligentes",
    
    'website': "http://www.hgsoft.com.br/",

    'category': 'Marketing',
    
    'version': '11.0.0',

    'depends': ['base', 'survey'],

    'data': [
        'views/custom_survey_views.xml',
        'views/survey.xml',
        'data/survey_idea.xml',
        'security/ir.model.access.csv',
    ],
    
}