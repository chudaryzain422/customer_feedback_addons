from odoo import models, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def create(self, values):
        production = super().create(values)
        if production.bom_id:
            # Add Labor and FOH components to the manufacturing order
            for labor_foh in production.bom_id.labor_foh_line_ids:
                self.env['stock.move'].create({
                    'name': labor_foh.product_id.name,
                    'product_id': labor_foh.product_id.id,
                    'product_uom_qty': labor_foh.product_qty,
                    'product_uom': labor_foh.product_id.uom_id.id,
                    'location_id': production.location_src_id.id,
                    'location_dest_id': production.product_id.property_stock_production.id,
                    'raw_material_production_id': production.id,
                    'company_id': production.company_id.id,
                })
        return production