# AI-Powered-Stock-Prediction-Platform
# How to Run This Project
This document provides the necessary steps to set up and run the project. Please follow the instructions carefully to ensure everything works smoothly.


## Configuration

1. Modify the `secret.yml` file in the project root:
   - Open [secret.yml](./secret.yml)
   - Replace the default token with your OpenAI API key.

## Running the Project

After setting up your environment and configuring the necessary files, you can start the project using the following commands:

1. Install project dependencies:
   ```bash
   poetry install
   ```
2. To generate the vector store:
   ```bash
   poetry run python3 rag_demo/vector_store_generator.py
   ```
3. To start the unified API server:
   ```bash
   poetry run python3 unified_api/unified_api_server.py
   ```
Ensure you execute these commands from the root of the project directory where the pyproject.toml file is located.



>>>>>>> 8cf0407 (Initial commit with Docker setup)
