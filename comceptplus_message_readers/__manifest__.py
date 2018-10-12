# -*- coding: utf-8 -*-
{
    'name': "Message readers",
    'version': '1.0',
    'license': 'AGPL-3',
    'author' : 'comceptPLUS',
    'website' : 'https://comceptplus.com',
    'support': 'odoo@comceptplus.com',
    'category': 'Tools',
    'summary': 'Shows who has read the chatter messages',
    'description': 'Shows who has read the chatter messages',
    'depends': ['mail'],
    'data': [
            'views/mail_templates.xml',
            'views/mail_view.xml',
            ],
    'qweb': ['static/src/xml/thread.xml'],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
