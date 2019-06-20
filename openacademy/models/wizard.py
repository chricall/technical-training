from odoo import api, exceptions, fields, models

class SessionWizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"
    
    def _default_attendees(self):
        return self.env['res.partner'].browse(self._context.get('active_ids'))
    
    session_id = fields.Many2one('openacademy.session', string="Session", required=True)
    
    attendee_ids = fields.Many2many('res.partner', string="Attendees",required=True, default=_default_attendees)
    
    @api.multi
    def action_subscribe(self):
        self.session_id.attendee_ids |= self.attendee_ids
        return {}