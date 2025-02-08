import os
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
import tensorflow as tf
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline

app = Flask(__name__)
api = Api(app)

# Suppress TensorFlow warnings
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Load the FAISS vector store 
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

HF_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
if not HF_TOKEN:
    raise ValueError("Hugging Face token not found in environment variable 'HF_TOKEN'.")

# Initialize the text-generation pipeline.
hf_pipeline = pipeline(
    "text-generation",
    model="gpt2-medium", 
    max_new_tokens=200   
)
llm = HuggingFacePipeline(pipeline=hf_pipeline)

@app.route('/')
def home():
    return "Flask server is running!"

class Chat(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or 'question' not in data:
                return make_response(jsonify({"error": "Missing 'question' parameter"}), 400)
            question = data['question']

            # Retrieve the top 3 relevant chunks from the vector store.
            docs = vector_store.similarity_search(question, k=3)
            # Convert each document's content to a plain string.
            context_lines = [str(doc.page_content) for doc in docs]
            context = "\n".join(context_lines)

    
            # The prompt instructs the model to synthesize the unorganized data into a coherent paragraph.
            prompt = (
    "You are an expert educational assistant. "
    "Below is unorganized raw data scraped from the Brainlox website that contains various course details. "
    "From this data, identify and list the top three best courses offered by Brainlox along with a brief description for each course. "
    "Ignore any unrelated or duplicate information and provide your answer in a numbered list, with each item on a new line.\n\n"
    "Raw Data:\n" + context + "\n\n"
    "Question: What are the best courses I can do from Brainlox?\n\n"
    "Answer:"
)

            print("DEBUG: Prompt sent to LLM:")
            print(prompt)

            # Generate the response.
            generated = llm(prompt)
            print("DEBUG: Raw generated output:")
            print(generated)

            # Process the generated output.
            if isinstance(generated, list) and generated and "generated_text" in generated[0]:
                full_text = str(generated[0]["generated_text"]).strip()
            elif isinstance(generated, str):
                full_text = generated.strip()
            else:
                full_text = str(generated)

            # Remove any echoed prompt (if present) by splitting at the "Answer:" marker.
            if "Answer:" in full_text:
                refined_answer = full_text.split("Answer:")[-1].strip()
            else:
                refined_answer = full_text

            # Return the final structured answer.
            return make_response(jsonify({"response": refined_answer}), 200)

        except Exception as e:
            print("Server error:", e)
            return make_response(jsonify({"error": str(e)}), 500)

api.add_resource(Chat, "/chat")

if __name__ == "__main__":
    app.run(debug=True)
