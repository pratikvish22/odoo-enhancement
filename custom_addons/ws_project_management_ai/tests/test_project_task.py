# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged

@tagged('ws_project_management_ai')
class TestProjectTaskDependency(TransactionCase):
    """Test project.task dependency logic in ws_project_management_ai."""

    def setUp(self):
        super().setUp()
        ProjectStage = self.env["project.task.type"]
        self.stage_open = ProjectStage.create({"name": "Open", "is_closed": False})
        self.stage_closed = ProjectStage.create({"name": "Closed", "is_closed": True})

    def test_no_circular_dependency(self):
        ProjectTask = self.env["project.task"]
        task1 = ProjectTask.create({"name": "Task 1", "stage_id": self.stage_closed.id})
        task2 = ProjectTask.create({"name": "Task 2", "stage_id": self.stage_closed.id})
        task1.depends_on_ids = [(6, 0, [task2.id])]
        with self.assertRaises(ValidationError):
            task2.depends_on_ids = [(6, 0, [task1.id])]

    def test_blocked_by_dependency(self):
        ProjectTask = self.env["project.task"]
        task1 = ProjectTask.create({"name": "Task 1", "stage_id": self.stage_open.id})
        task2 = ProjectTask.create({"name": "Task 2", "stage_id": self.stage_open.id})
        with self.assertRaises(ValidationError):
            task1.depends_on_ids = [(6, 0, [task2.id])]
        # Now close the dependency and check no error
        task2.stage_id = self.stage_closed.id
        task1.depends_on_ids = [(6, 0, [task2.id])]
        task1._compute_blocked()  # Should not raise

    def test_no_block_when_no_dependency(self):
        ProjectTask = self.env["project.task"]
        task1 = ProjectTask.create({"name": "Task 1", "stage_id": self.stage_open.id})
        task1.depends_on_ids = [(6, 0, [])]
        task1._compute_blocked()  # Should not raise

    def test_blocked_on_kanban_state_change(self):
        ProjectTask = self.env["project.task"]
        task1 = ProjectTask.create({"name": "Task 1", "stage_id": self.stage_open.id})
        task2 = ProjectTask.create({"name": "Task 2", "stage_id": self.stage_open.id})
        with self.assertRaises(ValidationError):
            task1.depends_on_ids = [(6, 0, [task2.id])]
        # Unblock by closing dependency
        task2.stage_id = self.stage_closed.id
        task1.depends_on_ids = [(6, 0, [task2.id])]
        task1.kanban_state = "done"
        task1._compute_blocked()  # Should not raise

    def test_blocked_with_multiple_dependencies(self):
        ProjectTask = self.env["project.task"]
        t1 = ProjectTask.create({"name": "T1", "stage_id": self.stage_open.id})
        t2 = ProjectTask.create({"name": "T2", "stage_id": self.stage_closed.id})
        t3 = ProjectTask.create({"name": "T3", "stage_id": self.stage_open.id})
        with self.assertRaises(ValidationError):
            t1.depends_on_ids = [(6, 0, [t2.id, t3.id])]
        # Close all dependencies
        t3.stage_id = self.stage_closed.id
        t1.depends_on_ids = [(6, 0, [t2.id, t3.id])]
        t1._compute_blocked()  # Should not raise

    def test_unblock_by_removing_dependency(self):
        ProjectTask = self.env["project.task"]
        t1 = ProjectTask.create({"name": "T1", "stage_id": self.stage_open.id})
        t2 = ProjectTask.create({"name": "T2", "stage_id": self.stage_open.id})
        with self.assertRaises(ValidationError):
            t1.depends_on_ids = [(6, 0, [t2.id])]
        # Remove dependency
        t1.depends_on_ids = [(6, 0, [])]
        t1._compute_blocked()  # Should not raise

    def test_self_dependency_not_allowed(self):
        ProjectTask = self.env["project.task"]
        t1 = ProjectTask.create({"name": "T1", "stage_id": self.stage_closed.id})
        with self.assertRaises(ValidationError):
            t1.depends_on_ids = [(6, 0, [t1.id])]

    def test_dependency_on_closed_task(self):
        ProjectTask = self.env["project.task"]
        t1 = ProjectTask.create({"name": "T1", "stage_id": self.stage_open.id})
        t2 = ProjectTask.create({"name": "T2", "stage_id": self.stage_closed.id})
        t1.depends_on_ids = [(6, 0, [t2.id])]
        t1._compute_blocked()  # Should not raise

    def test_dependency_becomes_closed(self):
        ProjectTask = self.env["project.task"]
        t1 = ProjectTask.create({"name": "T1", "stage_id": self.stage_open.id})
        t2 = ProjectTask.create({"name": "T2", "stage_id": self.stage_open.id})
        with self.assertRaises(ValidationError):
            t1.depends_on_ids = [(6, 0, [t2.id])]
        t2.stage_id = self.stage_closed.id
        t1.depends_on_ids = [(6, 0, [t2.id])]
        t1._compute_blocked()  # Should not raise

    def test_unrelated_tasks(self):
        ProjectTask = self.env["project.task"]
        t1 = ProjectTask.create({"name": "T1", "stage_id": self.stage_open.id})
        t2 = ProjectTask.create({"name": "T2", "stage_id": self.stage_open.id})
        t1._compute_blocked()
        t2._compute_blocked()
        # No dependencies, should not raise
