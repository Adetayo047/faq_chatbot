# FAQ Chatbot API

## Overview
This is a FastAPI-based chatbot API that leverages Hugging Face sentence embeddings and OpenAI's GPT to provide answers to frequently asked questions (FAQ). It includes CORS support and utilizes LangChain for embedding-based retrieval.

## Features
- **FastAPI Backend**: Lightweight and high-performance API framework.
- **Hugging Face Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` for semantic search.
- **OpenAI GPT Integration**: Enhances responses based on FAQ embeddings.
- **CORS Support**: Allows cross-origin requests for flexibility.

## Requirements
Ensure you have the following installed:
- Python 3.7+
- FastAPI
- Uvicorn
- LangChain
- Hugging Face Transformers
- OpenAI Python SDK
- Python-dotenv

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/faq-chatbot-api.git
   cd faq-chatbot-api
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```sh
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the API
Start the FastAPI server using Uvicorn:
```sh
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```
The API will be available at `http://localhost:8002`.

## API Endpoints
### Root Endpoint
**Endpoint:**
```
GET /
```
**Response:**
```json
{
  "API": "FAQ"
}
```

### FAQ Query Endpoint
**Endpoint:**
```
POST /Osun_FAQ
```
**Request Body:**
```json
{
  "user_id": "12345",
  "prompt": "What are the services available?"
}
```
**Response:**
```json
{
  "response": "Here are the available services..."
}
```

## Deployment
To deploy the API, you can use services like AWS, Google Cloud, Heroku, or Docker.

Example using Docker:
1. Build the Docker image:
   ```sh
   docker build -t faq-api .
   ```
2. Run the container:
   ```sh
   docker run -p 8002:8002 faq-api
   ```

## License
This project is licensed under the MIT License.

