from Agents.AgentsLLM import AgentLLM
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class QueryRouterBot:
    def __init__(self):
        self.llm=AgentLLM().basellm
        self.routequerytemplate="""
        You are a query router. Your job is to decide whether the query should be answered by the web or not.
        If the query is related to items and their positions, output the word 'vectorstore'.
        Otherwise output 'command'

        Query:{query}
        """
        self.routetemplate=ChatPromptTemplate.from_template(self.routequerytemplate)

    def routeQuery(self,query):
        routingchain=self.routetemplate|self.llm|StrOutputParser()
        return routingchain.invoke({"query":query})
