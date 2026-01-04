from langchain.prompts import ChatPromptTemplate
from Agents.AgentsLLM import AgentLLM
from langchain_core.output_parsers import StrOutputParser


relevanceprompttemplate="""
Your role is to check if the given solution successfully answers the query.
Simply say yes if it does and no if it does not.
Make sure the solution is of the same domain as the query and can be used to completely answer the query as well.
ONLY provide a "yes" or "no" answer.

Query:{query}

Solution:{solution}
"""

class OutputRelevanceBot:
    def __init__(self):
        self.relevancetemplate=ChatPromptTemplate.from_template(relevanceprompttemplate)
    
    def checkRelevance(self,query,answer):
        relevancechain=self.relevancetemplate|AgentLLM().basellm|StrOutputParser()
        return relevancechain.invoke({"query":query,"solution":answer})
