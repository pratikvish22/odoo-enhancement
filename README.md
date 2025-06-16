# Odoo Enhancement

Adding additional functionality to odoo addons modules

## Features 🚀

### Sale Module

- Display warehouse costs directly in Sale Orders
- Automatic synchronization of costs with Delivery Orders

### Project Module

- Enhanced task dependencies management in projects
- Added support for task relationships and dependencies

## Project Structure

1. **`custom_addons/`**: Directory for custom Odoo modules
    - Contains all custom modules developed for this project
    - Each module follows Odoo's standard structure:

      ```text
      module_name/
      ├── __init__.py
      ├── __manifest__.py
      ├── models/
      ├── views/
      ├── security/
      └── data/
      ```

2. **`etc/`**: Configuration files and dependencies
    - **`odoo-sample.conf`**: Template configuration file
      - Sample configuration without sensitive data
      - Used as reference for setting up new environments

3. **`.env-sample/`**: Environment variables and secrets
    - **`db.env`**: Database environment variables
      - Contains database connection settings
      - Includes host, port, name, user and password
      - Not tracked in version control for security

    - **`odoo.env`**: Environment variables template
      - Sample configuration for database settings
      - Used as reference for local development
      - Contains placeholder values that need to be replaced

## Getting Started with Application

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. Set up environment files and update with your values:

   ```bash
   cp env-sample/ env/
   nano env/odoo.env
   nano env/db.env
   ```

3. Configure Odoo and update Odoo config:

   ```bash
   cp etc/odoo-sample.conf etc/odoo.conf
   nano etc/odoo.conf
   ```

4. Build and run with Docker:

   ```bash
   docker compose up --build
   ```

5. Accessing the application:

    ```bash
    http://localhost:8069
    ```
