from odoo import fields, models

class CancelAppointmentWizard(models.Model):
    _name = "cancel.appoinment.wizard"
    _description = "Cancel appointment wizard"\

    appointment_id = fields.Many2one('hospital.apppointment', string='Appointment')
    