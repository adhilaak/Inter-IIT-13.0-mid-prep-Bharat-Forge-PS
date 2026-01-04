from Agents.AgentsLLM import AgentLLM
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

generatorprompttemplate="""
Based on the given query and context. Provide an answer.
Make sure there is no illegal or inhumane content in your answer.
If the context is not relevant to the query, ignore the context.

Query:{query}

Context:{documents}
"""

class GeneratorBot:
    def __init__(self):
        self.generatorprompt=ChatPromptTemplate.from_template(generatorprompttemplate)

    def generate(self, query, documents):
        generator_chain=self.generatorprompt|AgentLLM().basellm|StrOutputParser()
        return generator_chain.invoke({"query":query,"documents":documents})
