from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List, Dict, Any
from dotenv import load_dotenv
import os
import requests
from db.db_client import DatabaseClient
from log.logger import logger
import ast

load_dotenv() # This loads the variables from .env into the environment


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
        It accepts any complex mongoDB query.
        
        Here is an example of a query dict:
        The example query dict:
        {"title" : {"$regex": f'Lead Software Engineer'},
        "company" : {"$regex": "Wells Fargo"},
        "location" : {"$regex": "Hyderabad"},
        "experience" : {"$regex": "1-3 Yrs"},
        "post_date" : {"$regex": f'1 day ago'}',
        "key_skills" : {"$in": ["Java", "React", "Kafka"]}
        }
    If no specific query is needed, pass an empty dictionary {}.

    Returns:
        List[str]: A list of ids, where each id is a document id from the database
                            matching the query.Returns an empty list if no results
                            or an error occurs.
    """
    
    logger.debug("inputDict", input_string_literal)
    print("Received tool call: inputDict", input_string_literal)
    extracted_dict = ast.literal_eval(input_string_literal)
    
    collection = extracted_dict["collection"]
    query = extracted_dict["query"]

    # logger.info("coll", collection)
    # logger.info("query", query)
    try:
        results = db_client.run_query(collection, query)
        print(f"--- Tool Call: Received {len(results)} results from server. ---")
        def process_results(result):
            id = ""
            if "_id" in result:
                id = result["_id"]
                print("id", id)
            return id
        processed_result = list(map(process_results, results))
        print("No. of jobs found: ", len(results))
        return processed_result
    except Exception as e:
        return [{"error": f"An unexpected error occurred: {e}"}]


class GeminiClient:
    def __init__(self):
        # System instructions are passed within the message list for each API call,
        # rather than during model initialization.
        # I've also updated the model to a generally available one.
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
        self.model = init_chat_model("gemini-1.5-flash-latest", model_provider="google_genai")
        logger.info("Gemini client created successfully...")

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
        Action Input: The input to the action, which should be a dictionary with 'collection' and 'query' keys and strictly NOT any markdown literal text. Make the query should NOT be case sensitive.
        Observation: The result of the action from the database.
        ... (this Thought/Action/Action Input/Observation can repeat 5 times if you need to refine the search)
        Thought: I now have the final list of job _id.
        Final Answer: The final answer should be the direct output from the tool and nothing extra.
        
        - If the user's query is related to a job search, you must extract the relevant information and call the 'run_db_query_tool' tool to get data from the database.
        - If the query is ambiguous or lacks specific details for a particular field, you should construct the query with the available information.
        - If the user's query is not related to a job search, you must respond with the message: "I can only help with job-related queries."

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}""")
        agent = create_react_agent(self.llm, tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        response = await agent_executor.ainvoke({"input": query})
        print(f"\n--- Agent Response: {response} ---")
        return response


# gemini_client = GeminiClient()
# query = "I am looking for software engineering jobs in kolkata of java spring boot a mid senior level job"

# if __name__ == "__main__":
#     response = gemini_client.get_user_query_response(query, "")
#     print(response)