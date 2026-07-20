# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",
    'version': '1.0',
    'category': 'Hospital',
    'author' : 'aufal',
    'sequence': 1,
    'summary': """Hospital Management System""",
    'description': """Hospital Management System""",
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag.xml'
    ],
    'depends': ['base','mail','product'],
    'demo': [],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
    }
