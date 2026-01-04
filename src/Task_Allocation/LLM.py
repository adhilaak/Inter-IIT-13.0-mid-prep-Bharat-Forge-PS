from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import subprocess
import sys

from dotenv import load_dotenv
import os

from Agents.QueryRouter import QueryRouterBot
from Agents.DocumentRelevanceChecker import DocumentRelevanceBot
from Agents.OutputRelevanceChecker import OutputRelevanceBot
from Agents.VectorStoreRetriever import RetrieverBot
from Agents.QueryRewriter import QueryRewriteBot
from Agents.Generator import GeneratorBot

load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")

text_loader_kwargs={'encoding':'UTF-8'}
directory=DirectoryLoader(path="Documents",loader_cls=TextLoader)
documents=directory.load()


text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=1)
chunks=text_splitter.split_documents(documents=documents)


embedder=GoogleGenerativeAIEmbeddings(model='models/embedding-001',google_api_key=api_key)
vectorstore=FAISS.from_documents(documents=chunks,embedding=embedder) #CHANGE DOCUMENTS TO CHUNKS(VERY SLOW)

k=1
retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":1})


def RewriteQuery(query,documents):
    rewriter_bot=QueryRewriteBot()
    return rewriter_bot.rewriteQuery(query,documents)

def GenerateAnswer(query,documents):
    generator_bot=GeneratorBot()
    return generator_bot.generate(query=query,documents=documents)

def VectorStoreRetrieval(queries,retriever):
    retriever_bot=RetrieverBot()
    return retriever_bot.retrieveDocuments(queries=queries,retriever=retriever)

def RouteQuery(query):
    #subqueries=CreateSubqueries(query=query,num=2)
    subqueries=query

    #Source Decision
    router_bot=QueryRouterBot()
    source=router_bot.routeQuery(query)

    documents=VectorStoreRetrieval(subqueries,retriever)

    #Generate Answer
    if("vectorstore" in source):
        answer=GenerateAnswer(query=query,documents=documents)
    else:
        answer=RewriteQuery(query=query,documents=documents)


    return answer
    
#The main code
xpositions = []
ypositions = []
urgencies = [] 

userinput=""
'''print("WELCOME TO THE COMMAND TERMINAL")

print("ENTER ALL CO-ORDINATE TASKS IN (X,Y,Priority) FORMAT (PRINT EXIT WHEN DONE)")
while True:
    user_input = input()
    if("exit" in user_input.lower()):
        break

    else:
        order = eval(user_input)
        xpositions.append(order[0])
        ypositions.append(order[1])
        urgencies.append(order[2])

print("ENTER ALL ITEM TASKS (Example:- Go to fire extinguisher)")
while(True):
    userinput=input("Enter Command: ")
    print("Processing Query :",userinput)
    if("exit" in userinput.lower()):
        print("EXITING")
        break
    return_string = RouteQuery(userinput)
    token = return_string.splitlines()
    pos = eval(token[0])
    urgency = int(token[2])
    print(pos)
    print(urgency)
    xpositions.append(pos[0])
    ypositions.append(pos[1])
    urgencies.append(urgency)

print(xpositions)
print(ypositions)
print(urgencies)

#Create a new command line command
command = ["python3.9","Allocator.py"]
for i in range(0,len(urgencies)):
    command.append(str(xpositions[i]))
    command.append(str(ypositions[i]))
    command.append(str(urgencies[i]))

print(command)

#R
try:
    result = subprocess.run(command,capture_output=True,text=True,check=True)
    


except subprocess.CalledProcessError as e:
    print("Error:")
    print(e.stderr)
'''
item = False
for i in range(1,len(sys.argv)):
    print(sys.argv[i])
    if(sys.argv[i]==':'):
        print("Next")
        item = True
        continue

    if(item == False):
        order = eval(sys.argv[i])
        xpositions.append(order[0])
        ypositions.append(order[1])
        urgencies.append(order[2])
    
    elif(item == True):
        print("Processing Query :",sys.argv[i])
        if("exit" in userinput.lower()):
            print("EXITING")
            break
        return_string = RouteQuery(sys.argv[i])
        token = return_string.splitlines()
        pos = eval(token[0])
        urgency = int(token[2])
        print(pos)
        print(urgency)
        xpositions.append(pos[0])
        ypositions.append(pos[1])
        urgencies.append(urgency)

#Create a new command line command
command = ["python2","Allocator.py"]
for i in range(0,len(urgencies)):
    command.append(str(xpositions[i]))
    command.append(str(ypositions[i]))
    command.append(str(urgencies[i]))

print(command)
try:
    result = subprocess.run(command,capture_output=True,text=True,check=True)
    
except subprocess.CalledProcessError as e:
    print("Error:")
    print(e.stderr)
