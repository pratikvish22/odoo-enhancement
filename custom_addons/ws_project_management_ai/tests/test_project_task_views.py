# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.tests import tagged

@tagged('ws_project_management_ai')
class TestProjectTaskViews(TransactionCase):
    """Test the project.task form view modifications in ws_project_management_ai."""

    def test_depends_on_ids_field_in_form_view(self):
        # Use env.ref to get the view by XML ID
        view = self.env.ref('ws_project_management_ai.view_project_task_form', raise_if_not_found=False)
        self.assertTrue(view, "Custom project.task form view not found")
        # Check that the field is present in the view arch
        self.assertIn('depends_on_ids', view.arch_db, "'depends_on_ids' field not found in the form view architecture")
        # Check that the widget is set to many2many_tags
        self.assertIn('widget="many2many_tags"', view.arch_db, "'depends_on_ids' field does not have the correct widget")
