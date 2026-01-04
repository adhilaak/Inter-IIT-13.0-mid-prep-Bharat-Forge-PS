from Submodules.SubModuleLLM import BaseLLM
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

rewriteprompttemplate="""
You will be provided a query for destination items and/or (x,y) co-ordinates to go to.
If items as well as (x,y) co-ordinates are in the query consider them as separate positions.

Query:{query}

Context:{context}

Extract the level of urgency of the query and categorise it from 0 to 10, 10 being very urgent.

If the destination cannot be found, return "DESTINATION NOT FOUND"
If the query contains a time gap, set task priority to "0"


IF MULTIPLE ITEMS AND/OR CO-ORDINATES ARE GIVEN, FOLLOW THE NEXT GUIDELINES FOR EACH ITEM.
Structure the query in the given format STRICTLY and return it:

(Enter the co-ordinates of the item, or )
(If the destination item is given, enter it's name here or simply enter "General" or if raw co-ordinates then write General)
(Enter the numerical urgency here)
"""

rewritetemplate=ChatPromptTemplate.from_template(rewriteprompttemplate)

def rewriteQuery(query,documents):
    rewritechain=rewritetemplate|BaseLLM().basellm|StrOutputParser()
    return rewritechain.invoke({"query":query,"context":documents})
