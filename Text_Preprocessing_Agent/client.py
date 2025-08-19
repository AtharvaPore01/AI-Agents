import asyncio
import os
from uagents import Agent, Context, Model

# Define the model for sending a resume file
class ResumeFile(Model):
    file_path: str

# Define the model for receiving the processed resume
class ProcessedResume(Model):
    text: str
    output_file_path: str

# Define the client agent
client_agent = Agent(
    name="preprocessing_client",
    port=5069,
    endpoint=["http://localhost:5069/submit"],  # Corrected format
    seed="preprocessing_client_seed"
)

# Preprocessing Agent's address
recipient_address = "address"

# File path to be sent (modify accordingly)
resume_path = "path"  # Change this to the actual path

@client_agent.on_event("startup")
async def send_resume(ctx: Context):
    ctx.logger.info(f"Sending resume file: {resume_path}")

    if not os.path.exists(resume_path):
        ctx.logger.error("Resume file not found. Check the file path.")
        return

    await ctx.send(recipient_address, ResumeFile(file_path=resume_path))
    ctx.logger.info("Resume file sent successfully.")

@client_agent.on_message(model=ProcessedResume)
async def handle_processed_resume(ctx: Context, sender: str, msg: ProcessedResume):
    ctx.logger.info(f"Processed resume received from {sender}! Saved at: {msg.output_file_path}")

if __name__ == "__main__":
    client_agent.run()
