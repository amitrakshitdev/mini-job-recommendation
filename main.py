# main.py
# This file contains the FastAPI application setup and integration points for Scrapy.

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import subprocess
import os
import asyncio
from typing import List, Dict, Any

# Initialize FastAPI app
app = FastAPI(
    title="Job Recommendation System API",
    description="API for scraping jobs, recommending jobs, and processing resumes.",
    version="1.0.0"
)

# --- Pydantic Models for API Request/Response ---

class JobQuery(BaseModel):
    query: str

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
db_client = None # Placeholder for database client (e.g., PostgreSQL or MongoDB)

# --- API Endpoints ---

@app.get("/")
async def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Job Recommendation System API!"}

@app.post("/scrape-jobs")
async def scrape_jobs():
    """
    Triggers the Scrapy spider to scrape job listings.
    Note: In a production environment, you might want to run this as a scheduled task
    or a separate microservice rather than directly via an API endpoint,
    especially for long-running scraping jobs.
    """
    try:
        # Change to the Scrapy project directory
        # This assumes your Scrapy project is located at ./scrapy_project relative to main.py
        scrapy_project_path = "./scrapy_project"
        if not os.path.exists(scrapy_project_path):
            raise HTTPException(status_code=500, detail="Scrapy project directory not found.")

        # Run the Scrapy spider as a subprocess
        # 'naukri' is the name of your spider. You can add more spiders or parameters.
        # '-o jobs.json' can be used to output to a file, but we'll integrate with DB later.
        process = await asyncio.create_subprocess_exec(
            "scrapy", "crawl", "naukri", "-o", "jobs-naukri.json",
            cwd=scrapy_project_path, # Set the current working directory for the subprocess
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            print(f"Scrapy Error: {stderr.decode()}")
            raise HTTPException(status_code=500, detail=f"Scrapy failed: {stderr.decode()}")

        print(f"Scrapy Output: {stdout.decode()}")
        return {"message": "Scraping initiated successfully!", "output": stdout.decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate scraping: {str(e)}")

@app.post("/jobs/search")
async def search_jobs(query: JobQuery) -> List[JobPost]:
    """
    Searches for jobs based on a user query using the LLM/NLP module and vector similarity.
    """
    # Placeholder for actual logic:
    # 1. Use LLM/NLP module to process 'query.query' and generate its embedding.
    # 2. Perform vector similarity search in your database (PostgreSQL with pgvector).
    # 3. Retrieve matching job posts.
    print(f"Searching for jobs with query: {query.query}")
    # Mock data for demonstration
    mock_jobs = [
        JobPost(id="1", title="Software Engineer", company="Tech Corp", location="Bangalore", description="Develop software.", url="http://example.com/job1"),
        JobPost(id="2", title="Data Scientist", company="Data Inc", location="Mumbai", description="Analyze data.", url="http://example.com/job2")
    ]
    return mock_jobs

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


# --- Scrapy Project Structure Placeholder ---
# In your project, you would create a directory named 'scrapy_project'
# and initialize a Scrapy project inside it.
# Example structure:
# .
# ├── main.py
# └── scrapy_project/
#     ├── scrapy.cfg
#     ├── scrapy_project/
#     │   ├── __init__.py
#     │   ├── items.py
#     │   ├── middlewares.py
#     │   ├── pipelines.py
#     │   └── settings.py
#     └── spiders/
#         └── naukri_spider.py

# Example content for scrapy_project/spiders/naukri_spider.py:
"""
import scrapy

class NaukriSpider(scrapy.Spider):
    name = 'naukri'
    start_urls = ['https://www.naukri.com/python-jobs'] # Example URL

    def parse(self, response):
        # This is a highly simplified example.
        # You'll need to inspect Naukri's HTML/JS to extract actual job data.
        # Use CSS selectors or XPath to extract job title, company, description, etc.
        for job_card in response.css('.jobTuple'): # Example selector, needs verification
            yield {
                'title': job_card.css('.jobTupleHeader .title::text').get(),
                'company': job_card.css('.jobTupleHeader .companyInfo .companyName::text').get(),
                'location': job_card.css('.jobTupleFooter .location::text').get(),
                'description': ''.join(job_card.css('.jobDescriptionContent::text').getall()).strip(),
                'url': response.urljoin(job_card.css('.jobTupleHeader .title::attr(href)').get()),
            }

        # Follow pagination links if available
        next_page = response.css('.pagination .next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
"""

# To initialize a Scrapy project:
# 1. Create a directory named `scrapy_project` in the same level as `main.py`.
# 2. Navigate into `scrapy_project` in your terminal.
# 3. Run `scrapy startproject scrapy_project .` (the dot means create project in current dir).
# 4. Navigate into `scrapy_project/spiders`.
# 5. Create `naukri_spider.py` (or whatever name you choose) and paste the spider code.

# To run this FastAPI app locally (for testing without Docker yet):
# 1. Make sure you have FastAPI and Uvicorn installed:
#    pip install fastapi uvicorn python-multipart
# 2. Run from your terminal in the directory containing main.py:
#    uvicorn main:app --reload --host 0.0.0.0 --port 8000
# 3. Access the API documentation at http://127.0.0.1:8000/docs
