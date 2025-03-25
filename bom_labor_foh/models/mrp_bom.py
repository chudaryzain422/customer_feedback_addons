from odoo import models, fields

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    labor_foh_line_ids = fields.One2many(
        'mrp.bom.labor.foh',
        'bom_id',
        string='Labor and FOH Components'
    )