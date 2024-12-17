To Run this in your local Computer

Clone the repor from GitHub

Install the necessary dependencies

"""pip innnstall langchain langchain_groq"""

Visit this link to get your API Key:

""" https://console.groq.com/keys """

Save the Key in an environment variable like this

""" export GROQ_API_KEY=<your-api-key-here> """

Run the application

"""python3 run.py"""

The code uses a version 1 langchain and the LLM Chain is due for depreciation

Functionality:

The model extracts perfomance matrices,
start and end date of the matrices, and
the company name from a user query using
langhain and llama3-8b-8192, and exports
them in a json format using Pydantic
Output Parser. The application has a
conversational memory and it is able to
ompare results with previous queries and
can return multiple JSON objects as a
response. The model takes the last year
as the period if no date is specified,
and has partial support for spelling
mistakes and relative date ranges like
month, week, quarter and such

# JSONExtractor

Example: <br/>

User: Get me FlipKart's Profit for the last year
<br/>
Output:
[{
"entity": "FlipKart",
"parameter": "Profit",
"start": "2024-12-17",
"end" : "2023-12-17",
}] <br/>

User: Compare this with Amazon <br/>
Output: [{
"entity": "FlipKart",
"parameter": "Profit",
"start": "2024-12-17",
"end" : "2023-12-17",
},
{
"entity": "Amazon",
"parameter": "Profit",
"start": "2024-12-17",
"end" : "2023-12-17",
}]
