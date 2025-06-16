import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger("--------Project Task--------")


class ProjectTask(models.Model):
    _inherit = "project.task"

    depends_on_ids = fields.Many2many(
        "project.task",
        "project_task_dependency_rel",
        "task_id",
        "depends_on_id",
        string="Depends on",
        help="Tasks that this task depends on.",
    )

    @api.constrains("depends_on_ids")
    def _check_no_circular_dependency(self):
        for task in self:
            if task.id and task._has_circular_dependency(task, set()):
                _logger.warning(f"Circular dependency detected for task ID {task.id}")
                raise ValidationError(_("Circular dependency detected!"))

    def _has_circular_dependency(self, task, visited):
        if task.id in visited:
            return True
        visited.add(task.id)
        for dep in task.depends_on_ids:
            if dep.id == self.id or self._has_circular_dependency(dep, visited):
                return True
        visited.remove(task.id)
        return False

    @api.constrains("stage_id", "depends_on_ids", "kanban_state")
    def _compute_blocked(self):
        for task in self:
            if task.depends_on_ids and any(
                not dep.stage_id.is_closed for dep in task.depends_on_ids
            ):
                _logger.info(f"Task ID {task.id} is blocked due to dependencies.")
                raise ValidationError(_("Task is blocked because of the dependency."))
