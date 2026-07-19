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
    # testing = fields.Char(string='Testing', default='Default Testing Value')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_line_ids = fields.Many2one('appointment.pharmacy.lines','appointment_id',string="Pharmacy Lines")

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

    def action_in_consultation(self):
        for rec in self:
            rec.status = "in_consultation"
    def action_done(self):
        for rec in self:
            rec.status = "done"
    def action_cancel(self):
        for rec in self:
            rec.status = "cancel"

class AppointmentPharmacyLines(models.Model):
    _name   = "appointment.pharmacy.lines"
    _description = "appointment pharmacy lines" 

    product_id = fields.Many2one('product.product',  required=True)
    price_unit = fields.Float(related="product_id.list_price")
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.One2many('hospital.appointment', string="Appointment")