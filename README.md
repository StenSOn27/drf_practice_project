# Libary API

This project is a RESTful API built with Django REST Framework, designed to manage books, users, and borrowing operations in a library system.

## Features

- **Books Service:** Full CRUD functionality with permissions restricting write operations to admin users only, while allowing anyone (even unauthenticated) to view the book listings. JWT authentication is integrated from the Users Service.
  
- **Users Service:** Handles user registration and authentication using JWT. Customizes the authorization header for better integration with tools like ModHeader.
  
- **Borrowings Service:** Allows authenticated users to borrow and return books with inventory management. Borrowing records are filtered by user permissions, with admins able to view all borrowings and apply additional filters.

## Technologies Used

- Python 3.x  
- Django & Django REST Framework  
- JWT Authentication  

## Setup Instructions

Follow these steps to set up and run the **Libary API** project locally:

### 1. Clone the repository

```bash
git clone https://github.com/StenSOn27/drf_practice_project.git
cd drf_practice_project
```

2. Create and activate a virtual environment

```
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```
4. Apply database migrations
```
python manage.py migrate
```
5. Create a superuser (admin)
```
python manage.py createsuperuser
```
6. Run the development server
```
python manage.py runserver
```
7. Access the API

    The API will be available at ```http://127.0.0.1:8000/```

    Admin panel: ```http://127.0.0.1:8000/admin/```