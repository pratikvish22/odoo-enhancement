# Odoo Enhancement
Adding additional functionality to odoo addons modules

## Key Points in This `README.md`

1. **`custom_addons/`**: A dedicated directory for your custom Odoo modules.

- **Purpose**: This directory is specifically designated for custom modules that developers create for the Odoo project.
  - **Module Naming**: Each module should be placed as a subdirectory under `custom_addons/`.
  - **Development**: Developers should add their Odoo modules inside this directory, following Odoo's standard module structure.

2. **`etc/requirements.txt`**: A list of Python dependencies necessary for your custom modules.
    - **Purpose**: This file lists all the external Python dependencies required to run the project.
    - **Usage**: Developers should add any external packages or libraries needed for the custom modules inside this file.

3. **`etc/odoo.config`**: Describes the function of the configuration file, what settings it can include.
