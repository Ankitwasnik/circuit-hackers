from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import MessagesPlaceholder
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate

from src.llm.llm_provider import LLMProvider
from src.service.es_service import execute_query
from data.few_shot_examples import examples


def get_nl2esq_agent():
    system_prompt = """You are an agent designed to interact with a Elastic Search database. 
    Given an input question, create a search query in Elasticsearch DSL format, execute the query on the database using execute_query tool and based on the execution results provide output in the json format specified.
    
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 10 results. 
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
    DO NOT make query that can change db state (PUT, PATCH, POST, DELETE etc.).
    You must only fetch the relevant data as per the question. For example, if the question is - "Who hit the most centuries in 2022?" your query should only fetch the player names and number of centuries.
    You must use execute_query tool to execute Elasticsearch queries and only respond to user's question based on the query execution results.
    
    There is one index available in the db: BATTING
    BATTING Index Schema: 
    | Field  | Type    | Description |
    |--------|--------|-------------|
    | `50`   | `long`  | Number of half-centuries scored |
    | `100`  | `long`  | Number of centuries scored |
    | `4s`   | `long`  | Number of fours hit |
    | `6s`   | `long`  | Number of sixes hit |
    | `Avg`  | `double` | Batting average |
    | `BF`   | `long`  | Balls faced |
    | `HS`   | `long`  | Highest individual score in an innings |
    | `Inns` | `long`  | Number of innings played |
    | `Mat`  | `long`  | Number of matches played |
    | `NO`   | `long`  | Number of times the batsman was not out |
    | `Player` | `keyword` | Name of the player |
    | `Runs` | `long`  | Total runs scored |
    | `SR`   | `double` | Strike rate (runs per 100 balls) |
    | `Year` | `long`  | Year of the recorded statistics |

    ### Output format:
    Your response must be in JSON format as below:
    ```json
    {{
        "search_query": "Executed Elasticsearch query",
        "execution_result": "Elasticsearch query execution result as it is",
        "status": "SUCCESS/FAILURE. If no data found for the given query, that's not considered as FAILURE",
        "error": "error message"
    }}
    ```

    **Note:** Use only the provided data and never generate response independently.
    """

    few_show_prompt = get_few_shot_prompt(system_prompt)

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_show_prompt),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    llm = LLMProvider.get_chat_model()

    tools = [execute_query]

    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent, tools=tools, verbose=True, max_iterations=10, max_execution_time=50
    )


def get_few_shot_prompt(system_prompt) -> FewShotPromptTemplate:

    embeddings = LLMProvider.get_embedding_model()
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        FAISS,
        k=5,
        input_keys=["input"],
    )

    example_prompt = PromptTemplate.from_template(
        "Question: {input}\n Elasticsearch Query: {es_query}\n"
    )

    system_prompt = system_prompt + "\n##Query Examples:\n"

    return FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=system_prompt,
        suffix="",
        input_variables=["input"],
    )
