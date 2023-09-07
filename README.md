# FastAPI Consent Management Service

This is a FastAPI-based Consent Management Service that allows users to define consents, add or revoke consents for users, and check the consents granted by a user. The service is designed to be modular and supports different data persistence layers, with an initial implementation using an in-memory "database".

This is meant to be an example project for showing of skills in RESTAPI development.

## Features

- Create consents with optional expiration dates.
- Add consents to a user.
- Revoke consents from a user.
- Retrieve a user's consents.
- Check if a user has given specific consent.
- Modular code structure for easy extension.

## Getting Started

Follow these instructions to set up and run the FastAPI consent management service locally.

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Run locally

1. Clone this repository to your local machine:

   ```bash
    git clone https://github.com/TODO
    cd TODO
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```
This will start the server at http://localhost:8000.

Access the FastAPI Swagger documentation at http://localhost:8000/docs to interact with the API and test the endpoints.

### API Endpoints

    POST /consents/: Create a new consent.
    POST /users/{username}/consents/: Add a consent to a user.
    DELETE /users/{username}/consents/: Revoke a consent from a user.
    GET /users/{username}/consents/: Get a user's consents.
    GET /users/{username}/consents/{consent}: Check if user has given specific consent.

#### Manual usage of endpoints
You can use all of the GET endpoints from your browser.
All endpoints can also be used using CURL.
Here are a few examples:

##### Create a consent
```bash
curl -X POST "http://localhost:8000/consents/?consent_name=exampleconsent&seconds=60&days=0"
```
##### Add consent to user
```bash 
curl -X POST "http://localhost:8000/users/John/consents/exampleconsent"
```

##### Check if Consent is valid
```bash 
curl "http://localhost:8000/users/John/consents/exampleconsent"
```

##### Revoke Consent from a User
```bash 
curl -X DELETE "http://localhost:8000/users/John/consents/exampleconsent"
```


## Modifying Data Persistence

By default, the service uses an in-memory database for data storage. You can replace it with a different SQL database by adding a database adapter and replacing 
    databseAdapter = DBMockup()
in the main.py file with the new adapter. Use DBMockup from database_mockup as a template on what methods the new adapter needs.
 
## Testing

To run unit tests install pytest using pip then use the following command:

    pytest tests/

## Deployment

For deploying the FastAPI service in a production environment, please refer to the FastAPI deployment documentation.
