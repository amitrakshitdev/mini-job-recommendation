# main.py
# This file contains the FastAPI application setup and integration points for Scrapy.

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
import subprocess
import os
import asyncio
from typing import List, Dict, Any
from db.db_client import DatabaseClient
from db.jobs_schema import JobDocument
from scrapers.naukri_scraper import main as scrap_naukri
from llm.gemini import GeminiClient
from utils.string_utils import get_list_from_string
from bson import ObjectId




# Initialize FastAPI app
app = FastAPI(
    title="Job Recommendation System API",
    description="API for scraping jobs, recommending jobs, and processing resumes.",
    version="1.0.0"
)

# --- Pydantic Models for API Request/Response ---

class JobQueryBody(BaseModel):
    title: str
    company: str
    location: str
    experience: str
    post_date: str
    key_skills: List[str]

class JobPost(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    # Add more fields as per your scraped data structure

class RecommendationRequest(BaseModel):
    job_id: str

class RecommendationResponse(BaseModel):
    recommended_jobs: List[JobPost]

# --- Placeholder for Database Connection (will be initialized later) ---
# In a real application, you'd use SQLAlchemy (for PostgreSQL) or PyMongo (for MongoDB)
# and initialize connections here or via dependency injection.
# For now, these are just placeholders.
db_client = DatabaseClient(db_name="JobReco")
gemini = GeminiClient()
# --- API Endpoints ---

@app.get("/")
async def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Job Recommendation System API!"}

@app.post("/scrape-jobs-naukri")
async def scrape_jobs(req: Request):
    """
    Triggers the naukri scraping process using playright.
    Note: In a production environment, you might want to run this as a scheduled task
    or a separate microservice rather than directly via an API endpoint,
    especially for long-running scraping jobs.
    """
    try:
        body = await req.json()
        search_query = body.get("search_query", "Software Engineering Jobs")
        start_page = body.get("start_page", 1)
        end_page = body.get("end_page", 5)

        await scrap_naukri(search_query, start_page, end_page)
        return {"message": "Scraping initiated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate scraping: {str(e)}")
    
@app.post("/user-query")
async def user_query(request: Request):
    body = await request.json()
    print(f"Received user query:", body)
    response = await gemini.get_jobs_by_agent(body["query"])
    output_string = ''
    if "output" in response:
        output_string = response["output"]
    jobs_id_list = get_list_from_string(output_string)
    jobs_object_id_list = list(map(lambda id: ObjectId(id), jobs_id_list))
    jobs_data = db_client.run_query("Jobs", {"_id": {"$in": jobs_object_id_list}})
    response = {"data": jobs_data,
            "count": len(jobs_data)}
    if len(jobs_id_list) == 0:
        response = {"data": [], 
                    "count": 0, 
                    "message" : output_string}
    return response
    

@app.post("/jobs/search")
async def search_jobs(body: JobQueryBody) -> List[Any]:
    """
    Searches for jobs based on a user query using the LLM/NLP module and vector similarity.
    """ 
    print(f"Searching for jobs with query: {body}")
    query = {
        "title": body.title,
        "company": body.company,
        "location": body.location,
        "experience": body.experience,
        "post_date": body.post_date,
        "key_skills": body.key_skills
    }
    search_results: List[JobDocument] = db_client.run_query("Jobs", query)
    return search_results

@app.post("/jobs/{job_id}/recommend-similar")
async def recommend_similar_jobs(job_id: str) -> RecommendationResponse:
    """
    Recommends similar jobs based on a given job ID.
    """
    # Placeholder for actual logic:
    # 1. Retrieve the embedding of the job with 'job_id'.
    # 2. Perform vector similarity search to find other similar job embeddings.
    # 3. Retrieve details of recommended jobs.
    print(f"Recommending similar jobs for job ID: {job_id}")
    # Mock data for demonstration
    mock_recommended_jobs = [
        JobPost(id="3", title="Senior Software Engineer", company="Innovate Solutions", location="Hyderabad", description="Lead software development.", url="http://example.com/job3"),
        JobPost(id="4", title="Backend Developer", company="CodeWorks", location="Bangalore", description="Build robust backend systems.", url="http://example.com/job4")
    ]
    return RecommendationResponse(recommended_jobs=mock_recommended_jobs)

@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Uploads a resume (PDF/DOCX) and recommends jobs based on its content.
    """
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed.")

    file_location = f"/tmp/{file.filename}" # Temporary storage for the uploaded file
    try:
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Placeholder for actual logic:
        # 1. Use Document Processing module to extract text from 'file_location'.
        # 2. Use NLP/LLM module to parse resume text, extract skills, and generate resume embedding.
        # 3. Perform vector similarity search using resume embedding against job embeddings.
        # 4. Return recommended jobs.
        print(f"Received resume: {file.filename} ({file.content_type})")
        # Mock recommendation for demonstration
        mock_recommended_jobs = [
            JobPost(id="5", title="Cloud Engineer", company="Cloud Solutions", location="Pune", description="Manage cloud infrastructure.", url="http://example.com/job5"),
            JobPost(id="6", title="DevOps Specialist", company="Automate Inc", location="Chennai", description="Implement CI/CD pipelines.", url="http://example.com/job6")
        ]
        return {"message": f"Resume '{file.filename}' uploaded and processed successfully!", "recommended_jobs": mock_recommended_jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(file_location):
            os.remove(file_location)

# To run this FastAPI app locally (for testing without Docker yet):
# 1. Make sure you have FastAPI and Uvicorn installed:
#    pip install fastapi uvicorn python-multipart
# 2. Run from your terminal in the directory containing main.py:
#    uvicorn main:app --reload --host 0.0.0.0 --port 8000
# 3. Access the API documentation at http://127.0.0.1:8000/docs
