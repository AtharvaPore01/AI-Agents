import os
import asyncio
from uagents import Agent, Context, Model
from PyPDF2 import PdfReader
from docx import Document

SERVER_AGENT = 'address'

# Define Resume Analysis Request Model
class ResumeAnalysisRequest(Model):
    resumes: list  # List of resume texts
    job_description: str  # Job description text

# Define Resume Analysis Response Model
class ResumeAnalysisResponse(Model):
    analysis_results: dict  # Dictionary containing readability, grammar, and keyword analysis
    compatibility: dict  # Dictionary to store compatibility results (True/False)

# Define the client agent
clientAgent = Agent(
    name='linguistic_analysis_client',
    port=5069,
    endpoint='http://localhost:5069/submit',  # Specify endpoint for the client agent
    seed='linguistic_analysis_client_seed'
)

def read_pdf(file_path):
    """Reads content from a PDF file."""
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def read_docx(file_path):
    """Reads content from a DOCX file."""
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def load_resumes(num_resumes):
    """Prompts the user to input file paths for the resumes."""
    resumes = []
    for i in range(num_resumes):
        file_path = input(f"Enter the file path for resume {i + 1} (PDF or DOCX): ").strip()
        if not os.path.exists(file_path):
            print("Invalid file path. Please try again.")
            return load_resumes(num_resumes)
        
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.pdf':
            resumes.append(read_pdf(file_path))
        elif file_extension == '.docx':
            resumes.append(read_docx(file_path))
        else:
            print("Unsupported file format. Please provide a PDF or DOCX file.")
            return load_resumes(num_resumes)
    
    return resumes

def load_job_description():
    """Prompts the user to input the job description file path."""
    file_path = input("Enter the job description file path (PDF or DOCX): ").strip()
    if not os.path.exists(file_path):
        print("Invalid file path. Please try again.")
        return load_job_description()

    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.pdf':
        return read_pdf(file_path)
    elif file_extension == '.docx':
        return read_docx(file_path)
    else:
        print("Unsupported file format. Please provide a PDF or DOCX file.")
        return load_job_description()

# Handle the response from the linguistic analysis agent
@clientAgent.on_message(model=ResumeAnalysisResponse)
async def handle_response(ctx: Context, sender: str, msg: ResumeAnalysisResponse):
    print(f"Received analysis results from {sender}")
    if msg.analysis_results:
        print("Linguistic Analysis Results:")
        for resume, analysis in msg.analysis_results.items():
            print(f"\n{resume}:")
            print("Readability Scores:", analysis["Readability Scores"])
            print("Grammar Issues:", analysis["Grammar Issues"])
            print("Missing Keywords:", analysis["Missing Keywords"])
            print("Linguistic Score:", analysis["Linguistic Score"])
        
        print("\nCompatibility Results:")
        for resume, compatibility in msg.compatibility.items():
            print(f"{resume}: {'Compatible' if compatibility else 'Not Compatible'}")

# Prepare and send request to linguistic analysis agent
@clientAgent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Client Agent {ctx.agent.name} started at {ctx.agent.address}')

    # Collect user input for resumes and job description
    num_resumes = int(input("How many resumes do you have? ").strip())
    resumes = load_resumes(num_resumes)
    job_description = load_job_description()

    # Send request to linguistic analysis agent
    sender_address = clientAgent.address
    request = ResumeAnalysisRequest(resumes=resumes, job_description=job_description)
    
    # Send the request to the server agent
    await ctx.send(SERVER_AGENT, request)

if __name__ == "__main__":
    clientAgent.run()
