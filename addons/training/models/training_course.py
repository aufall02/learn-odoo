# -*- coding: utf-8 -*-

from odoo import models, fields


class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'training.course'

    name = fields.Char(string='Course Name', required=True)
    description = fields.Text(string='Course Description')
    user_id = fields.Many2one(comodel_name='res.users', string='Trainer', required=True)
    session_id = fields.Many2one(comodel_name='training.session', inverse_name='course_id', string='Session',)


class TrainingSession(models.Model):
    _name = 'training.session'
    _description = 'training.session'
    name = fields.Char(string='Session Name', required=True)
    description = fields.Text(string='Session Description')
    course_id = fields.Many2one(comodel_name='training.course', required=True)
    start_date = fields.Datetime(string='Start Date', required=True)
    duration = fields.Integer(string='Duration', required=True)
    seats = fields.Integer(string='Seats', required=True)
