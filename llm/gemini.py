from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
import re
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from utils.string_utils import get_json_from_string
from db.db_client import DatabaseClient
from log.logger_config import configured_logger
from loguru import logger
import ast

load_dotenv() # This loads the variables from .env into the environment
class ResumeDetails(BaseModel):
    job_title: Optional[str]
    location: Optional[str]
    key_skills: List[str]
    exp_years: int

class ModelResponseJobs(BaseModel):
    output: List[str]

class AgentJobResponse(BaseModel):
    input: str
    output: str
    
db_client = DatabaseClient(db_name="JobReco")
@tool
def run_db_query_tool(input_string_literal: str) -> List[Dict[str, Any]]:
    """
    Runs a database query on the specified collection with the given query parameters.
    This tool makes an HTTP POST request to the FastAPI server's /run_db_query endpoint.

    Args:
        collection (str): The name of the database collection (e.g., "Jobs").
        
        query (Dict[str, Any]): A dictionary representing the mongoDB client query.
        It accepts any complex mongoDB query. You should create a db query object based on the
        document structure of the mongoDB document.
        
        Here is an example of a mongoDB Document:
        {
            _id: ObjectId('686a718b9ec6ecefa24595d5'),
            id: 'Ppu2Pt4GhZ8DmKK',
            title: 'Dot Net Developer - Senior Software Engineer',
            company: 'Bajaj Financial Securities',
            location: 'Pune',
            experience: '4-8 Yrs',
            experience_min_years: 4,
            experience_max_years: 8,
            post_date: '4 days ago',
            link: 'https://www.naukri.com/job-listings-dot-net-developer-senior-software-engineer-bajaj-financial-securities-pune-4-to-8-years-010725024658',
            key_skills: [
            '.Net Core', 'web API',
            'PYTHON',    'AWS',
            'redis',     'C#',
            'Azure',     'Mysql',
            'linux',     'SQL Server'
            ],
            job_description: <The description of the jobs in html format with html tags>
        }
    If no specific query is needed, pass an empty dictionary {}.

    Returns:
        List[str]: A list of ids, where each id is a document id from the database
        matching the query. Returns an empty list if no results or an error occurs.
    """
    
    logger.debug("inputDict", input_string_literal)
    logger.info("Received tool call: inputDict", input_string_literal)
    
    extracted_json = get_json_from_string(input_string_literal)
    extracted_dict = ast.literal_eval(extracted_json)
    
    collection = extracted_dict["collection"]
    query = extracted_dict["query"]

    # logger.info("coll", collection)
    # logger.info("query", query)
    try:
        results = db_client.run_query(collection, query)
        logger.info(f"--- Tool Call: Received {len(results)} results from server. ---")
        def process_results(result):
            id = ""
            if "_id" in result:
                id = result["_id"]
                # logger.info("id", id)
            return id
        processed_result = list(map(process_results, results))
        logger.info("No. of jobs found: ", len(processed_result))
        return processed_result
    except Exception as e:
        return [{"error": f"An unexpected error occurred: {e}"}]

