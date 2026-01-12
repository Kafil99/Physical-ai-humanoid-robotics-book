# Physical AI Humanoid Robotics Book

This repository contains the source code for the "Physical AI Humanoid Robotics Book", a Docusaurus-based website with an integrated RAG chatbot.

## Running the Application

To run the complete application, you need to run the backend server and the frontend development server in two separate terminals.

### 1. Backend Setup & Execution

First, ensure you have all the required environment variables set up in a `.env` file in the `backend` directory. These should include:
- `OPENROUTER_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `QDRANT_COLLECTION_NAME`
- `COHERE_API_KEY`

Next, install the dependencies and run the server:

```bash
# Navigate to the backend directory
cd backend

# (Optional, but recommended) Activate your Python virtual environment
# On Windows:
# .venv\Scripts\activate
# On macOS/Linux:
# source .venv/bin/activate

# Install/update Python dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload
```

The backend server will start on `http://localhost:8000`.

### 2. Frontend Execution

In a second terminal, run the Docusaurus development server:

```bash
# Navigate to the project root directory
# (If you are in the backend directory, navigate back)
# cd ..

# Install npm dependencies (if you haven't already)
npm install

# Start the Docusaurus development server
npm start
```

The frontend development server will start on `http://localhost:3000` and open in your browser.

### 3. Using the Chatbot

Navigate to your Docusaurus site in the browser. You should see a floating chat icon in the bottom right corner. Click it to open the chat window.

You can now ask questions in two ways:
1.  **Global Book RAG:** Simply type a question and hit send. The agent will search the entire book content for an answer.
2.  **Selected Text RAG:** Highlight any text on the page, then open the chat window and ask a question about the selection. The agent will only use the text you selected to answer.