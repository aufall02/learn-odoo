# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Hospital Patient'


    name = fields.Char(string='Patient Name', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    ref = fields.Char(string='Reference',
                      tracking=True,
                      )
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string='Gender',
                              tracking=True,
                              default='female')
    active = fields.Boolean(string='active', default=True, tracking=True)
    street = fields.Char(string='Address')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")


    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('anjay.patient')
        return super(HospitalPatient, self).create(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1
