from odoo import models, fields


class TrainingWizard(models.TransientModel):
    _name = 'training.wizard'
    _description = 'Training wizard'

    def _default_session(self):
        return self.env['training.session'].browse(self._context.get('active_ids'))

    session_id = fields.Many2one(comodel_name='training.session', string='Session Training', default=_default_session)
    participant_ids = fields.Many2many(comodel_name='training.participant', string='Peserta Training')
    session_ids = fields.Many2many(comodel_name='training.session', string='Multi Sesi Training', default=_default_session)

    def add_participant(self):
        self.session_id.participant_ids |= self.participant_ids
        return {"type": "ir.actions.act_window_close"} 
    
    def tambah_banyak_peserta(self):
        for session in self.session_ids:
            session.peserta_ids |= self.peserta_ids

