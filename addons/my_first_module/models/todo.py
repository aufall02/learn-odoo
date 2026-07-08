# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TodoTask(models.Model):
    """A simple To-Do task model for learning Odoo development."""

    _name = "todo.task"
    _description = "To-Do Task"
    _order = "priority desc, create_date desc"

    name = fields.Char(
        string="Task Title",
        required=True,
        help="Enter the title of your task",
    )
    description = fields.Text(
        string="Description",
        help="Detailed description of the task",
    )
    is_done = fields.Boolean(
        string="Done?",
        default=False,
    )
    priority = fields.Selection(
        selection=[
            ("0", "Normal"),
            ("1", "Low"),
            ("2", "High"),
            ("3", "Urgent"),
        ],
        string="Priority",
        default="0",
    )
    deadline = fields.Date(
        string="Deadline",
    )
    responsible_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        comodel_name="todo.tag",
        string="Tags",
    )

    def action_mark_done(self):
        """Mark the task as done."""
        for record in self:
            record.is_done = True

    def action_mark_undone(self):
        """Mark the task as not done."""
        for record in self:
            record.is_done = False


class TodoTag(models.Model):
    """Tags for categorizing To-Do tasks."""

    _name = "todo.tag"
    _description = "To-Do Tag"

    name = fields.Char(
        string="Tag Name",
        required=True,
    )
    color = fields.Integer(
        string="Color Index",
    )
