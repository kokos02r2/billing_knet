# Billing KNet

## Project Description

Billing KNet is a billing management system developed in Django. It provides an API and web interface for managing tariffs, calculations, and user payments.

### Key Features:

- User and tariff management
- Automatic calculation and recalculation of service costs
- Invoice and notification generation
- Integration with payment systems
- API for interaction with external services

## Installation and Setup

### Requirements

- Python 3.9+
- PostgreSQL
- Poetry (for dependency management)

### Installation

1. Clone the repository:

   ```bash
   git clone <repository>
   cd billing_knet-main
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Configure environment variables (can use a `.env` file):

   ```
   DATABASE_URL=postgres://user:password@localhost:5432/billing_db
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

4. Apply database migrations:

   ```bash
   poetry run python billing/manage.py migrate
   ```

5. Create a superuser:

   ```bash
   poetry run python billing/manage.py createsuperuser
   ```

6. Populate the database with test data (if required):
   ```bash
   poetry run python billing/manage.py loaddata initial_data.json
   ```

## Running the Project

1. Start the development server:

   ```bash
   poetry run python billing/manage.py runserver
   ```

2. Open the application at `http://127.0.0.1:8000/`.

## API

### Main Endpoints:

- **Authentication:** `/api/auth/login/`, `/api/auth/logout/`
- **Users:** `/api/users/` – user management
- **Tariffs:** `/api/tariffs/` – tariff management
- **Invoices:** `/api/bills/` – payment and invoice information

The API supports authentication via JWT tokens. To obtain a token, run:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ -d '{"username": "admin", "password": "admin"}' -H "Content-Type: application/json"
```

## Usage

- Admin Panel: `http://127.0.0.1:8000/admin/`
- API Documentation: `http://127.0.0.1:8000/api/docs/` (if Swagger is enabled)

## Project Structure

```
billing_knet-main/
│── billing/
│   ├── manage.py        # Django entry point
│   ├── core/            # Main module
│   │   ├── settings.py  # Django settings
│   │   ├── urls.py      # Routing
│   │   ├── views.py     # Views
│   │   ├── helpers/     # Helper modules
│   │   ├── tests/       # Tests
│── poetry.lock          # Project dependencies
│── pyproject.toml       # Poetry configuration
│── setup.cfg            # Package configuration
│── .gitignore           # Ignored files
```

## Testing

To run tests, execute:

```bash
poetry run python billing/manage.py test
```

## Deployment

### Running with Gunicorn and Nginx

1. Install Gunicorn:
   ```bash
   poetry add gunicorn
   ```
2. Start the Gunicorn server:
   ```bash
   poetry run gunicorn billing.core.wsgi:application --bind 0.0.0.0:8000
   ```
3. Configure Nginx to proxy requests to Gunicorn.

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t billing_knet .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env billing_knet
   ```

## Support and Development

If you have any questions or suggestions, create an issue in the repository or contact the developer.

## License

This project is distributed under the MIT License.
