examples = [
    {
        "input": "Get me runs scored by Virat Kohli over the years",
        "es_query": '{{ "size": 0, "query": {{ "bool": {{ "filter": [ {{ "term": {{ "Player": "Virat Kohli" }} }} ] }} }}, "aggs": {{ "yearwise_runs_scored": {{ "terms": {{ "field": "Year" }}, "aggs": {{ "total_runs": {{ "sum": {{ "field": "Runs" }} }} }} }} }} }}',
    },
    {
        "input": "Most matches played by players",
        "es_query": '{{ "size": 10, "query": {{ "match_all": {{}} }}, "sort": [ {{ "matches_played": {{ "order": "desc" }} }} ] }}',
    },
]
