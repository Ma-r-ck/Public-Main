from odoo import  fields, models, api



class PivotConditionalSetting(models.Model):
    _name = 'pivot.conditional.settings'
    _description = 'pivot conditional setting'

    model_id = fields.Many2one('ir.model')
    view_id = fields.Many2one('ir.ui.view' )
    rules_ids = fields.One2many('conditional.rules','conditional_id')

    @api.onchange('model_id')
    def onchange_field_model(self):
        return {'domain': {'view_id': [('model', '=', self.model_id.model),('type','=','pivot')]}}


class ConditionalRules(models.Model):
    _name = 'conditional.rules'
    _description = 'conditional formatting'

    rule = fields.Selection(string='Rule', selection=([
        ('greater_than','Greater than'),('less_than','Less Than'),
        ('is_empty','Is Empty'),('in_between','In Between')]))

    value = fields.Float(string='Value')
    second_value = fields.Float(string='Second value')
    color = fields.Char(string='Color', required=True)
    text_color = fields.Char(string='Text Color', required=True)
    model = fields.Many2one('ir.model', related='conditional_id.model_id')
    view_id = fields.Many2one('ir.ui.view', related='conditional_id.view_id')
    conditional_id = fields.Many2one('pivot.conditional.settings')