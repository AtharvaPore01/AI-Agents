![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:automation](https://img.shields.io/badge/automation-3D8BD3)

## Agent Name: Linguistic_Analysis_Agent

# Linguistic Analysis System

## Overview
The **Linguistic Analysis System** consists of two agents, a **Preprocessing Agent** and a **Linguistic Analysis Agent**, that analyze resumes and job descriptions for readability, grammar, and keyword relevance. This system helps job seekers optimize their resumes to match job descriptions.

## Components
1. **Linguistic Analysis Agent (Server)**
2. **Linguistic Analysis Client**

## Features
- **Readability Analysis**: Uses multiple readability metrics to assess resume complexity.
- **Grammar Analysis**: Detects and suggests corrections for grammatical errors.
- **Keyword Extraction**: Identifies important keywords and compares them to job descriptions.
- **Compatibility Scoring**: Evaluates how well a resume matches a job description based on keyword similarity.
- **Multi-format Support**: Processes resumes and job descriptions in PDF and DOCX formats.

---

## 1. Linguistic Analysis Agent (Server)

### **Description**
The **Linguistic Analysis Agent** evaluates resumes based on readability, grammar correctness, and keyword relevance compared to a given job description. It returns analysis results along with a compatibility score.

### **Technologies Used**
- **Python**
- **uAgents** (Agent-based framework)
- **TextStat** (Readability scoring)
- **LanguageTool** (Grammar checking)
- **Regular Expressions (re)** (Text processing)
- **Collections (Counter)** (Keyword extraction)

### **Setup & Execution**
1. Install dependencies:
   ```bash
   pip install uagents textstat language-tool-python collections PyPDF2 python-docx
   ```
2. Run the **server agent**:
   ```bash
   python linguistic_server.py
   ```

### **Server Code Overview**
- **Receives a request** containing multiple resumes and a job description.
- **Performs linguistic analysis** using readability metrics and grammar tools.
- **Extracts keywords** and determines missing job-related keywords.
- **Computes a compatibility score** based on keyword overlap.
- **Sends back structured results** to the client.

---

## 2. Linguistic Analysis Client

### **Description**
The **Linguistic Analysis Client** reads resumes and job descriptions, formats them into an appropriate request, and sends them to the server for analysis. The client then displays the results received from the server.

### **Technologies Used**
- **Python**
- **uAgents** (Agent-based framework)
- **PyPDF2** (PDF processing)
- **python-docx** (DOCX processing)

### **Setup & Execution**
1. Ensure all dependencies are installed (see server setup).
2. Run the **client agent**:
   ```bash
   python client.py
   ```

### **Client Code Overview**
- **Prompts user** for resume and job description file paths (PDF or DOCX).
- **Reads and extracts text** from the documents.
- **Formats a request** containing resumes and job descriptions.
- **Sends the request** to the Linguistic Analysis Agent.
- **Receives results** and displays readability scores, grammar issues, missing keywords, and compatibility results.

---

## API Communication

### **Request Format (ResumeAnalysisRequest)**
```json
{
    "resumes": ["resume_text_1", "resume_text_2"],
    "job_description": "job_description_text"
}
```

### **Response Format (ResumeAnalysisResponse)**
```json
{
    "analysis_results": {
        "Resume 1": {
            "Readability Scores": {
                "Flesch Reading Ease": 60.5,
                "Gunning Fog Index": 12.3,
                "Dale-Chall Readability Score": 7.5,
                "SMOG Index": 10.2,
                "Automated Readability Index": 8.7,
                "Coleman-Liau Index": 11.1
            },
            "Grammar Issues": [
                {"error": "Incorrect tense usage", "suggestion": ["used"], "severity": "TENSE_ERROR"}
            ],
            "Missing Keywords": ["Python", "Machine Learning", "Data Science"],
            "Linguistic Score": 72.3
        }
    },
    "compatibility": {
        "Resume 1": true
    }
}
```

---

## Usage Instructions
1. **Start the Server Agent** (linguistic_analysis_agent)
2. **Start the Client Agent** (linguistic_analysis_client)
3. **Follow on-screen prompts** to provide resume and job description files.
4. **Receive and analyze results** to optimize resumes effectively.

---

## Future Enhancements
- **Enhanced NLP Models**: Improve keyword relevance using NLP models like BERT.
- **More Readability Metrics**: Integrate additional linguistic features.
- **Web Interface**: Develop a front-end for easier interaction.
- **Real-time Suggestions**: Generate real-time feedback for improving resumes.

---

## Contributors
- **Aishwarya Dekhane** - AI & Computer Vision Specialist


