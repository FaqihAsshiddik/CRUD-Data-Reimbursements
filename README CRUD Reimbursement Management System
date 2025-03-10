```markdown
# CRUD Reimbursement Management System

A comprehensive reimbursement management application with role-based access controls.

## Overview

This Python-based application provides a complete solution for managing business reimbursements across different organizational roles. The system implements CRUD (Create, Read, Update, Delete) operations with appropriate permissions based on user roles.

## Features

- **Role-based access control** (Admin, Manager, Employee)
- **Complete CRUD functionality**
- **Data validation** for all inputs
- **Category-based spending limits**
- **Detailed audit trails** for changes and deletions
- **Advanced search and filtering** capabilities

## User Roles

| Role | Permissions |
|------|-------------|
| **Admin** | Full system access (add, view, update, delete, search) |
| **Manager** | Can add, view, update, and approve/reject reimbursements |
| **Employee** | Can submit and view own reimbursements, update pending submissions |

## Installation

1. Ensure Python 3.6+ is installed
2. Install required package:
   ```
   pip install tabulate
   ```
3. Download the source code
4. Run `python reimbursement_system.py`

## Usage

### Login Credentials

- **Admin**: Username: `admin`, Password: `purwadhika37`
- **Manager**: Username: `manager`, Password: `purwadhika50`
- **Employee**: Username: `emp_[ID]`, Password: `pass_[ID]` (e.g., `emp_25001`, `pass_25001`)

### Workflow

1. **Adding Reimbursements**:
   - Select category, amount, date, and provide description
   - System validates inputs against predefined rules

2. **Viewing Reimbursements**:
   - Admins/Managers see all reimbursements
   - Employees see only their own submissions

3. **Updating Reimbursements**:
   - Different options based on user role
   - All changes are tracked with audit information

4. **Approving/Rejecting** (Managers and Admins):
   - Review pending submissions
   - Provide rejection reasons if needed

5. **Searching and Filtering**:
   - Filter by employee, category, status, date range, or amount

## Data Model

- **Users**: Authentication and role information
- **Reimbursements**: Core expense data with approval status
- **Categories**: Predefined expense types with spending limits
- **Deletion Logs**: Audit trail for deleted records

## Future Enhancements

- Database integration for persistent storage
- Password hashing for improved security
- Export functionality for reporting
- Data visualization for spending analytics
- Email notifications for status changes

## Technologies

- Python 3.6+
- Tabulate (for formatted console output)
- Data structures: Dictionaries and Lists

## License

This project is intended for educational purposes.
```
