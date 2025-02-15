
# Inspiration Board API

A Flask-based RESTful API for managing inspiration boards and cards.
You can access the deployed project [here](https://inspiration-board-app-frontend-62f20317cc28.herokuapp.com/).

## Features

- **Board Management:** Create, read, update, and delete boards.
- **Card Management:** Create, read, update, and delete cards associated with specific boards.
- **Database Support:** PostgreSQL database with SQLAlchemy ORM.
- **Migrations:** Manage database migrations seamlessly using Alembic.
- **Slack Integration:** Send notifications to a Slack channel when actions are performed on tasks/cards.

## Technologies Used

### Backend

- **[Flask](https://flask.palletsprojects.com/):** A lightweight WSGI web application framework.
- **[SQLAlchemy](https://www.sqlalchemy.org/):** An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **[Alembic](https://alembic.sqlalchemy.org/):** A lightweight database migration tool for SQLAlchemy.
- **[PostgreSQL](https://www.postgresql.org/):** An open-source, powerful, and advanced object-relational database system.

### Continuous Integration

This project includes a simple CI pipeline using GitHub Actions to automate testing.

On every push or pull request to the main branch, the pipeline:
1.	Sets up Python 3.12.
2.	Installs dependencies listed in requirements.txt.
3.	Runs the test suite with pytest.

The workflow ensures the codebase remains robust and reliable by automatically executing all tests before changes are merged.

### Testing

- **[Pytest](https://docs.pytest.org/):** A framework that makes building simple and scalable test cases easy.
- **Test Suite Overview:**
   - Route validation tests
   - Database operation tests 
   - Error handling tests
   - Response format validation

 - **Test Categories Implemented:**
   #### Route Validation
   - HTTP methods (GET, POST, PUT/PATCH, DELETE)
   - Invalid URL parameter handling
   - 404 handling for non-existent resources

   #### Database Operations  
   - CRUD operations for boards/cards
   - Board-card relationships
   - Transaction handling (commit/rollback)

   #### Error Handling
   - 404 responses for missing resources 
   - Missing field validation
   - Status code verification (200, 201, 400, 404)

   #### API Response Formatting
   - JSON structure validation
   - Data type verification
   - Response status code checks

 - **Test Infrastructure:**
   - Custom fixtures for database setup
   - Test client configuration
   - Sample data generation

### Deployment

- **[Heroku](https://www.heroku.com/):** Cloud platform as a service (PaaS) supporting several programming languages.

### Additional Libraries

- **Flask-CORS:** Manage Cross-Origin Resource Sharing (CORS) for the API.
- **Python-dotenv:** Manage environment variables using a `.env` file.
- **Gunicorn:** Python WSGI HTTP server for running Flask applications.

## Project Structure

```
back-end-inspiration-board/
│
├── app/
│   ├── __init__.py             # Application factory and setup
│   ├── models/                 # SQLAlchemy models for Board and Card
│   │   ├── base.py             
|   |   ├── board.py            
│   │   └── card.py             
│   ├── routes/                 # API route definitions
│   │   ├── board_routes.py     
│   │   ├── card_routes.py      
|   |   └── route_utilities.py  # File with reusable route helper functions
│   └── db.py                   # Database connection setup
│
├── migrations/                 # Alembic migrations directory
├── tests/                      # Pytest test cases
|   ├── conftest.py             # Pytest configuration file
│   ├── test_board_routes.py
│   ├── test_card_routes.py
|   └── test_setup.py
│
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Specifies Python runtime version for Heroku
├── Procfile                    # Specifies commands to run the app on Heroku
└── README.md                   # Project documentation
```

## API Endpoints

### Boards

| Method | Endpoint          | Description                  |
|--------|--------------------|------------------------------|
| GET    | `/boards`         | Retrieve all boards          |
| POST   | `/boards`         | Create a new board           |
| GET    | `/boards/<id>`    | Retrieve a specific board    |
| PUT    | `/boards/<id>`    | Update a specific board      |
| DELETE | `/boards/<id>`    | Delete a specific board      |

### Cards

| Method | Endpoint                        | Description                          |
|--------|----------------------------------|--------------------------------------|
| GET    | `/boards/<board_id>/cards`      | Retrieve all cards for a board       |
| POST   | `/boards/<board_id>/cards`      | Add a new card to a specific board   |
| GET    | `/cards/<card_id>`              | Retrieve a specific card             |
| PATCH  | `/cards/<card_id>`              | Update a specific card               |
| DELETE | `/cards/<card_id>`              | Delete a specific card               |
| PATCH  | `/cards/like/<card_id>`         | Increments like count for a card by one|

## Setup Instructions

### Prerequisites

- Python 3.12+
- PostgreSQL

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Nerpassevera/back-end-inspiration-board.git
    cd back-end-inspiration-board
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts activate     # On Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file:
    ```bash
    touch .env
    ```

    Add the following:
    ```
    SQLALCHEMY_DATABASE_URI=<your_database_url>
    SLACK_API_KEY=<your_slack_api_key>
    ```

5. Run database migrations:
    ```bash
    flask db upgrade
    ```

6. Start the development server:
    ```bash
    flask run
    ```

7. Run tests:
    ```bash
    pytest
    ```

## Contributing

This project is built for educational purposes, and contributions are always welcome! Whether you want to enhance the features, fix bugs, or simply learn and explore, feel free to fork the repository, make changes, and open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
