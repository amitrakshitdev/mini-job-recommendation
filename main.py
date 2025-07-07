# main.py
# This file contains the FastAPI application setup and integration points for Scrapy.

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
import json
import os
import asyncio
from typing import List, Dict, Any
from db.db_client import DatabaseClient
from db.jobs_schema import JobDocument
from scrapers.naukri_scraper import main as scrap_naukri
from llm.gemini import GeminiClient
from utils.string_utils import get_list_from_string
from bson import ObjectId
from utils.string_utils import extract_text_from_pdf, extract_text_from_docx
from log.logger_config import configured_logger
from loguru import logger

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
model_name = "gemini-1.5-flash-8b-latest"
gemini = GeminiClient(model_name)
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
    logger.info(f"Received user query:", body)
    response = await gemini.get_jobs_by_agent(body["query"])
    output_string = ''
    if "output" in response:
        output_string = response["output"]
    jobs_id_list = get_list_from_string(output_string)
    jobs_object_id_list = list(map(lambda id: ObjectId(id), jobs_id_list))
    jobs_data = db_client.run_query("Jobs", {"_id": {"$in": jobs_object_id_list}})
    response = {"count" : len(jobs_data),
                "data": jobs_data}
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
    logger.info(f"Searching for jobs with query: {body}")
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

@app.get("/jobs/recommend-similar/{job_id}")
async def recommend_similar_jobs(job_id: str):
    """
    Recommends similar jobs based on a given job ID.
    """
    job_data = db_client.run_query("Jobs", {"_id": ObjectId(job_id)})
    if len(job_data) == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    else:
        job = job_data[0]
        del job["job_description"]
    llm_response = await gemini.get_similar_jobs(job)
    output_string = ''
    if "output" in llm_response:
        output_string = llm_response["output"]
    jobs_id_list = get_list_from_string(output_string)
    jobs_object_id_list = list(map(lambda id: ObjectId(id), jobs_id_list))
    jobs_data = db_client.run_query("Jobs", {"_id": {"$in": jobs_object_id_list}})
    response = {"data": jobs_data,
                    "count": len(jobs_id_list)}
    if len(jobs_data) == 0:
        response = {"data": [], 
                        "count": 0, 
                        "message" : "No similar jobs found."}
    return response

@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Uploads a resume (PDF/DOCX) and recommends jobs based on its content.
    """
    if file.content_type not in ["application/pdf",
                                #  "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                 ]:
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_location = f"/tmp/{file.filename}" # Temporary storage for the uploaded file
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    try:
        if file.content_type == "application/pdf":
            resume_text = extract_text_from_pdf(file)
        else:
            resume_text = extract_text_from_docx(file)
        # resume_key_info = await gemini.extract_key_info_from_resume(resume_text)
        response = await gemini.analyse_resume_text_and_fetch_jobs(resume_text)
        logger.info(f"Received resume: {file.filename} ({file.content_type})")
        output_string = ''
        if "output" in response:
            output_string = response["output"]
        jobs_id_list = get_list_from_string(output_string)
        jobs_object_id_list = list(map(lambda id: ObjectId(id), jobs_id_list))
        jobs_data = db_client.run_query("Jobs", {"_id": {"$in": jobs_object_id_list}})

        response = {"data": jobs_data,
                    "count": len(jobs_id_list)}
        if len(jobs_data) == 0:
            response = {"data": [], 
                        "count": 0, 
                        "message" : "No jobs found for this resume."}
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(file_location):
            os.remove(file_location)

@app.post("/resume/upload-key-info")
async def upload_resume_key_info(file: UploadFile = File(...)):
    """
    Uploads a resume (PDF/DOCX) and recommends jobs based on its content.
    """
    if file.content_type not in ["application/pdf",
                                #  "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                 ]:
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_location = f"/tmp/{file.filename}" # Temporary storage for the uploaded file
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    try:
        logger.info(f"Received resume: {file.filename} ({file.content_type})")
        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(file)
        else:
            text = extract_text_from_docx(file)
        response = await gemini.extract_key_info_from_resume(text)
        logger.info(response)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(file_location):
            os.remove(file_location)


