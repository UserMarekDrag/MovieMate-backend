# MovieMade
MovieMade is a web application for managing and organizing movie collections. The project is divided into separate repositories for the backend and frontend components, utilizing Python, Django, PostgreSQL for the backend, and React for the frontend.

## Backend Repository
The backend repository contains the server-side code for the MovieMade application. It uses Python and Django to handle API requests and communicate with the PostgreSQL database.

### Prerequisites
Before running the backend, make sure you have the following installed:

- Docker
- Docker Compose

### Installation
To install the backend:

1. Clone the backend repository to your local machine.
2. Navigate to the backend directory.
3. Build the Docker image for the backend using docker-compose build.
4. Start the Docker container using docker-compose up.
5. The backend API will now be running at http://localhost:8000/.

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