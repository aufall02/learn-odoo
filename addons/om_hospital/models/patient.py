# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models, fields


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Hospital Patient'


    name = fields.Char(string='Patient Name', tracking=True)
    ref = fields.Char(string='Reference',
                      tracking=True,
                      default=lambda self: 'REF' + str(len(self.env['hospital.patient'].sudo().search([])) + 1).zfill(4))
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string='Gender',
                              tracking=True,
                              default='female')
    active = fields.Boolean(string='active', default=True, tracking=True)
    street = fields.Char(string='alamat')

