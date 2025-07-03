# Order Detail Service

This service provides a GraphQL API to fetch details for a specific order. It aggregates information from an Order Creation service and an Order Status service.

## Folder Structure

Here's an overview of the main folders and their purpose:

-   `.github/workflows/`: Contains GitHub Actions workflow configurations.
    -   `docker-publish.yml`: Defines the CI/CD pipeline for building, testing, publishing the Docker image, and deploying to EC2.
-   `app/`: The core application code.
    -   `services/`: Contains business logic.
        -   `order_detail_service.py`: Fetches and aggregates order data from external services.
    -   `types/`: Defines GraphQL types.
        -   `order_type.py`: Defines the `OrderDetailType` and `OrderItemType` for the GraphQL schema.
    -   `config.py`: Handles application configuration, primarily loading external service URLs from environment variables.
    -   `schema.py`: Defines the GraphQL schema, including queries and resolvers that use the `OrderDetailService`.
    -   `__init__.py`: Makes the `app` directory a Python package.
-   `tests/`: Contains automated tests.
    -   `functional/`: Functional tests that test the GraphQL API endpoint.
        -   `test_graphql_order_detail.py`: Tests the `orderDetail` query.
    -   `unit/`: Unit tests for individual components.
        -   `test_order_detail_service.py`: Tests the `OrderDetailService` in isolation.
    -   `conftest.py`: Pytest configuration and fixtures, like the Flask test client.
-   `Dockerfile`: Instructions to build the Docker image for the application.
-   `requirements.txt`: Lists Python dependencies for the project.
-   `run.py`: The entry point to run the Flask application.
-   `.gitignore`: Specifies intentionally untracked files that Git should ignore.

## Backend Design and Architecture

### Backend Pattern

The application utilizes a **Service Layer** pattern. The `OrderDetailService` (`app/services/order_detail_service.py`) encapsulates the core business logic of fetching and combining data from external sources. This keeps the GraphQL resolvers in `app/schema.py` clean and focused on request handling and data presentation.

### Communication Architecture

-   **API Exposure**: The service exposes a **GraphQL API** endpoint (`/graphql`) for clients to query order details. This allows clients to request exactly the data they need.
-   **Inter-Service Communication**: For fetching underlying order data and status, this service communicates with other backend services (presumably microservices) via **RESTful HTTP GET requests**.
    -   An "Order Creation Service" is queried for basic order details.
    -   An "Order Status Service" is queried for the current status of the order.
    This indicates that the application is part of a larger microservices ecosystem.

### Folder Pattern

The project primarily follows a **layer-based** folder structure within the `app/` directory:
-   `app/types/`: Contains GraphQL type definitions (presentation layer).
-   `app/services/`: Contains business logic (service layer).
-   `app/schema.py`: Defines the GraphQL schema and resolvers (API/controller layer).
-   `app/config.py`: Handles configuration (infrastructure layer).

## Running the Code

### Prerequisites

-   Python 3.10 or higher
-   `pip` (Python package installer)
-   Docker (optional, for running in a container)
-   Access to the Order Creation and Order Status services.

### Environment Variables

The application requires the following environment variables to be set:

-   `ORDER_CREATION_URL`: The base URL for the Order Creation service (e.g., `http://localhost:5001/orders`). The service will append `/{order_id}` to this URL.
-   `ORDER_STATUS_URL`: The base URL for the Order Status service (e.g., `http://localhost:5002/status`). The service will append `/{order_id}` to this URL.

You can set these variables in your shell, or create a `.env` file in the project root directory. The `app/config.py` uses `python-dotenv` to load these variables automatically if the file exists.

Example `.env` file:
```
ORDER_CREATION_URL="http://order-creation-service.example.com/api/orders"
ORDER_STATUS_URL="http://order-status-service.example.com/api/status"
```

### Local Development (using Python directly)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DaYascaribay/PF_order_detail.git
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Environment Variables:**
    Ensure `ORDER_CREATION_URL` and `ORDER_STATUS_URL` are set in your environment or in a `.env` file.

4.  **Run the application:**
    ```bash
    python run.py
    ```
    The application will start on `http://0.0.0.0:1015`.
    The GraphQL interface (GraphiQL) will be available at `http://localhost:1015/graphql`.

## API Usage Example

The service exposes a GraphQL endpoint at `/graphql`. You can use tools like GraphiQL (available at `http://localhost:1015/graphql` when running locally) or Postman to send queries.

### Query for Order Details

To get details for an order, use the `orderDetail` query with an `orderId`:

