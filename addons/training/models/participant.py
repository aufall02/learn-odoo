from odoo import api, fields, models


class TrainingParticipant(models.Model):
    _name = 'training.participant'
    _description = 'Training Participant'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner',
                                 string='Partner',
                                 required=True,
                                 ondelete='cascade')
    no_participant = fields.Char(string='No. Participant', readonly=True)
    place_of_birth = fields.Char(string='Place of Birth')
    date_of_birth = fields.Date(string='Date of Birth')
    education = fields.Selection([('sd', 'SD'),
                                  ('smp', 'SMP'),
                                  ('sma', 'SMA/SMK'),
                                  ('d3', 'D3'),
                                  ('s1', 'Bachelor')],
                                 string='Education')
    occupation = fields.Char(string='Occupation')
    is_married = fields.Boolean(string='Married')
    spouse_name = fields.Char(string='Partner Name')
    spouse_phone = fields.Char(string='Phone Number')

    @api.model
    def create(self, vals):
        vals['no_participant'] = self.env['ir.sequence'].next_by_code('training.participant')
        return super(TrainingParticipant, self).create(vals)