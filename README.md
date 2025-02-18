
# Employee Leave Management System

This Django application allows an admin to manage employee data and view leave reports, while enabling employees to track and apply for leave. Below is a description of the key functionalities:

## Features

### 1. **Admin Dashboard**
- **View Employee Information**: The admin can view a list of employees, including their leave balances (sick leave and earned leave).
- **Leave Report**: The admin can see a breakdown of leaves taken by each employee for the current month, quarter, and year.

### 2. **Modify Employee Details**
- **Edit Employee Information**: The admin can modify employee profiles. The employee password must be a 4-digit number.
- **Form Validation**: A validation error will be shown if the password is not 4 digits long.

### 3. **Employee Login**
- **Login with Phone Number and Password**: Employees can log in with their phone number and a 4-digit password.
- **Session Management**: After successful login, the employee's details are stored in the session.

### 4. **Employee Dashboard**
- **View Leave Balances**: Employees can view their sick and earned leave balances.
- **Leave History**: Employees can see the number of leave days taken in the current month, quarter, and year.

### 5. **Apply for Leave**
- **Leave Application Form**: Employees can apply for leave through a form that captures start and end dates, and leave type.
- **Leave Deduction**: When leave is approved, the corresponding leave balance (sick or earned) is reduced based on the number of days applied for.

## Key Models:
1. **EmployeeProfile**: Stores employee details (name, phone number, password, leave balances, etc.).
2. **EmployeeLeave**: Tracks employee leave requests, including the type and dates of leave taken.

## Key Forms:
1. **EmployeeForm**: Form to edit employee details.
2. **LeaveApplicationForm**: Form for employees to apply for leave.

## Key Views:
- **admin_dashboard**: View for the admin to see employee leave reports.
- **modify_employee**: View for the admin to modify employee details.
- **employee_login**: Login page for employees to authenticate using their phone number and password.
- **employee_dashboard**: Dashboard for employees to see leave balances and applied leaves.
- **apply_leave**: Page for employees to apply for leave.

## Notes:
- All views are protected by the `@login_required` decorator to ensure that only logged-in users can access them.
- The application uses Django's ORM to query employee leave data and calculate leave balances.

## Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/01e529b5-bd14-40d3-bc35-ce042814c132" width="500" height="250" /><br>
  <img src="https://github.com/user-attachments/assets/e8d30cf8-1b18-4a3d-83a6-d068424ceba9" width="500" height="250" /><br>
  <img src="https://github.com/user-attachments/assets/00b265a7-1124-4874-8a78-4ec991063538" width="500" height="250" /><br>
  <img src="https://github.com/user-attachments/assets/1cfbca42-1d2a-4304-8263-26fb99ec3f60" width="500" height="250" /><br>
  <img src="https://github.com/user-attachments/assets/4ef238f5-5858-433a-9e13-ff8dfa36cd1c" width="500" height="250" /><br>
</p>