```graphql
query GetOrderDetails {
  orderDetail(orderId: 1) {
    orderId
    userId
    total
    orderDate
    status
    items {
      productId
      quantity
      price
    }
  }
}
```

### Example Response

If the order exists and the dependent services respond successfully, you'll receive a JSON response like this (based on the example in `tests/functional/test_graphql_order_detail.py`):

```json
{
  "data": {
    "orderDetail": {
      "orderId": 1,
      "userId": 10,
      "total": 99.99,
      "orderDate": "2025-07-03T10:00:00Z",
      "status": "PAID",
      "items": [
        {
          "productId": 1,
          "quantity": 2,
          "price": 49.99
        }
      ]
    }
  }
}
```

If the order is not found (HTTP 404 from Order Creation service) or an internal error occurs, the GraphQL response will include an `errors` array:

```json
{
  "errors": [
    {
      "message": "Orden no encontrada", // Or "Error interno al obtener detalle de orden"
      "locations": [
        {
          "line": 2, // Example line number, may vary based on query
          "column": 3 // Example column number, may vary
        }
      ],
      "path": [
        "orderDetail"
      ]
    }
  ],
  "data": {
    "orderDetail": null
  }
}
```

## Testing

The project uses `pytest` for both unit and functional tests. The tests are located in the `tests/` directory, with subdirectories for `unit` and `functional` tests.

1.  **Ensure Dependencies are Installed:**
    Make sure all development dependencies, including `pytest` and `requests-mock`, are installed. If you've installed from `requirements.txt`, these should be present. You might need to install `requests-mock` separately if it's not in `requirements.txt` (though it is used by the tests and ideally should be).
    ```bash
    pip install -r requirements.txt
    pip install pytest requests-mock # If not already included or for explicitness
    ```

2.  **Set PYTHONPATH (if necessary):**
    In some environments, or if not using a virtual environment where the project is installed correctly, you might need to set the `PYTHONPATH` for `pytest` to find the `app` module.
    ```bash
    export PYTHONPATH=$(pwd) # For Linux/macOS
    # For Windows (Command Prompt): set PYTHONPATH=%cd%
    # For Windows (PowerShell): $env:PYTHONPATH = (Get-Location).Path
    ```
    The GitHub Actions workflow also sets this for CI.

3.  **Running Tests:**
    Navigate to the project's root directory in your terminal.
    Execute the following command:
    ```bash
    pytest
    ```
    Pytest will automatically discover and run all test files (conventionally `test_*.py` or `*_test.py`) within the `tests` directory and its subdirectories.
    The functional tests (e.g., `tests/functional/test_graphql_order_detail.py`) use `requests-mock` to simulate responses from the external Order Creation and Order Status services, allowing the GraphQL endpoint to be tested in isolation without actual external calls during testing.

## CI/CD

This project uses GitHub Actions for its Continuous Integration and Continuous Deployment (CI/CD) pipeline, defined in `.github/workflows/docker-publish.yml`.

The workflow is triggered on:
-   Pushes to the `QA` branch.
-   Manual dispatch (`workflow_dispatch`).

Key stages in the pipeline:

1.  **Run Unit and Functional Tests (`run-tests` job):**
    -   Checks out the repository.
    -   Sets up Python 3.10.
    -   Installs dependencies from `requirements.txt` along with `pytest` and `requests-mock`.
    -   Sets the `PYTHONPATH`.
    -   Runs `pytest` to execute all tests.

2.  **Build and Push Docker Image (`build-and-push` job):**
    -   Depends on the successful completion of the `run-tests` job.
    -   Checks out the repository.
    -   Sets up Docker Buildx.
    -   Logs into Docker Hub using secrets.
    -   Builds the Docker image using the `Dockerfile` in the project root.
    -   Pushes the image to Docker Hub, tagged appropriately (e.g., with the branch name or commit SHA).
    -   Signs the published Docker image using `cosign`.

3.  **Deploy to EC2 (`deploy-to-ec2` job):**
    -   Depends on the successful completion of the `build-and-push` job.
    -   Uses SSH to connect to an EC2 instance (credentials and host stored in secrets).
    -   Pulls the newly built Docker image from Docker Hub.
    -   Stops and removes any existing container named `order_detail`.
    -   Runs the new Docker image as a container named `order_detail`, exposing port `1015`.
    -   Passes `ORDER_STATUS_URL` and `ORDER_CREATION_URL` as environment variables to the container (values sourced from GitHub secrets).
    -   Sets the container to restart `unless-stopped`.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

© 2025 David Yascaribay
