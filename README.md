# OMNI-PMS-BACKEND API

This is the backend api for OMNI-PMS-SYSTEM

### Follow the instructions below to run the project.

Clone the repository to your local machine:
shell

```
git clone <repository_url>

```

Change into the project directory:
shell

```
cd <project_directory>

```

Create a virtual environment (Recommended):
shell

```
python -m venv env

```

Activate the virtual environment:

For Windows:
shell

```
env\Scripts\activate

```

For macOS/Linux:
shell

```
source env/bin/activate

```

Install the required packages from the requirements.txt file:
shell

```
pip install -r requirements.txt

```

Run database migrations:
shell

```
python manage.py migrate

```

Start the development server:
shell

```
python manage.py runserver

 ```

Access the API endpoints and explore the documentation:
API endpoints: http://localhost:8000/api/
Obtain JWT token: http://localhost:8000/api/token/
Refresh JWT token: http://localhost:8000/api/token/refresh/
API documentation (Swagger UI): http://localhost:8000/api/docs/
API documentation (Redoc): http://localhost:8000/api/redoc/

That's it! You have successfully set up and started the Django backend API. You can now interact with the API endpoints and explore the documentation using the provided URLs.

Please note that these instructions assume you have Python and Git installed on your machine. If not, make sure to install them before proceeding.

Certainly! Here are some instructions with URLs to the documentation of the most used libraries used in this project:

Django: A high-level Python web framework that makes it easy to build web applications. You can find the official documentation at: https://docs.djangoproject.com/

Django Rest Framework (DRF): A powerful and flexible toolkit for building Web APIs. You can find the official documentation at: https://www.django-rest-framework.org/

SimpleJWT: A JSON Web Token (JWT) implementation for Django REST Framework. You can find the documentation and usage examples at: https://django-rest-framework-simplejwt.readthedocs.io/

DRF-YASG: Yet Another Swagger Generator for Django REST Framework. It generates OpenAPI (formerly Swagger) specifications from Django Rest Framework code. You can find the documentation and usage examples at: https://drf-yasg.readthedocs.io/

Feel free to visit these URLs to learn more about each library, including their features, usage, and examples. The documentation will provide you with detailed explanations and code samples to help you understand and utilize these libraries effectively in your Django backend API.


change from Anoe