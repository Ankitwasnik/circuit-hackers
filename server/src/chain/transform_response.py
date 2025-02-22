from llm.llm_provider import LLMProvider
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter
from langchain_core.output_parsers import JsonOutputParser

from data.few_shot_examples import examples


def get_transformer_chain():

    system_prompt = f"""
    **Task:** Your task is to transform the data that I received after executing Elasticsearch Query into the json format specified.

    Target JSON Format:
    {{{{
        "labels": "array of strings",
        "datasets": [
            {{{{
            "label": "string",
            "data": "array of numbers"
            }}}}
        ]
    }}}}

    Your response must be in Target JSON format.

    **Note:** Use only the provided data and never generate answers independently.

    ### Example 1

    Elasticsearch Response: {{{{ "aggregations": {{{{ "yearwise_runs_scored": {{{{ "buckets": [ {{{{ "key": 2016, "total_runs": {{{{ "value": 973 }}}} }}}}, {{{{ "key": 2017, "total_runs": {{{{ "value": 308 }}}} }}}}, {{{{ "key": 2018, "total_runs": {{{{ "value": 530 }}}} }}}}, {{{{ "key": 2019, "total_runs": {{{{ "value": 464 }}}} }}}}, {{{{ "key": 2020, "total_runs": {{{{ "value": 466 }}}} }}}}, {{{{ "key": 2021, "total_runs": {{{{ "value": 405 }}}} }}}}, {{{{ "key": 2022, "total_runs": {{{{ "value": 341 }}}} }}}} ] }}}} }}}} }}}}
    Target Json: {{{{"labels": ["2016", "2017", "2018", "2019", "2020", "2021", "2022"], "datasets": [{{{{"label": "Total Runs", "data": [973, 308, 530, 464, 466, 405, 341]}}}}]}}}}
    
    ### Example 2

    Elasticsearch Response: {{{{ "hits": {{{{ "hits": [ {{{{ "_source": {{{{ "Player": "Shikhar Dhawan", "matches_played": 110 }}}} }}}}, {{{{ "_source": {{{{ "Player": "Dinesh Karthik", "matches_played": 107 }}}} }}}}, {{{{ "_source": {{{{ "Player": "MS Dhoni", "matches_played": 105 }}}} }}}}, {{{{ "_source": {{{{ "Player": "Sanju Samson", "matches_played": 100 }}}} }}}}, {{{{ "_source": {{{{ "Player": "Virat Kohli", "matches_played": 100 }}}} }}}}, {{{{ "_source": {{{{ "Player": "Ravindra Jadeja", "matches_played": 99 }}}} }}}}, {{{{ "_source": {{{{ "Player": "Rohit Sharma", "matches_played": 99 }}}} }}}}, {{{{ "_source": {{{{ "Player": "Hardik Pandya", "matches_played": 98 }}}} }}}}, {{{{ "_source": {{{{ "Player": "Krunal Pandya", "matches_played": 98 }}}} }}}}, {{{{ "_source": {{{{ "Player": "Rishabh Pant", "matches_played": 98 }}}} }}}} ] }}}} }}}}
    Target Json: {{{{"labels": ["Shikhar Dhawan", "Dinesh Karthik", "MS Dhoni", "Sanju Samson", "Virat Kohli", "Ravindra Jadeja", "Rohit Sharma", "Hardik Pandya", "Krunal Pandya", "Rishabh Pant"], "datasets": [{{{{"label": "Most Matches", "data": [110, 107, 105, 100, 100, 99, 99, 98, 98, 98]}}}}]}}}}

    ### Example 3

    Elasticsearch Response: {{{{"took":6,"timed_out":false,"_shards":{{{{"total":1,"successful":1,"skipped":0,"failed":0}}}},"hits":{{{{"total":{{{{"value":1005,"relation":"eq"}}}},"max_score":null,"hits":[]}}}},"aggregations":{{{{"season stats":{{{{"doc_count_error_upper_bound":0,"sum_other_doc_count":0,"buckets":[{{{{"key":2016,"doc_count":136,"total_runs":{{{{"value":17962}}}},"avg_strike_rate":{{{{"value":115.03411764705882}}}},"total_fours":{{{{"value":1632}}}},"total_sixes":{{{{"value":638}}}},"total_hundreds":{{{{"value":7}}}}}}}},{{{{"key":2017,"doc_count":143,"total_runs":{{{{"value":17907}}}},"avg_strike_rate":{{{{"value":112.15482517482518}}}},"total_fours":{{{{"value":1608}}}},"total_sixes":{{{{"value":705}}}},"total_hundreds":{{{{"value":5}}}}}}}},{{{{"key":2018,"doc_count":138,"total_runs":{{{{"value":19098}}}},"avg_strike_rate":{{{{"value":114.95152173913043}}}},"total_fours":{{{{"value":1652}}}},"total_sixes":{{{{"value":872}}}},"total_hundreds":{{{{"value":5}}}}}}}},{{{{"key":2019,"doc_count":144,"total_runs":{{{{"value":18574}}}},"avg_strike_rate":{{{{"value":109.6175}}}},"total_fours":{{{{"value":1653}}}},"total_sixes":{{{{"value":784}}}},"total_hundreds":{{{{"value":6}}}}}}}},{{{{"key":2020,"doc_count":133,"total_runs":{{{{"value":18508}}}},"avg_strike_rate":{{{{"value":107.36473684210526}}}},"total_fours":{{{{"value":1582}}}},"total_sixes":{{{{"value":734}}}},"total_hundreds":{{{{"value":5}}}}}}}},{{{{"key":2021,"doc_count":149,"total_runs":{{{{"value":17716}}}},"avg_strike_rate":{{{{"value":105.0556375838926}}}},"total_fours":{{{{"value":1548}}}},"total_sixes":{{{{"value":687}}}},"total_hundreds":{{{{"value":4}}}}}}}},{{{{"key":2022,"doc_count":162,"total_runs":{{{{"value":23052}}}},"avg_strike_rate":{{{{"value":120.40623456790124}}}},"total_fours":{{{{"value":2017}}}},"total_sixes":{{{{"value":1062}}}},"total_hundreds":{{{{"value":8}}}}}}}}]}}}}}}}}}}}}
    Target JSON: {{{{"labels":["2016","2017","2018","2019","2020","2021","2022"],"datasets":[{{{{"label":"Total Runs","data":[17962,17907,19098,18574,18508,17716,23052]}}}},{{{{"label":"Average Strike Rate","data":[115.03,112.15,114.95,109.62,107.36,105.06,120.41]}}}},{{{{"label":"Total Fours","data":[1632,1608,1652,1653,1582,1548,2017]}}}},{{{{"label":"Total Sixes","data":[638,705,872,784,734,687,1062]}}}},{{{{"label":"Total Hundreds","data":[7,5,5,6,5,4,8]}}}}]}}}}


    Elasticsearch Response: {{es_response}}
    Target JSON:
    """

    prompt = ChatPromptTemplate.from_template(system_prompt)

    llm = LLMProvider.get_chat_model()

    parser = JsonOutputParser()

    return (
        {
            "es_response": itemgetter("es_response"),
        }
        | prompt
        | llm
        | parser
    )
