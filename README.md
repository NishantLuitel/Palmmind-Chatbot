# ChatBot Readme

## Description
This repository contains a question-answering chatbot implemented using the RAG (Retrieval-Augmented Generation) methodology. The chatbot utilizes langChain and Gemini-pro for its functioning. It specializes in answering questions related to cell biology, neurobiology, or any custom content provided in a PDF format. The model is designed to provide answers only if the retrieved passages from the specified sources can answer the query effectively. Additionally, the chatbot supports a conversational form if requested to do so.

## Implementation Details
1. **RAG Methodology**: The chatbot employs the RAG methodology for question answering, which combines retrieval-based techniques with generative capabilities to produce accurate and informative responses.
2. **langChain and Gemini-pro**: These libraries are utilized for various aspects of the chatbot's functionality, including text processing, retrieval, and generation.
3. **Specialization**: Users can prompt the model to specialize in answering questions related to cell biology, neurobiology, or provide custom content in a PDF format for the chatbot to process and answer questions from.
4. **Answer Verification**: The model is programmed to verify that the retrieved passages contain relevant information to answer the user's query effectively, ensuring the quality and accuracy of responses.
5. **Conversational Form**: Optionally, the chatbot can engage in conversational interactions with users upon request.

## Usage
To run the chatbot, follow these steps:
1. Clone this repository to your local machine.
2. Ensure you have Python installed.
3. Set up your Gemini-pro API key:
   - Obtain your Gemini-pro API key from the Gemini website.
   - Set the API key as an environment variable named `GOOGLE_API_KEY`.
4. Navigate to the repository directory.
5. Run the `run.py` file using Python. This will initiate the chatbot interface.
    ```
    python run.py
    ```

## File Structure
- `run.py`: This file initiates the chatbot interface.
- `chat_agent.py`: Contains the class implementation of the chat agent, including its methods and functionality.
- Other supporting files and dependencies.

## Contact
For any inquiries or issues regarding the chatbot, feel free to contact the repository owner.
