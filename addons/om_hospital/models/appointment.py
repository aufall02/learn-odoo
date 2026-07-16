# -*- coding: utf-8 -*-
from odoo import models, fields
from openpyxl.worksheet import related


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient')
    gender = fields.Selection(related='patient_id.gender',
                              string='Gender',
                              readonly=False)
    age = fields.Integer(related='patient_id.age', string='Age', readonly=False)
    street = fields.Char(related='patient_id.street', string='Street', readonly=False)
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
