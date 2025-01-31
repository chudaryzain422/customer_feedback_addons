from odoo import models, fields

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    is_feedback_survey = fields.Boolean(string="Use as Feedback Survey", default=False)
