# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError

class Crmext(models.Model):
    #_name = 'library.crmext'
    #_description = 'CRM Extension'
    _inherit = ['crm.lead']
    
    def action_set_won_rainbowman(self):        
        result = super(Crmext, self).action_set_won_rainbowman()
        result['effect']['message'] = "IT IS WORKING!!!!!"
        return result