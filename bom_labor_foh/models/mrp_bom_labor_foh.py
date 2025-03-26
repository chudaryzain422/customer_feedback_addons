from odoo import models, fields, api

class MrpBomLaborFoh(models.Model):
    _name = 'mrp.bom.labor.foh'
    _description = 'BOM Labor and FOH Components'

    bom_id = fields.Many2one('mrp.bom', string='Bill of Material', required=True, ondelete='cascade')
    product_id = fields.Many2one(
        'product.product', 
        string='Product',
        required=True,
        domain=[('type', '=', 'consu'),('is_labour', '=', True)],  # Only consumable products
    )
    product_qty = fields.Float(
        'Quantity',
        default=1.0,
        required=True,
    )
    cost = fields.Float(
        string='Cost',
        compute='_compute_cost',
        store=True,
    )

    @api.depends('product_id.standard_price', 'product_qty')
    def _compute_cost(self):
        for rec in self:
            rec.cost = rec.product_id.standard_price * rec.product_qty