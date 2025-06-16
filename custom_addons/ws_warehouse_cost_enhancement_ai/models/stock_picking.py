import logging
from odoo import api, fields, models

_logger = logging.getLogger("--------Stock Picking--------")


class StockPicking(models.Model):
    _inherit = "stock.picking"

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Currency used for warehouse cost",
    )

    warehouse_cost = fields.Monetary(
        string="Warehouse Cost",
        compute="_compute_warehouse_cost",
        store=True,
        currency_field="currency_id",
    )

    @api.depends(
        "sale_id.order_line.product_id.standard_price",
        "sale_id.order_line.product_uom_qty",
    )
    def _compute_warehouse_cost(self):
        for picking in self:
            total_cost = 0.0
            for move in picking.move_ids_without_package:
                if move.product_id:
                    total_cost += move.product_id.standard_price * move.product_uom_qty
            picking.warehouse_cost = total_cost
            _logger.debug(
                f"Computed warehouse cost for picking ID {picking.id}: {total_cost}"
            )
