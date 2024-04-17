"""
This Module contains the implementation of agent that converses with human
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Dict

import os
import json

# Works only for linux or max if 'pip install jq is performed'
# loader = JSONLoader(data_path,
#                     jq_schema = ".contents",
#                     text_content = False,
#                     json_lines = True)


class ChatAgent():
    '''
    Defining a class for the agent
    
    
    '''

    def __init__(self, text = "You are a Chatbot.", specialize = 'cell_biology',chuncks = 300,custom_file = ".pdf"):
        self.initial_text = text
        self.chat_history = ChatMessageHistory()
        self.chat_history2 = ChatMessageHistory()
        self.custom = False
        self.store = []
        
        if specialize == 'cell_biology':
            self.data_path = os.path.join(os.getcwd(),'data','Cell_Biology_Alberts.jsonl')
        elif specialize == 'psichiatry':
            self.data_path = os.path.join(os.getcwd(),'data','Neurology_Adams.jsonl')
        elif specialize == 'custom':
            self.custom = True
            self.custom_file = custom_file
            self.data_path = os.path.join(os.getcwd(),'data',custom_file)
        self.number_of_chunck = chuncks


    def initialize(self, text):
        
        self.llm = ChatGoogleGenerativeAI(model = "gemini-pro",temperature = 0.55)
        self.prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                 text + "Following are the context passages: \n\n{context}\n"
            ),      

            MessagesPlaceholder(variable_name="messages"),
        ]
        )
        self.document_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.retriever = self.retrieve(self.data_path).as_retriever(search_kwargs={'k': 2})



        self.retrieval_chain = RunnablePassthrough.assign(
            context=self.parse_retriever_input | self.retriever).assign(
                answer = self.document_chain,
            )
        

    def build_context(self, msg, type):

        if type == 'h':
            self.chat_history = ChatMessageHistory()
            self.chat_history.add_messages(
                self.chat_history2.messages)
            
            self.chat_history.add_user_message(
        "k = Is the following question related to the context passages?\n"
        # "k = Can the following question be accurately answered from the context passages?\n"
        f"Question: {msg}\n" 
        "If k == True: answer in one sentence using the context passages as your knowledge base(without showing k).\n"
        "If k == False: reply with a casual message asif you don't know(without showing k)."
            )
            self.chat_history2.add_user_message(msg)

        else:
            
            self.chat_history2.add_ai_message(msg)


    def update_state(self):
        pass


    def parse_retriever_input(self,params: Dict):
        return params["messages"][-1].content

    def should_call(self, input_msg):

        response = self.llm.invoke(f"'Message: {input_msg}' \n Does the message asks to call the user? Answer only Yes or No.'")
        # print(response.content)
        return response.content.startswith('Yes')


    def conversation_form(self):
        name = input("AI: What's your name?\nYou: ")
        phone_number = input("AI:What's your phone number?\nYou: ")
        email = input("AI:What's your email address?\nYou: ")
        self.store.append((name,phone_number,email))
        


    def reply(self, input_msg):
        self.initialize(self.initial_text)
        if self.should_call(input_msg):
            self.conversation_form()
            return "Thanks for the information! I'll remember to call you."

        else:
            self.query = self.build_query(input_msg)
            self.build_context(self.query, 'h')


            response = self.retrieval_chain.invoke(
                {
                    "messages": self.chat_history.messages,
                }
            )

            # print(response)
            self.build_context(response['answer'], 'ai')

            return response['answer']

    
    def retrieve(self, file):

        if self.custom:
            loader = PyPDFLoader(file)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            data_splits = text_splitter.split_documents(documents)
        else:
            with open(file, 'r') as f:
            # Load each line into a list
                lines = f.readlines()

            # Convert each line to a dictionary using json.loads
            json_list = [json.loads(line) for line in lines]
            data_splits = [Document(page_content = data['content'])
                                    # ,metadata = {'id': data['id'], 'title':data['title']}) 
                            for data in json_list]

        vectorstore = Chroma.from_documents(documents = data_splits[:self.number_of_chunck], 
                                            embedding = GoogleGenerativeAIEmbeddings(model = "models/embedding-001"),
                                            # persist_directory="data/"
                                            )       
        return vectorstore
    
    def build_query(self, msg):

        # You can implement a function to build better query from input message or questions!

        return msg


    def process_input(self):
        pass



    