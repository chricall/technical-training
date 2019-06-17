from odoo import api, models, fields

class OpenacademySession (models.Model):
    _name = 'openacademy.session'
    _description = "Session for OpenAcademy"
    
    
    
    name = fields.Char(string="Name")
    date = fields.Datetime(string="Date and Time")
    state = fields.Selection([('1','Inactive'), ('2','Active')], string="State")
    archived = fields.Boolean(string="Archived")
    
    class_id = fields.Many2one('openacademy.class',string="Related Class")
    
    maester_id = fields.Many2one('res.partner',string="Session Maester")
    
    attendess_ids = fields.Many2many('res.partner',string="Session attendees")