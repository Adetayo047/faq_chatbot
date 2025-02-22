import os
import json
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import openai


class OSUN_FAQ:
    def __init__(self, embedding):
        # Initialize Embedding
        self.embedding = embedding

        # Load Document in Chroma Vectorstore
        self.vectordb = Chroma(
            persist_directory="./data/OSUN_VECTOR_STORE",
            embedding_function=self.embedding,
        )
        self.create_users_directory()

    def create_users_directory(self):
        """Create directory for user conversation history if it doesn't exist."""
        self.directory = "./USERS/OSUN_USERS"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def load_history(self, user_id):
        """Load the conversation history for a user."""
        file_path = os.path.join(self.directory, f"{user_id}_conversation.json")

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                history = json.load(file)
        else:
            history = []  # If no history, start fresh
        return history

    def save_history(self, user_id, history):
        """Save the updated conversation history for a user."""
        file_path = os.path.join(self.directory, f"{user_id}_conversation.json")

        with open(file_path, "w") as file:
            json.dump(history, file)

    def system_prompt(self, document,user_name):
        SYSTEM_PROMPT = f"""
        You are an FAQ chatbot designed to assist users by answering questions about topic for Osun State. 
        Your responses must be based on the provided document `{document}`. Follow these rules:

        1. **Greeting:** 
        - Do NOT introduce yourself unless the user greets you first.
        - If greeted, respond with: "Hello! How can I assist you today?" or a suitable alternative.

        2. **Conversational Flow:** 
        - Ask ONLY one question at a time.
        - Wait for the user's response before proceeding.

        3. **Response Format:** 
        - Keep responses concise (max two lines).
        - Be direct and clear.

        4. **Personalization:** 
        - Tailor responses to match the user's query for a more natural interaction.

        5. **Knowledge Retrieval:** 
        - Retrieve answers strictly from `{document}`.
        - If an answer is not found, direct the user to the appropriate contact from the document.

        6. **Handling Missing Information:** 
        - If no relevant answer is found, respond with:
            "I'm unable to find that information. Please contact [support line/email] for assistance."
        """
        return SYSTEM_PROMPT

    def chat_function(self, message, user_id):
        # Load user's conversation history
        history = self.load_history(user_id)

        # Perform a similarity search for User Query
        query = self.vectordb.similarity_search(message, k=3)
        document = [doc.page_content for doc in query]

        # Generate the system prompt based on the retrieved document
        SYSTEM_PROMPT = self.system_prompt(document, user_id)

        # Append user message to history
        history.append({"role": "user", "content": message})

        # Create messages list for the OpenAI model
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

        try:
            # Get response from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use "gpt-3.5-turbo" for GPT-3.5
                messages=messages,
                max_tokens=1050,
                temperature=0.7,
                top_p=0.9,
            )
            # Extract the generated message
            assistant_message = response["choices"][0]["message"]["content"]

            # Append bot response to history
            history.append({"role": "assistant", "content": assistant_message})

            # Save updated history to the user's file
            self.save_history(user_id, history)

            return assistant_message
        except Exception as e:
            print(f"Error: {e}")
            return "I'm sorry, but I encountered an error while processing your request."



# # ✅ Step 1: Initialize the embedding model
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# # ✅ Step 2: Initialize the FAQ system
# faq = OSUN_FAQ(embedding_model)

# # ✅ Step 3: Test similarity search
# test_query = "Is the scheme voluntary or compulsory?"
# retrieved_docs = faq.vectordb.similarity_search(test_query, k=3)

# # ✅ Step 4: Print retrieved documents
# print("\n=== Similarity Search Results ===")
# for i, doc in enumerate(retrieved_docs, start=1):
#     print(f"\nDocument {i}:")
#     print(doc.page_content)