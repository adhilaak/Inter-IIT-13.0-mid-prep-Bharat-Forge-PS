from langchain.prompts import ChatPromptTemplate
from Agents.AgentsLLM import AgentLLM
from langchain_core.output_parsers import StrOutputParser

relevanceprompttemplate="""
Your role is to check if the given context is relevant to the query.
Simply say yes if it is and no if it is not.
Make sure the context is of the same domain as the query and can be used to answer the query as well.
ONLY provide a "yes" or "no" answer.

Query:{query}

Context:{context}
"""

class DocumentRelevanceBot:
    def __init__(self):
        self.relevancetemplate=ChatPromptTemplate.from_template(relevanceprompttemplate)
    
    def checkRelevance(self,query,context):
        relevancechain=self.relevancetemplate|AgentLLM().basellm|StrOutputParser()
        return relevancechain.invoke({"query":query,"context":context})
