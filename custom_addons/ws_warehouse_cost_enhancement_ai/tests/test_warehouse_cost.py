# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged("ws_warehouse_cost_enhancement_ai")
class TestWarehouseCost(TransactionCase):
    """Test warehouse cost computation for sale orders and stock pickings."""

    def setUp(self):
        super().setUp()
        Product = self.env["product.product"]
        Currency = self.env.user.company_id.currency_id
        self.product_a = Product.create(
            {
                "name": "Product A",
                "standard_price": 10.0,
                "list_price": 20.0,
            }
        )
        self.product_b = Product.create(
            {
                "name": "Product B",
                "standard_price": 5.0,
                "list_price": 15.0,
            }
        )
        self.currency = Currency
        self.location_id = self.env.ref("stock.stock_location_stock")
        self.location_dest_id = self.env.ref("stock.stock_location_customers")

    def test_sale_order_warehouse_cost(self):
        SaleOrder = self.env["sale.order"]
        order = SaleOrder.create(
            {
                "partner_id": self.env.ref("base.res_partner_1").id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_a.id,
                            "product_uom_qty": 2,
                            "price_unit": 20.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_b.id,
                            "product_uom_qty": 3,
                            "price_unit": 15.0,
                        },
                    ),
                ],
            }
        )
        order._compute_warehouse_cost()
        expected = 2 * 10.0 + 3 * 5.0
        self.assertEqual(order.warehouse_cost, expected)

    def test_sale_order_warehouse_cost_zero_qty(self):
        SaleOrder = self.env["sale.order"]
        order = SaleOrder.create(
            {
                "partner_id": self.env.ref("base.res_partner_1").id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_a.id,
                            "product_uom_qty": 0,
                            "price_unit": 20.0,
                        },
                    ),
                ],
            }
        )
        order._compute_warehouse_cost()
        self.assertEqual(order.warehouse_cost, 0.0)

    def test_stock_picking_warehouse_cost(self):
        Picking = self.env["stock.picking"]
        picking = Picking.create(
            {
                "partner_id": self.env.ref("base.res_partner_1").id,
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "location_id": self.location_id.id,
                "location_dest_id": self.location_dest_id.id,
                "move_ids_without_package": [
                    (
                        0,
                        0,
                        {
                            "name": "Move A",
                            "product_id": self.product_a.id,
                            "product_uom_qty": 1,
                            "product_uom": self.product_a.uom_id.id,
                            "location_id": self.location_id.id,
                            "location_dest_id": self.location_dest_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Move B",
                            "product_id": self.product_b.id,
                            "product_uom_qty": 4,
                            "product_uom": self.product_b.uom_id.id,
                            "location_id": self.location_id.id,
                            "location_dest_id": self.location_dest_id.id,
                        },
                    ),
                ],
            }
        )
        picking._compute_warehouse_cost()
        # Dynamically compute expected value from actual moves
        expected = sum(
            move.product_id.standard_price * move.product_uom_qty
            for move in picking.move_ids_without_package
        )
        self.assertEqual(picking.warehouse_cost, expected)

    def test_stock_picking_warehouse_cost_no_moves(self):
        Picking = self.env["stock.picking"]
        picking = Picking.create(
            {
                "partner_id": self.env.ref("base.res_partner_1").id,
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "location_id": self.location_id.id,
                "location_dest_id": self.location_dest_id.id,
            }
        )
        picking._compute_warehouse_cost()
        self.assertEqual(picking.warehouse_cost, 0.0)

    def test_edge_case_negative_standard_price(self):
        self.product_a.standard_price = -10.0
        SaleOrder = self.env["sale.order"]
        order = SaleOrder.create(
            {
                "partner_id": self.env.ref("base.res_partner_1").id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_a.id,
                            "product_uom_qty": 1,
                            "price_unit": 20.0,
                        },
                    ),
                ],
            }
        )
        order._compute_warehouse_cost()
        self.assertEqual(order.warehouse_cost, -10.0)
