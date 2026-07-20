from odoo import models, fields


class TrainingWizard(models.Model):
    _name = 'training.wizard'
    _description = 'Training wizard'

    def _default_session(self):
        return self.env['training.session'].browse(self._context.get('active_ids'))

    session_id = fields.Many2one(comodel_name='training.session', string='Session Training', default=_default_session)
    participant_ids = fields.Many2many(comodel_name='participant', string='Peserta Training')

def add_participant(self):
    self.session_id.participant_ids |= self.participant_ids 
