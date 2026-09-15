from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
)

model=ChatHuggingFace(llm=llm)

parser=StrOutputParser()

template=PromptTemplate(
    template="""Answer the user's question using ONLY the provided webpage content.

If the answer is present in the webpage content, answer directly.
If the answer is not present, say that the information is not available on the page.

Webpage content:
{page_text}

User question:
{question}""",
    input_variables=['page_text','question']
)



class AskRequest(BaseModel):
    url:str = Field(description="url of the webpage")
    question:str = Field(description="question of the user")


chain= template|model|parser
print("1. Chain created")


@app.post("/ask")

def ask(askreq:AskRequest):
    response={
        "url":askreq.url,
        "question":askreq.question
    }
    print("1. Request received")
    loader=WebBaseLoader(askreq.url)
    print("2. Loader created")
    try:
        data=loader.load()
        print("3. Page loaded")
        print(data[0].page_content)
        result=chain.invoke({"page_text":data[0].page_content[:8000] ,"question":askreq.question})
        print("5. LLM response received")
        return {"answer":result}
    except Exception as e:
        print(f"Error loading {e}")
        return {"answer":"Sorry, I couldn't load this page. It might be blocking access or have complex content."}
    
    
    
    

