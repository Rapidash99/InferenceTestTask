# InferenceTestTask
My solution for Inference Technologies test task for backend internship
## Task:
A microservice for messages processing (each message sends from one user to another). Messages should be processed via REST Api.
## Use case scenarios – CRUD:
* Create message
* Read message
* Update message
* Delete message
## Technologies:
* Python
* Django
* Django Rest Framework
## Urls:
### For authorized users:
* /api/v1/messenger/message/create/ **– Create message**
* /api/v1/messenger/message/all/ **– Read all messages that user may see (he is sender or owner)**
* /api/v1/message/user/<int:pk> **– Read all messages from chat with certain user (by user id)**
* /api/v1/message/user/<str:username **– Read all messages from chat with certain user (by username)**
* /api/v1/message/<int:pk> **– Read/Update/Delete certain message (by id)**
### For admins only:
* /api/v1/user/list/ **– Read all users information**
* /admin/ **– Admin menu**
### For unathorized:
* /api/v1/auth/ **– For login by Djoser**
* /api/v1/auth_token/ **– For login by Djoser**
