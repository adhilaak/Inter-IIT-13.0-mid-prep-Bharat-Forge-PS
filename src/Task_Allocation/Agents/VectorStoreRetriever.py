from Agents.AgentsLLM import AgentLLM

class RetrieverBot:
    def __init__(self):
        self.llm=AgentLLM().basellm #Currently Useless

    def retrieveDocuments(self,queries,retriever):
        docs=[]
        for i in queries:
            if(len(i)!=0):
                docs.append(retriever.invoke(i))
        return docs

