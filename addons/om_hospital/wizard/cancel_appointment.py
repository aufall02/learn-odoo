from odoo import fields, models, api
import datetime


class CancelAppointmentWizard(models.Model):
    _name = "cancel.appointment.wizard"
    _description = "Cancel appointment wizard"

    @api.model
    def default_get(self, fields):
        print('get function')
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['cancel_date'] = datetime.date.today()
        return res

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    reason = fields.Text(string='Reason')
    cancel_date = fields.Date(string='Cancel Date')


    def action_cancel(self):
        return


