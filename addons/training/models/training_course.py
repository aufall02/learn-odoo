# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'training.course'

    name = fields.Char(string='Course Name', required=True)
    description = fields.Text(string='Course Description')
    trainer_id = fields.Many2one(comodel_name='training.instructor', string='Trainer', required=True)
    session_ids = fields.One2many(comodel_name='training.session', inverse_name='course_id', string='Sessions')


class TrainingSession(models.Model):
    _name = 'training.session'
    _description = 'training.session'

    instructor_id = fields.Many2one(related='course_id.trainer_id', string='Instructor', readonly=True)
    instructor_phone = fields.Char(string='Instructor Phone', related='instructor_id.mobile', readonly=True)
    instructor_mail = fields.Char(string='Instructor Email', related='instructor_id.email', readonly=True)
    instructor_gender = fields.Selection(related='instructor_id.gender', readonly=True)

    name = fields.Char(string='Session Name', required=True)
    description = fields.Text(string='Session Description')
    course_id = fields.Many2one(comodel_name='training.course', required=True)
    start_date = fields.Datetime(string='Start Date', required=True)
    duration = fields.Integer(string='Duration', required=True)
    seats = fields.Integer(string='Seats', required=True)

    participant_ids = fields.Many2many(comodel_name='training.participant', string='Participants')
    total_participant = fields.Integer(string='Total Participant', compute='_compute_total_participant')
    status = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done')], string='Status',
                              default='draft', tracking=True)

    @api.depends('participant_ids')
    def _compute_total_participant(self):
        for session in self:
            session.total_participant = len(session.participant_ids)

    def action_done(self):
        self.status = 'done'
    def action_draft(self):
        self.status = 'draft'
    def action_confirm(self):
        self.status = 'confirm'
