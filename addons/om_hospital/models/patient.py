# -*- coding: utf-8 -*-

from odoo import models, fields


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Hospital Patient'

    name = fields.Char(string='Patient Name', tracking=True)
    ref = fields.Char(string='Reference', tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string='Gender',
                              tracking=True,
                              default='female')
    active = fields.Boolean(string='active', default=True, tracking=True)


