from Submodules import QueryRewriteModule

class QueryRewriteBot:
    def __init__(self):
        pass

    def rewriteQuery(self,query,documents):
        return QueryRewriteModule.rewriteQuery(query=query,documents=documents)
