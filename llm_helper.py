from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()
key = os.getenv("groq_api_key")
llm = ChatGroq(api_key = key , model = "llama-3.3-70b-versatile")

if __name__ == '__main__':
    response = llm.invoke('Please tell me the 2 important ingredients of Fruit Chat')
    print(response.content)