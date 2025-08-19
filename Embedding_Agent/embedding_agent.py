from uagents import Agent, Context, Model
import openai
import json
from sklearn.metrics.pairwise import cosine_similarity

openai.api_key = "api-key"

SIMILARITY_AGENT_ADDRESS = "address"
CLIENT_AGENT_ADDRESS = "address"

class FileProcessingRequest(Model):
    file_content: str  # Base64-encoded file content
    file_type: str
    job_description: str
    jd_type: str

class FileProcessingResponse(Model):
    extracted_text: str
    similarity:float

embedding_agent = Agent(
    name="embedding_agent",
    port=5002,
    endpoint="http://localhost:5002/submit",
    seed="embedding_seed"
)

def preprocess_text(text: str) -> str:
    """Preprocess text by removing noise and normalizing."""
    import re
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.lower().strip()

@embedding_agent.on_message(model=FileProcessingRequest)
async def handle_embedding(ctx: Context, sender: str, request: FileProcessingRequest):

    response = openai.Embedding.create(input=preprocess_text(request.file_content), model="text-embedding-ada-002")
    resume_embedding = response["data"][0]["embedding"]
    resume_embedding_str = json.dumps(resume_embedding)

    response = openai.Embedding.create(input=preprocess_text(request.job_description), model="text-embedding-ada-002")
    jd_embedding = response["data"][0]["embedding"]
    jd_embedding_str = json.dumps(jd_embedding)
    # Send embeddings back to the original sender (Client)

    similarity = cosine_similarity([resume_embedding], [jd_embedding])[0][0]
    print(similarity)
    await ctx.send(CLIENT_AGENT_ADDRESS, FileProcessingResponse(extracted_text='', 
                                                                    similarity=similarity))

if __name__ == "__main__":
    embedding_agent.run()
