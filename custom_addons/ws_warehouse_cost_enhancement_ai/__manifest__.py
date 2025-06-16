{
    "name": "Warehouse Cost Enhancement AI",
    "version": "15.0.1.0.0",
    "summary": "Show and sync warehouse cost in Sale and Delivery Orders",
    "category": "Sales",
    "author": "Neelima",
    "description": """
        This module provides the following features:
        1. Show and sync warehouse cost in Sale and Delivery Orders
    """,
    "website": "https://www.marsdevs.com",
    "depends": ["sale_management", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
