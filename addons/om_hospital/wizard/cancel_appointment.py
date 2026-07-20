from odoo import fields, models

class CancelAppointmentWizard(models.Model):
    _name = "cancel.appointment.wizard"
    _description = "Cancel appointment wizard"

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
