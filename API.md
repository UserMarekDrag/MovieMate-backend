# MovieMate API Endpoints

## Movie API

### GET /api-movie/

Listing API endpoints.

**Status Codes:**
- 200 OK –

### GET /api-movie/cinemas_in_city/

API endpoint for listing shows based on filters.

**Query Parameters:**
- cinema__city (string) –
- date (string) –

**Status Codes:**
- 200 OK –

**Response JSON Object:**
- [].booking_link (string) – (required)
- [].cinema.city (string) – (required)
- [].cinema.name (string) – (required)
- [].date (string) – (required)
- [].movie.category (string) –
- [].movie.description (string) –
- [].movie.image_url (string) –
- [].movie.title (string) – (required)
- [].time (string) – (required)

### POST /api-movie/movie-create/

Creates a new movie.

**Request JSON Object:**
- city (string) – (required)
- created_date (string) – (read only)
- id (integer) – (read only)
- showing_date (string) – (required)
- user (integer) – (read only)

**Status Codes:**
- 201 Created –

**Response JSON Object:**
- city (string) – (required)
- created_date (string) – (read only)
- id (integer) – (read only)
- showing_date (string) – (required)
- user (integer) – (read only)

### DELETE /api-movie/movie-delete/{id}/

Deletes a movie.

**Parameters:**
- id (integer) – A unique integer value identifying this search history.

**Status Codes:**
- 204 No Content –

### GET /api-movie/movie-detail/{id}/

Returns details of a specific movie.

**Parameters:**
- id (integer) – A unique integer value identifying this search history.

**Status Codes:**
- 200 OK –

**Response JSON Object:**
- city (string) – (required)
- created_date (string) – (read only)
- id (integer) – (read only)
- showing_date (string) – (required)
- user (integer) – (read only)

### GET /api-movie/movie-list/

Returns a list of movie searches.

**Status Codes:**
- 200 OK –

**Response JSON Object:**
- [].city (string) – (required)
- [].created_date (string) – (read only)
- [].id (integer) – (read only)
- [].showing_date (string) – (required)
- [].user (integer) – (read only)

### PUT /api-movie/movie-update/{id}/

Updates an existing movie.

**Parameters:**
- id (integer) – A unique integer value identifying this search history.

**Request JSON Object:**
- city (string) – (required)
- created_date (string) – (read only)
- id (integer) – (read only)
- showing_date (string) – (required)
- user (integer) – (read only)

**Status Codes:**
- 200 OK –

**Response JSON Object:**
- city (string) – (required)
- created_date (string) – (read only)
- id (integer) – (read only)
- showing_date (string) – (required)
- user (integer) – (read only)

### PATCH /api-movie/movie-update/{id}/

Updates an existing movie.

**Parameters:**
- id (integer) – A unique integer value identifying this search history.

**Request JSON Object:**
- city (string) – (required)
- created_date (string) – (read only)
- id (integer) – (read only)
- showing_date (string) – (required)
- user (integer) – (read only)

**Status Codes:**
- 200 OK –

**Response JSON Object:**
- city (string) – (required)
- created_date (string) – (read only)
- id (integer) – (read only)
- showing_date (string) – (required)
- user (integer) – (read only)

## User API

### POST /api-user/login/

Handles user login POST request.

**Status Codes:**
- 201 Created –

### POST /api-user/logout/

Handles user logout POST request.

**Status Codes:**
- 201 Created –

### POST /api-user/register/

Handles user registration POST request.

**Status Codes:**
- 201 Created –

### GET /api-user/user/

Handles GET request to retrieve user information.

**Status Codes:**
- 200 OK –
