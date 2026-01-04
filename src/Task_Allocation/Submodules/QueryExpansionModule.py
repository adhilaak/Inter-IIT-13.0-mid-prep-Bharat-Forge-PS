from Submodules.SubModuleLLM import BaseLLM
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

expandprompttemplate="""
Your role is to expand a question and provide a better version of that question.
Your provided question should have more details, and should be concise.
Simply expand the given question and provide a better one.
MAKE SURE YOUR OUTPUT IS A QUESTION.

Question:{query}
"""

expandtemfrom Submodules.SubModuleLLM import BaseLLM
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

expandprompttemplate="""
Your role is to expand a question and provide a better version of that question.
Your provided question should have more details, and should be concise.
Simply expand the given question and provide a better one.
MAKE SURE YOUR OUTPUT IS A QUESTION.

Question:{query}
"""

expandtemplate=ChatPromptTemplate.from_template(expandprompttemplate)

def expandQuery(query):
    expandchain=expandtemplate|BaseLLM().basellm|StrOutputParser()
    return expandchain.invoke({"query":query})