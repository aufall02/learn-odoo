# -*- coding: utf-8 -*-
from odoo import models, fields, api
from openpyxl.drawing import effect
from openpyxl.worksheet import related


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient')
    gender = fields.Selection(related='patient_id.gender',
                              string='Gender',
                              readonly=False)
    age = fields.Integer(related='patient_id.age', string='Age', readonly=False)
    street = fields.Char(related='patient_id.street', string='Street', readonly=False)
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string='Reference Date')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([('1', 'Normal'),
                                 ('2', 'Low'),
                                 ('3', 'High'),
                                 ('4', 'Very High')],
                                string='Priority')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', required=True , tracking=True)
    testing = fields.Char(string='Testing', default='Default Testing Value')

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            summary='Testing Button Diklik!',
            note='Button action_test berhasil dijalankan',
            user_id=self.env.user.id,
        )
        return {
            'effect': {
                'fadeout':'slow',
                'message':'Anjay testing',
                'type':'rainbow_man'


            }
        }
