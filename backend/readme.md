# Loan Calculator API
## Overview
This is a Django-based RESTful API for managing customers and loan offers. The API supports the following endpoints:

* POST /api/customers: Create a new customer.
* GET /api/customers/{id}: Retrieve a customer by ID.
* POST /api/loanoffers: Create a new loan offer.
## Getting Started
### Prerequisites
* Docker

### Build and Run the Docker Image
* Clone the repository:

```bash
git clone https://github.com/wsmith76/bees-and-bears-loan-calculator
```
* Navigate to this directory
```bash
cd bees-and-bears-loan-calculator
cd backend 
```
* Build the Docker image:

```bash
docker build -t loan_calculator_backend .
```
* Run the Docker container:

```bash
docker run -p 8000:8000 loan_calculator_backend
```
The API will be accessible at http://localhost:8000.

## Running Unit Tests
Run the tests inside the Docker container:

```bash
docker run loan_calculator sh -c "python manage.py test"
```
This will execute all the unit tests defined in the Django project.

## Using the Endpoints
You can use either cURL or Postman to interact with the API.

### Using cURL
#### Create a new customer:

```bash
curl -X POST http://localhost:8000/api/customers -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "street": "Musterstraße",
    "house_number": "123",
    "postal_code": "12345",
    "city": "Musterstadt",
    "state": "Musterland",
    "phone_number": "555-1234",
    "email": "john@example.com"
}'
```
#### Retrieve a customer by ID:

```bash
curl -X GET http://localhost:8000/api/customers/1
```
#### Create a new loan offer:

```bash
curl -X POST http://localhost:8000/api/loanoffers -H "Content-Type: application/json" -d '{
    "customer_id": 1,
    "amount": 5000.00,
    "interest_rate": 5.5,
    "term_in_months": 36
}'
```
### Using Postman
#### Create a new customer:

Open Postman and create a new POST request.

- URL: http://localhost:8000/api/customers
- Headers: Content-Type: application/json
- Body (raw JSON):
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "street": "Musterstraße",
    "house_number": "123",
    "postal_code": "12345",
    "city": "Musterstadt",
    "state": "Musterland",
    "phone_number": "555-1234",
    "email": "john@example.com"
}
```
Click Send.

#### Retrieve a customer by ID:

Create a new GET request.
- URL: http://localhost:8000/api/customers/1

Click Send.
#### Create a new loan offer:

Create a new POST request.

- URL: http://localhost:8000/api/loanoffers
- Headers: Content-Type: application/json

Body (raw JSON):
```json
{
    "customer_id": 1,
    "amount": 5000.00,
    "interest_rate": 5.5,
    "term_in_months": 36
}
```
Click Send.

## Notes
- Ensure Docker is installed and running on your machine.
- You might need to adjust firewall or security settings if you're running the Docker container on a remote server.
- This setup is for development purposes only. 