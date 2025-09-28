AI-Powered Database Schema Optimizer
An intelligent system that ingests natural-language descriptions of data and business rules and generates a complete, optimized, and normalized SQL database schema. This project leverages a powerful generative AI to understand complex requirements and translate them into a concrete, ready-to-use DDL (Data Definition Language) script.
Features
 * Natural Language Processing: Directly converts plain English sentences into a structured database plan.
 * Schema Synthesis: Automatically generates CREATE TABLE statements for all identified entities and their attributes.
 * Relationship Modeling: Correctly infers one-to-many (1:N) and many-to-many (N:M) relationships, generating foreign keys and junction tables as needed.
 * AI-Powered: Uses Google's Gemini model for state-of-the-art language understanding, ensuring high accuracy.
 * API-Driven: The entire workflow is exposed via a clean, modern FastAPI application.
 * Containerized: The complete application and its database dependency are managed by Docker and Docker Compose for easy, one-command setup.
Tech Stack & Architecture
 * Backend: Python 3.11+ with FastAPI
 * AI / NLP: Google Generative AI (Gemini 1.5 Flash)
 * Containerization: Docker & Docker Compose
 * Database (Sandbox): PostgreSQL
The system is designed as a single API service that receives a request, communicates with the Google AI API to create a structured plan, and then uses that plan to generate the final SQL schema.
Getting Started
Follow these steps to get the project running on your local machine.
Prerequisites
 * Docker Desktop: Make sure it is installed and running on your system.
 * Google AI API Key: You need a valid API key from Google AI Studio.
Installation & Setup
 * Clone the Repository
   git clone <your-repository-url>
cd ai-db-optimizer

 * Create the Environment File
   Create a file named .env in the root of the project directory and add your API key:
   GOOGLE_API_KEY=PASTE_YOUR_API_KEY_HERE

   Note: Remember to add .env to your .gitignore file to protect your key.
 * Build and Run the Application
   From the root of the project directory, run the following command:
   docker compose up --build

   This will build the Docker image, download all dependencies, and start the API and database containers.
 * Verify Setup
   Once the containers are running, open your web browser and navigate to http://localhost:8000/docs. You should see the FastAPI interactive documentation.
Usage
The primary way to use the application is through the /process endpoint. This endpoint handles the entire workflow from text to SQL in a single call.
Example Request
You can use the interactive documentation or a tool like cURL to send a request.
Endpoint: POST /process
Request Body:
{
  "text": "A Customer places many Orders. An Order can contain many Products, and a Product can be in many Orders. A Product has a name and a price."
}

Example Successful Response
A successful request will return a 200 OK status with the complete DDL bundle in the response body:
{
  "tables": [
    "CREATE TABLE customers (\n    id SERIAL PRIMARY KEY\n);",
    "CREATE TABLE orders (\n    id SERIAL PRIMARY KEY\n);",
    "CREATE TABLE products (\n    id SERIAL PRIMARY KEY,\n    name VARCHAR(255),\n    price DECIMAL(10, 2)\n);"
  ],
  "junctions": [
    "CREATE TABLE order_products (\n    order_id INTEGER REFERENCES orders(id),\n    product_id INTEGER REFERENCES products(id),\n    PRIMARY KEY (order_id, product_id)\n);"
  ],
  "foreign_keys": [
    "ALTER TABLE orders ADD COLUMN customer_id INTEGER REFERENCES customers(id);"
  ],
  "plan_id": "plan_..."
}

Future Work
This project has successfully implemented the core AI and schema generation logic. The next steps to expand it into a fully production-ready system would include:
 * Schema Execution: Implementing an endpoint (/schema/apply) to safely execute the generated DDL against a target database.
 * Query & Index Generation: Building the logic to automatically generate sample CRUD queries and recommend optimal database indexes.
 * Advanced Migrations: Adding support for generating safe migration scripts to alter an existing database schema based on new requirements.
