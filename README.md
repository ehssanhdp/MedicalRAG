# Medical Q&A Retrieval-Augmented Generation (RAG) System

This repository contains a **Retrieval-Augmented Generation (RAG) system** designed for answering **medical-related inquiries**. The system leverages a **vector database (Pinecone)** to store and retrieve relevant medical Q&A pairs and utilizes an **LLM (Groq API)** to generate responses based on the retrieved context.

## Features
- **Retrieval-Based Approach**: Uses Pinecone for efficient vector search.
- **LLM Integration**: Calls the Groq API to generate responses.
- **Structured Codebase**: Settings and environment configurations are managed using Pydantic.
- **Efficient Query Processing**: Retrieves the most relevant documents before synthesizing a final response.

## Project Structure
```
├── settings.py          # Manages environment variables using Pydantic
├── vector_store.py      # Handles embedding storage and retrieval via Pinecone
├── llm.py              # Interacts with Groq API to generate responses
├── synthesizer.py       # Synthesizes final answers from retrieved context
├── main.py             # Entry point to process user queries
├── requirements.txt    # List of required dependencies
├── example.env       # Example environment variables file
└── README.md           # Project documentation
```

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/medical-qa-rag.git
cd medical-qa-rag
```

### 2. Create a Virtual Environment (Optional)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file and define the following variables:
```sh
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
PINECONE_HOST=your_pinecone_host_address
HUGGINGFACE_API_KEY=your_hugginface_api_key
```

### 5. Run the Application
```sh
python main.py
```

## How It Works
1. **User Query**: A user provides a medical question.
2. **Vector Search**: The system retrieves the most relevant Q&A pairs from Pinecone.
3. **LLM Generation**: The Groq API generates a response based on retrieved documents.
4. **Response Synthesis**: The system refines and returns the final answer.

## Future Improvements
- Improve ranking of retrieved documents.
- Add support for multiple LLMs.
- Optimize embeddings for better retrieval accuracy.
- building a chat UI and chat history for LLM

## License
This project is open-source under the **MIT License**.


