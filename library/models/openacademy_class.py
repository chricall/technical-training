from odoo import api, models, fields

class OpenacademyClass (models.Model):
    _name = 'openacademy.class'
    _description = "Class for OpenAcademy"
    
    name = fields.Char(string="Name")
    level = fields.Selection([('1','Beginner'), ('2','Intermediate'), ('3','Advanced')], string="Level")
    
    session_ids = fields.One2many('openacademy.session','class_id',string="Related Sessions")
