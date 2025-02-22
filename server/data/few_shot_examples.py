examples = [
    {
        "input": "Get me runs scored by Virat Kohli over the years",
        "es_query": '{{ "size": 10, "query": {{ "bool": {{ "filter": [ {{ "term": {{ "Player": "Virat Kohli" }} }} ] }} }}, "aggs": {{ "yearwise_runs_scored": {{ "terms": {{ "field": "Year" }}, "aggs": {{ "total_runs": {{ "sum": {{ "field": "Runs" }} }} }} }} }} }}',
    },
    {
        "input": "Most matches played by players",
        "es_query": '{{ "size": 10, "_source": ["Player", "Mat"], "query": {{ "match_all": {{}} }}, "sort": [ {{ "matches_played": {{ "order": "desc" }} }} ] }}',
    },
    {
        "input": "Get me the following stats by year - total runs, average strike rate, total fours, total sixes, total hundreds",
        "es_query": '{{"size": 10,"aggs":{{"season stats":{{"terms":{{"field":"Year","order":{{"_key":"asc"}}}},"aggs":{{"total_runs":{{"sum":{{"field":"Runs"}}}},"avg_strike_rate":{{"avg":{{"field":"SR"}}}},"total_fours":{{"sum":{{"field":"4s"}}}},"total_sixes":{{"sum":{{"field":"6s"}}}},"total_hundreds":{{"sum":{{"field":"100"}}}}}}}}}}}}',
    },
    {
        "input": "Show the top 10 players with the most runs in 2018",
        "es_query": "{{'size': 10, '_source': ['Player', 'Runs'], 'query': {{'bool': {{'filter': [{{'term': {{'Year': 2018}}}}]}}}}, 'sort': [{{'Runs': {{'order': 'desc'}}}}]}}",
    },
    {
        "input": "What is the average strike rate of players per year?",
        "es_query": "{{'size': 0, 'aggs': {{'average_strike_rate_per_year': {{'terms': {{'field': 'Year', 'order': {{'_key': 'asc'}}}}, 'aggs': {{'average_strike_rate': {{'avg': {{'field': 'SR'}}}}}}}}}}}}",
    },
    {
        "input": "Who hit the most centuries in 2022?",
        "es_query": "{{'size': 10, '_source': 'Player', '100'], 'query': {{'term': {{'Year': 2022}}}}, 'sort': [{{'100': {{'order': 'desc'}}}}]}}",
    },
    {
        "input": "How has the total number of fours and sixes changed over the years?",
        "es_query": "{{'size': 0, 'aggs': {{'fours_and_sixes_over_years': {{'terms': {{'field': 'Year', 'order': {{'_key': 'asc'}}}}, 'aggs': {{'total_fours': {{'sum': {{'field': '4s'}}}}, 'total_sixes': {{'sum': {{'field': '6s'}}}}}}}}}}}}",
    },
    {
        "input": "Who hit the most sixes in 2021?",
        "es_query": "{{'size': 10, '_source': ['Player', '6s'], 'query': {{'bool': {{'filter': [{{'term': {{'Year': 2021}}}}]}}}}, 'sort': [{{'6s': {{'order': 'desc'}}}}]}}",
    },
    {
        "input": "Which players had the best batting average in IPL history, considering only those who played at least 10 innings?",
        "es_query": "{{'size': 10, '_source': ['Player', 'Avg'], 'query': {{'bool': {{'filter': [{{'range': {{'Inns': {{'gte': 10}}}}}}]}}}}, 'sort': [{{'Avg': {{'order': 'desc'}}}}]}}",
    },
    {
        "input": "How have total runs and average strike rate changed over the years?",
        "es_query": "{{'size': 0, 'aggs': {{'yearly_stats': {{'terms': {{'field': 'Year', 'order': {{'_key': 'asc'}}}}, 'aggs': {{'total_runs': {{'sum': {{'field': 'Runs'}}}}, 'average_strike_rate': {{'avg': {{'field': 'SR'}}}}}}}}}}}}",
    },
    {
        "input": "Show total runs and average strike rate of Rohit Sharma over the years.",
        "es_query": "{{'size': 0, 'query': {{'bool': {{'filter': [{{'term': {{'Player': 'Rohit Sharma'}}}}]}}}}, 'aggs': {{'yearwise_stats': {{'terms': {{'field': 'Year', 'order': {{'_key': 'asc'}}}}, 'aggs': {{'total_runs': {{'sum': {{'field': 'Runs'}}}}, 'average_strike_rate': {{'avg': {{'field': 'SR'}}}}}}}}}}}}",
    },
    {
        "input": "How many times have players remained not out compared to the total innings played each year?",
        "es_query": "{{'size': 0, 'aggs': {{'not_out_vs_innings_per_year': {{'terms': {{'field': 'Year', 'order': {{'_key': 'asc'}}, 'size': 1000}}, 'aggs': {{'total_not_outs': {{'sum': {{'field': 'NO'}}}}, 'total_innings': {{'sum': {{'field': 'Inns'}}}}}}}}}}}}",
    },
]
