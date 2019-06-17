# -*- coding: utf-8 -*-
from odoo import fields,models,api
from odoo.exceptions import ValidationError

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('openacademy.partner', string="Responsible")
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
    
    maxattendees = fields.Integer(string="Maximum Attendees")

    level = fields.Selection([(1, 'Easy'), (2, 'Medium'), (3, 'Hard')], string="Difficulty Level")


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Session'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([('draft', "Draft"), ('confirmed', "Confirmed"), ('done', "Done")], default='draft')

    start_date = fields.Date(default=fields.Date.context_today)
    duration = fields.Float(digits=(6, 2), help="Duration in days", default=1)
    
    maxattendees = fields.Integer(related="course_id.maxattendees",string="Maximum Attendees",store=True)

    instructor_id = fields.Many2one('openacademy.partner', string="Instructor")
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    
    # -- method 1 --
    #@api.constrains('attendee_ids','maxattendees')
    #def _check_attendees_count(self):
    #    if self.attendees_count > self.maxattendees:
    #        raise ValidationError("Your cannot have more than %s records" % self.maxattendees)
    #
    #-- method 2 --
    #_sql_constraints = [
    #     ('attandeeslimitcheck', 'CHECK (attendees_count <= maxattendees)', 'You have exceed attendees limit'),
    #]    
    #
    @api.onchange('duration')
    def onchange_duration(self):
        if self.duration > 5:
            self.name = self.name+ " (long long course)"
    
    attendee_ids = fields.Many2many('openacademy.partner', string="Attendees")
    attendees_count = fields.Integer(compute='_compute_attendees_count',string="Count of Attendees",store=True)
    @api.depends('attendee_ids')
    def _compute_attendees_count(self):
        self.attendees_count = len(self.attendee_ids)
        

        
        