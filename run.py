import os

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from typing import Optional, List # to define a Json class
from pydantic import BaseModel, Field ,ValidationError # pydantinc data parser
from datetime import datetime
from langchain_core.output_parsers import PydanticOutputParser
from datetime import datetime




date = datetime.today().strftime('%Y-%m-%d') # Storing Today's date

def main():
    # JSON Class
    class Entity(BaseModel):
        entity: Optional[str] = Field(description="Name of the Entity.")
        parameter: Optional[str] = Field(description="Parameter of the Entity.")
        start: Optional[datetime] = Field(description="Start Date of the Parameter.")
        end: Optional[datetime] = Field(description="End Date of the Parameter")

    class Entities(BaseModel):
        entities: List[Entity] 
    # Instantiating the Model
    groq_api_key = os.environ['GROQ_API_KEY']
    model = 'llama3-8b-8192'
    groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model
    )
    #Instantiating the Parser
    parser = PydanticOutputParser(pydantic_object=Entities)

    
    print("Hello! I am your parser, What do you want to look into today? Please give a company name with a matric")
    # Accomodating prompt to have two more input variables, today's date and the conversation history
    system_prompt = '''
            {chat_history}
            You are an expert data parser. Parse data from user query and store them in following fields.

            1. Entities (Company names mentioned in the query).
            2. Parameter (Performance metric requested, e.g., revenue, profit, etc. Should be same for all entities in a query).
            3. Start Date (Beginning of the requested Time period start for the metric requested. Should be same for all entities in a query).
            4. End Date (Ending of the requested Time period end for the metric requested. Should be same for all entities in a query).
            6. If the query mentions relative dates (e.g., "last quarter", "previous month"), convert these into exact calendar dates.
            7. If Period in not specified start date should be one year ago and end date should be today. Today is {date}
            If you don't know any field then set it to None.
            Our question is 
            {human_input}
            Format instructions:
            {format_instructions}
            '''  
    # Defining The prompt template with the required inputs
    prompt = PromptTemplate(
            template=system_prompt,
            input_variables=["human_input","date", "chat_history" ],
            partial_variables={"format_instructions": parser.get_format_instructions()},
            ) 
    # Defining the conversational memory
    conversational_memory_length = 1000 
    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history",  input_key="human_input", return_messages=True)


    while True:
        query = input("Ask a question: ")

        if query:
            # Passing the input paramets in formatted prompts
            _input = prompt.format_prompt(human_input=query, date = date, chat_history = memory)
            # Passing parameters to the chain
            conversation = LLMChain(
                llm=groq_chat,  
                prompt=prompt,  
                verbose=False,   
                memory=memory,  
            )
            
            try:
                # Try to get a response
                response = conversation.predict(human_input=_input.to_string(), date = date)
                output = parser.parse(response)
                dc = output.dict()
                for entity in dc['entities']: ## converting date time formats
                    entity['start'] = entity['start'].strftime('%Y-%m-%d')
                    entity['end'] = entity['end'].strftime('%Y-%m-%d')
                print("Chatbot:", dc['entities'])
            except:
                # Else throw Error
                print("Ran into a problem while parsing, please try again") 

if __name__ == "__main__":
    main()