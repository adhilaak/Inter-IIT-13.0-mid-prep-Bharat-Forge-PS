from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
wikipediatool=WikipediaQueryRufrom langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
wikipediatool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

def search(query):
    return wikipediatool.run(query)