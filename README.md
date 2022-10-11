# ToDo

This is backend for ToDo app. It is written in Python using Django framework. This provides REST API for Web, Desktop
and Mobile clients.

## Available API

1. User
    1. Login (Get Token) - `POST /api/token/`
    2. Register - `POST /api/users/`
    3. Change Password
    4. Reset Password
    5. Token Refresh - `POST /api/token/refresh/`
    6. Token Verify - `POST /api/token/verify/`
    7. User Details
    8. User Update
2. ToDo
    1. Create ToDo
    2. Update ToDo
    3. Delete ToDo
    4. Get ToDo
    5. Get ToDo List
    6. Set Alarm
    7. Set reminder
    8. Share ToDo
    9. Get suggestions
