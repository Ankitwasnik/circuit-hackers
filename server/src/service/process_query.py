import json

from langchain_core.output_parsers import JsonOutputParser
from src.agent.nl2esq import get_nl2esq_agent

parser = JsonOutputParser()
FAILURE_MESSAGE = (
    "Sorry, we cannot process your request right now. Please try again later."
)


def get_results(user_question):

    response = get_agent_response(user_question)

    return response


def get_agent_response(agent_input):
    try:
        chat_executor = get_nl2esq_agent()

        agent_input_str = json.dumps(agent_input)
        chat_result = chat_executor.invoke({"input": agent_input_str})
        print(f"chat_result: {chat_result}")
        api_response = {}
        try:
            api_response = parser.parse(chat_result["output"])
            # api_response = {
            #     "answer": chat_result['output']
            # }
        except Exception as e:
            print(f"error in response parsing | {e}")
            api_response = {"message": FAILURE_MESSAGE, "status": "FAILURE", "error": e}

        return api_response

    except Exception as e:
        print(f"error in chat agent | {e}")
        return {"message": FAILURE_MESSAGE, "status": "FAILURE", "error": str(e)}
