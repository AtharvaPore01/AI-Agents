import os
import base64  # Required for encoding binary data
from uagents import Agent, Context, Model

SERVER_AGENT = "address"

class FileProcessingRequest(Model):
    file_content: str  # Base64-encoded file content
    file_type: str
    job_description: str
    jd_type: str

class FileProcessingResponse(Model):
    extracted_text: str
    similarity:float

client_agent = Agent(
    name="file_processing_client",
    port=5069,
    endpoint="http://localhost:5069/submit",
    seed="file_processing_client_seed"
)

def read_file(file_path):
    """Reads the content of a PDF or DOCX file and encodes it as Base64."""
    if not os.path.exists(file_path):
        print("Invalid file path. Please try again.")
        return None, None

    file_extension = os.path.splitext(file_path)[1].lower()
    file_type = None
    if file_extension == ".pdf":
        file_type = "application/pdf"
    elif file_extension == ".docx":
        file_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        print("Unsupported file format. Please provide a PDF or DOCX file.")
        return None, None

    with open(file_path, "rb") as file:
        encoded_content = base64.b64encode(file.read()).decode("utf-8")  # Encode to Base64
        return encoded_content, file_type

# Handle the response from the file processing agent
@client_agent.on_message(model=FileProcessingResponse)
async def handle_response(ctx: Context, sender: str, msg: FileProcessingResponse):
    print(f"\n===== Extracted Text from {sender} =====\n")
    print(f'similarity:{msg.similarity}')
    print("\n" + "="*40)

@client_agent.on_event("startup")
async def startup_handler(ctx: Context):
    resume_file_path = input("Enter the resume file path (PDF or DOCX): ").strip()
    resume_file_content, resume_file_type = read_file(resume_file_path)
    print(resume_file_type)
    jd_file_path = input("Enter the jd file path (PDF or DOCX): ").strip()
    jd_file_content, jd_file_type = read_file(jd_file_path  )
    print(jd_file_type)
    if resume_file_content and resume_file_type and jd_file_content and jd_file_type:
        request = FileProcessingRequest(file_content=resume_file_content, 
                                        file_type=resume_file_type, 
                                        job_description=jd_file_content,
                                        jd_type=jd_file_type)
        await ctx.send(SERVER_AGENT, request)

if __name__ == "__main__":
    client_agent.run()
