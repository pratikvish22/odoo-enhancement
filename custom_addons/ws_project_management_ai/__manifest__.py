{
    "name": "WS Project Management AI",
    "version": "15.0.1.0.0",
    "summary": "Project task dependencies with blocked state",
    "category": "Project",
    "author": "Neelima",
    "description": """
        This module provides the following features:
        1. Dependencies on each task
        2. If a dependent task is not completed, it will block the current task
    """,
    "website": "https://www.marsdevs.com",
    "depends": ["project"],
    "data": ["views/project_task_views.xml"],
    "installable": True,
    "application": True,
    "auto_install": False,
}
