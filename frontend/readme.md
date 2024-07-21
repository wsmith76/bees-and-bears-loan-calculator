# Loan Calculator

This is a single-page React application that calculates monthly loan payments based on user input for loan amount, interest rate, and loan term. The application supports both English and German languages.

## Table of Contents

- [Build and Run the Docker Image](#build-and-run-the-docker-image)
- [Run the Unit Tests](#run-the-unit-tests)
- [Use the Web Application](#use-the-web-application)

## Build and Run the Docker Image

### Prerequisites

- Ensure you have Docker installed on your system.

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/wsmith76/bees-and-bears-loan-calculator
   cd bees-and-bears-loan-calculator/frontend

2. **Build the docker image:**

   ```bash
   docker build -t loan_calculator_frontend .
   ```
3. **Run the Docker container on port 3000:**
    ```bash
    docker run -p 3000:3000 loan_calculator_frontend
   ```
The application will be accessible at http://localhost:3000.

## Run the Unit Tests

### Prerequisites

- Ensure you have Node.js and npm installed on your system.

### Steps
1. **Install the dependencies:**

```bash
npm install
```
2. **Run the unit tests:**

```bash
npm test
```
This will run the unit tests using Jest and display the results in the terminal.

## Use the Web Application

### Steps
1. **Open your web browser and navigate to http://localhost:3000.**

2. **Enter the loan details:**

- **Loan Amount (€):** Enter the total amount of the loan.
- **Annual Interest Rate (%):** Enter the annual interest rate (can be 0 or a positive number).
- **Loan Term (months):** Enter the loan term in months (must be a positive integer).

3. Click the "Berechnen" button (in German) or the "Calculate" button (in English) to calculate the monthly payment.

4. **View the results:**

The monthly payment will be displayed below the form.

### Switch the language:

Use the language toggle button in the upper right corner to switch between English and German.
