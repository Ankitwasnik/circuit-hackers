import json

from langchain_core.output_parsers import JsonOutputParser
from src.agent.nl2esq import get_nl2esq_agent
from src.chain.transform_response import get_transformer_chain

parser = JsonOutputParser()
FAILURE_MESSAGE = (
    "Sorry, we cannot process your request right now. Please try again later."
)


def get_results(user_question):

    response = get_agent_response(user_question)

    if response.get("status") == "FAILURE":
        return response

    try:
        transformer_chain = get_transformer_chain()
        result = transformer_chain.invoke(
            {
                "es_response": response.get("execution_result", "{}"),
            }
        )
    except Exception as e:
        print(f"Error generating response: {e}")
        return {"message": FAILURE_MESSAGE, "status": "FAILURE", "error": str(e)}

    return result


def get_agent_response(agent_input):
    try:
        chat_executor = get_nl2esq_agent()

        chat_result = chat_executor.invoke({"input": agent_input})
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
