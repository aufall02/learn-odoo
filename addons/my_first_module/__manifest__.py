# -*- coding: utf-8 -*-
{
    "name": "My First Module",
    "version": "18.0.1.0.0",
    "summary": "A sample module to learn Odoo development",
    "description": """
        This is a sample custom module for learning Odoo development.
        It demonstrates the basic structure of an Odoo module including:
        - Models
        - Views
        - Security (access rights)
    """,
    "author": "Aufal",
    "website": "",
    "category": "Uncategorized",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/todo_views.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
