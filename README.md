# Westeros Capital Group

Welcome! Please follow the instructions below to run the application.

![image](./app/kingdoms_of_westeros_by_keyser94_dd03kjv-414w-2x.jpg)

### Prerequisites

- Clone the repository

- Generate an API key from [OpenAI](https://platform.openai.com/settings/organization/api-keys) and add it to an .env file in your root directory as `OPENAI_API_KEY=<key>`.

- Make sure you have [Docker](https://docs.docker.com/engine/install/) installed and running.

### Build and Run

- Build the docker image by running: `docker build -t westeros .`

- Run the service via command: `docker run -p 8000:80 --env-file .env westeros`. This will run the server on port 8000 and make the api key you added to .env accessible.

- Access the FastAPI endpoints locally via the Swagger UI at: [http://localhost:8000/docs]()

- Enter a query string into the `laws/query` endpoint and click "Execute". Scroll to the Response body section to see the query, response, and citations.