class GeminiClient:
    def __init__(self, model_name: str = "gemini-1.5-flash-latest", temperature: float = 0.0):
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
        self.model = init_chat_model("gemini-1.5-flash-latest", model_provider="google_genai")
        logger.info(f"Gemini client created successfully with model {model_name}")
        
    async def __run_react_agent__(self, prompt: PromptTemplate, tools, query):
        agent = create_react_agent(self.llm, tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        response = await agent_executor.ainvoke({"input": query})
        logger.info(f"\n--- Agent Response: {response} ---")
        return response

    async def get_jobs_by_agent(self, query: str) -> AgentJobResponse:
        llm = self.llm
        tools = [run_db_query_tool]
        # The ReAct agent prompt requires specific variables: `tools`, `tool_names`, 
        # and `agent_scratchpad`. It also expects a specific format for the agent's
        # reasoning process (Thought, Action, Action Input, Observation).
        prompt = PromptTemplate.from_template("""
        You are an expert at extracting key job-related information from a user's query to find relevant job postings.
        Your task is to analyze the user's input, identify job details, and use the available tools to query a database.

        You have access to the following tools:
        {tools}

        Use the following format:

        Question: The user's input about the job they are looking for.
        Thought: You should always think about what to do. Analyze the user's query to extract details like job title, location, skills, company, and experience. Then, decide to use the 'run_db_query_tool' to search the database.
        Action: The action to take, should be one of [{tool_names}].
        Action Input: The input to the action, which should be a dictionary with 'collection' and 'query' keys and strictly NOT any markdown literal text. Make the query should NOT be case sensitive. Limit the database query to retrieve 30 jobs.
        
        Observation: The result of the action from the database.
        ... (this Thought/Action/Action Input/Observation can repeat 5 times if you need to refine the search. Do NOT keep on trying the tool.)
        Thought: I now have the final list of job _id.
        Final Answer: The final answer should be the direct output from the tool and nothing extra.
        
        - If the user's query is related to a job search, you must extract the relevant information and call the 'run_db_query_tool' tool to get data from the database.
        - If the query is ambiguous or lacks specific details for a particular field, you should construct the query with the available information.
        - If the user's query is not related to a job search, you must respond with the message: "I can only help with job-related queries."

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}""")
        response = await self.__run_react_agent__(prompt, tools, query)
        return response

    async def analyse_resume_text_and_fetch_jobs(self, resume_text: str) -> AgentJobResponse:
        tools = [run_db_query_tool]
        prompt = PromptTemplate.from_template("""
        You are an expert at extracting key job-related information from a user's resume text to find relevant job postings and with the key information of the resume.
        Your task is to analyze the resume text data given by the user, identify the key job-related details, and use the available tools to query a database and then find relevant jobs for the user.

        You have access to the following tools:
        {tools}

        Use the following format:

        Question: The resume text data given by the user as input about the job they are looking for.
        Thought: You should always think about what to do. Analyze the text of the resume to extract details like job title, location, skills, company, and experience. Then, decide to use the 'run_db_query_tool' to search the database and Retrieve relevant Jobs.
        Action: The action to take, should be one of [{tool_names}].
        Action Input: You are calling an internal tool, so do NOT create any markdown literal text. The input to the action should be a Dictionary object with 'collection' and 'query' keys. The query should NOT be case sensitive.
        
        Observation: The result of the action from the database.
        ... (this Thought/Action/Action Input/Observation can repeat upto 6 times if you need to refine the search)
        Thought: I now have the final list of jobs.

        Final Answer: The final answer should be the direct output from the tool and nothing extra with schema {output_schema}
        
        - If you do not find any job relevant to the resume politely respond to the user.

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}""")
        response = await self.__run_react_agent__(prompt, tools, resume_text)
        return response

    async def extract_key_info_from_resume(self, resume_text: str):
        model_with_struct = self.model.with_structured_output(ResumeDetails)
        messages = [SystemMessage(content='''You are an expert in analysing peoples' resume from text data 
                                  and generating a structured output of the analysed data'''),
                    HumanMessage(content=f'''
                                 Analyse the following text information:
                                 {resume_text}
                                 Now, generate structured details of the resume.
                                 ''')
                    ]
        model_response = await model_with_struct.ainvoke(messages)
        return model_response.model_dump()
    
    async def get_similar_jobs(self, job_data):
        query = job_data if type(job_data) == str else str(job_data)
        tools = [run_db_query_tool]
        prompt=PromptTemplate.from_template(
            """
        You are an expert at extracting key job-related information from job posting data and finding similar job postings and with the key information from the provided job data.
        Your task is to analyse the job data given by the user and find similar job postings from a database.

        You have access to the following tools:
        {tools}

        Use the following format:

        Question: The Job data contains key information like job title, location, skills, company, and experience.
        Thought: You should always think about what to do. Analyze the key details of the job. Then, decide to use the 'run_db_query_tool' to search the database and Retrieve similar Jobs.
        Action: The action to take, should be one of [{tool_names}].
        Action Input: You are calling an internal tool, so do NOT create any markdown literal text. The input to the action should be a Dictionary object with 'collection' and 'query' keys. The query should NOT be case sensitive.
        
        Observation: The result of the action from the database.
        ... (this Thought/Action/Action Input/Observation can repeat upto 6 times if you need to refine the search)
        Thought: I now have the final list of jobs.

        Final Answer: The final answer should be the direct output from the tool and nothing extra.
        
        - If you do not find any relevant job return an empty list.

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}"""
        )
        response = await self.__run_react_agent__(prompt, tools, query)
        return response

# gemini_client = GeminiClient()
# query = "I am looking for software engineering jobs in kolkata of java spring boot a mid senior level job"

# if __name__ == "__main__":
#     response = gemini_client.get_user_query_response(query, "")
#     logger.info(response)