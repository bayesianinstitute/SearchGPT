import os
import json
import google.generativeai as genai
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


def get_answer_box(query):
    print("parsed query: ", query)

    search = GoogleSearch({
        "q": query, 
        "api_key": os.getenv('SERPAPI_API_KEY')
    })
    result = search.get_dict()
    
    if 'answer_box' not in result:
        return "No answer box found"
    
    return result['answer_box']

get_answer_box_declaration = {
    'name': "get_answer_box",
    'description': "Get the answer box result for real-time data from a search query",
    'parameters': {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query to search for"
            }
        },
        "required": [
            "query"
        ]
    },
}

prompt = "who won more medal in 2024 olyphmic?"
# prompt = "Morning! how is Tesla stock doing today? I just bought some shares yesterday."

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(
    prompt,
    tools=[{
        'function_declarations': [get_answer_box_declaration],
    }],
)

function_call = response.candidates[0].content.parts[0].function_call
args = function_call.args
function_name = function_call.name
if function_name == 'get_answer_box':
    result = get_answer_box(args['query'])

    data_from_api = json.dumps(result)[:5000]
else: 
    data_from_api=""

print("Data from Search : ",data_from_api)
response = model.generate_content(
    """
    Based on this information: `""" + data_from_api + """` 
    and this question: `""" + prompt + """`
    respond to the user in a friendly manner.
    """,
)
print(response.text)


