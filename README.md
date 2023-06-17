# MovieMade
Welcome to MovieMate, a one-stop solution for movie enthusiasts in Poland. MovieMate offers an interface where users can select their city and date to view all available movie showtimes, along with links for reservations. By scraping data daily from the websites of two of the largest cinemas in Poland, Multikino and Helios, we keep our information up-to-date and comprehensive. More cinemas will be added over time as we continue to expand the functionality of our site.


### Features

- Movie Showtimes: Users can enter their city and date to view all movie showtimes from all cinemas in that city. The application provides detailed information about each showtime and includes links for additional details.

- Data Scraping: The application utilizes Python scripts with BeautifulSoup (bs4) and Selenium to scrape data. Once a day, the scraper executes tasks using RabbitMQ and Celery, gathering showtime information for all cities, cinemas, and corresponding dates. The data is then saved into the application's models.

- API Management: The movie_api module manages the API views using Django Rest Framework (DRF) and the filter module to process requests from the frontend. It ensures the appropriate data is passed to the frontend queries and records information about the retrieved data for analysis and further application development.

- User Management: The user_api module handles user and superuser creation. It enables the addition of new features as the application evolves.

### Backend Repository
The backend repository contains the server-side code for the MovieMade application. It uses Python and Django to handle API requests and communicate with the PostgreSQL database.

### Prerequisites
Before running the backend, make sure you have the following installed:

- Docker
- Docker Compose

### Installation
MovieMate is designed to run on Docker and docker-compose, allowing for easy setup and deployment. Follow these steps to get it up and running:

1. Clone the repository:
```bash
git clone https://github.com/UserMarekDrag/MovieMate-backend.git
```
2. Navigate to the directory.
```bash
cd moviemate
```
3. Build and start the Docker services:
```bash
docker-compose build
docker-compose up
```
4. The backend API will now be running at http://localhost:8000/.

### Database Schema

![Database Schema](moviemate_visualized.png)

To generate a new database schema visualization, you can use the `django-extensions`'s `graph_models` command:

```bash
python manage.py graph_models -a -g -o moviemate_visualized.png
```

### Documentation

To generate the documentation for the project, navigate to the docs folder and run:

```bash
sphinx-build -b html ./source build/
```
The HTML files for the documentation will be in the build directory.

### Testing

We use coverage to run unit tests and check the code coverage of our tests. To run the tests, use:

```bash
coverage run --source='.' manage.py test
```
Current test coverage is as follows:
Total coverage: 91%.

### Code Quality

We use pylint to maintain the quality of our code. To check the code with pylint, use:

```bash
pylint module_name
```
Current Pylint ratings are:

- moviemate module: 10.00/10
- scraper module: 10.00/10
- movie_api module: 10.00/10
- user_api module: 10.00/10

### API Endpoints
Our API allows you to interact with MovieMate in a programmatic way. Please check [API.md](API.md) for more details about the available endpoints.

### Frontend Repository
The frontend repository contains the client-side code for the MovieMade application. It uses React to build the user interface.

For instructions on setting up and running the frontend, please refer to the [MovieMate-frontend repository](https://github.com/UserMarekDrag/MovieMate-frontend).

### License
The MovieMade project is open-source and released under the MIT License. Feel free to use, modify, and distribute the code as per the terms of the license.

### Contact
If you have any questions or issues with the MovieMade project, please contact the project maintainers or create an issue in the respective repositories.

Happy movie managing with MovieMade! 🎥🍿🎞️

## Author 
Marek Drąg