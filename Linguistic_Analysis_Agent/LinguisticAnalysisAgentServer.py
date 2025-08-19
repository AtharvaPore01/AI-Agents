from uagents import Agent, Context, Model
from textstat import flesch_reading_ease, gunning_fog, dale_chall_readability_score, smog_index, automated_readability_index, coleman_liau_index
import language_tool_python
from collections import Counter
import re

# Initialize grammar tool
language_tool = language_tool_python.LanguageToolPublicAPI('en-US')

# Define Resume Analysis Request Model
class ResumeAnalysisRequest(Model):
    resumes: list  # List of resume texts
    job_description: str  # Job description text

# Define Resume Analysis Response Model
class ResumeAnalysisResponse(Model):
    analysis_results: dict  # Dictionary containing readability, grammar, and keyword analysis
    compatibility: dict  # Dictionary to store compatibility results (True/False)

# Define the main agent
linguistic_agent = Agent(
    name='linguistic_analysis_agent',
    port=5068,
    endpoint='http://localhost:5068/submit',
    seed='linguistic_analysis_agent_seed'
)

# Function to extract keywords from text
def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

# Function to calculate compatibility score between resume and job description
def calculate_compatibility(resume_keywords, job_keywords):
    # Calculate common keywords
    common_keywords = resume_keywords & job_keywords
    score = len(common_keywords) / len(job_keywords)  # A simple compatibility score
    return score

# Handler for startup event
@linguistic_agent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Agent {ctx.agent.name} started at {ctx.agent.address}')

# Handler for receiving Resume Analysis Request
@linguistic_agent.on_message(model=ResumeAnalysisRequest)
async def handle_query(ctx: Context, sender: str, request: ResumeAnalysisRequest):
    results = {}
    compatibility_results = {}
    
    job_keywords = extract_keywords(request.job_description)
    
    for idx, resume in enumerate(request.resumes):
        # Calculate readability scores for each resume
        readability_scores = {
            "Flesch Reading Ease": flesch_reading_ease(resume),
            "Gunning Fog Index": gunning_fog(resume),
            "Dale-Chall Readability Score": dale_chall_readability_score(resume),
            "SMOG Index": smog_index(resume),
            "Automated Readability Index": automated_readability_index(resume),
            "Coleman-Liau Index": coleman_liau_index(resume)
        }
        
        # Get grammar feedback for each resume
        grammar_errors = language_tool.check(resume)
        grammar_feedback = [{
            "error": error.message,
            "suggestion": error.replacements,
            "severity": error.ruleId
        } for error in grammar_errors[:5]]  # Limit feedback to 5 errors per resume
        
        # Extract keywords from the resume and find missing ones
        resume_keywords = extract_keywords(resume)
        missing_keywords = [word for word in job_keywords if word not in resume_keywords]
        
        # Calculate linguistic score based on readability and grammar
        linguistic_score = sum(readability_scores.values()) / len(readability_scores) - len(grammar_errors) * 2  # Scoring formula
        
        # Calculate compatibility score
        compatibility_score = calculate_compatibility(resume_keywords, job_keywords)
        
        # Collect results for the resume
        results[f"Resume {idx+1}"] = {
            "Readability Scores": readability_scores,
            "Grammar Issues": grammar_feedback,
            "Missing Keywords": missing_keywords[:10],  # Limit to 10 missing keywords
            "Linguistic Score": round(linguistic_score, 2)
        }
        
        # Check compatibility
        compatibility_results[f"Resume {idx+1}"] = compatibility_score >= 0.5  # Threshold for compatibility (50%)

    # Send the analysis results and compatibility to the sender
    response = ResumeAnalysisResponse(
        analysis_results=results,
        compatibility=compatibility_results
    )
    await ctx.send(sender, response)

# Run the agent
if __name__ == "__main__":
    linguistic_agent.run()
