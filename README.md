# MovieMade
MovieMade is a web application for managing and organizing movie collections. The project is divided into separate repositories for the backend and frontend components, utilizing Python, Django, MySQL for the backend, and React for the frontend.

## Backend Repository
The backend repository contains the server-side code for the MovieMade application. It uses Python and Django to handle API requests and communicate with the MySQL database.

### Prerequisites
Before running the backend, make sure you have the following installed:

- Python (version 3.7+)
- Django (version 3.0+)
- MySQL (version 5.7+)

### Installation
To install the backend:

1. Clone the backend repository to your local machine.
2. Navigate to the backend directory.
3. Create and activate a virtual environment (optional but recommended).
4. Install the dependencies using pip install -r requirements.txt.
5. Set up the MySQL database with appropriate credentials in settings.py.
6. Run the migrations to create the necessary tables using python manage.py migrate.
7. Start the Django development server using python manage.py runserver.
8. The backend API will now be running at http://localhost:8000/.

### API Endpoints
The backend provides the following API endpoints for the frontend to interact with:

- /api/movies: CRUD operations for managing movies.
- /api/users: CRUD operations for managing users.

Make sure to refer to the backend's API documentation for detailed information on each endpoint, including request and response formats.

### Contributing
If you wish to contribute to the MovieMade project, please follow the guidelines in the CONTRIBUTING.md file in the respective repositories.

### License
The MovieMade project is open-source and released under the MIT License. Feel free to use, modify, and distribute the code as per the terms of the license.

### Contact
If you have any questions or issues with the MovieMade project, please contact the project maintainers or create an issue in the respective repositories.

Happy movie managing with MovieMade! 🎥🍿🎞️

## Author 
Marek Drąg