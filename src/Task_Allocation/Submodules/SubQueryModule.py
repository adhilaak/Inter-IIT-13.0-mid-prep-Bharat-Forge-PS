from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Submodules.SubModuleLLM import BaseLLM

multiquery_template="""Your main task is to take a query and divide it into {number} from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Submodules.SubModuleLLM import BaseLLM

multiquery_template="""Your main task is to take a query and divide it into {number} sub queries.
These subqueries should be coherent and relevent to the main query.
The main purpose of doing this is to make sure a broder scope of information can be gathered by the main query.
Only provide the subqueries in a numbered manner and nothing else.
The main query is {question}"""

multiquery_prompt=ChatPromptTemplate.from_template(multiquery_template)

def createSubQueries(query,number):
    subquerychain=multiquery_prompt|BaseLLM().basellm|StrOutputParser()|(lambda x:x.split('\n'))
    return subquerychain.invoke({"question":query,"number":number})