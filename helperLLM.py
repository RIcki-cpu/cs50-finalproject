from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

import prompt_templates as templates

template_personalities = templates.personalities

def get_reply_chatbot(personality, input_text, randomness = 0.0):
    """ USING LANGCHAIN DEFINE, DESIGN AND EXECUTE PROMPT"""

    #Expect key values of the MAP: emotions, wellbeing_level, answer, tokens
    response_as_dic = {} 

    #DEFINE SCHEMAS for the output parser
    emotions = ResponseSchema(name="emotions",
                              description="These are the emotions extracted from user's input")

    wellbeing_level = ResponseSchema(name="wellbeing_level",
                              description="Wellbeing in scale 1 to 10")

    chat_answer = ResponseSchema(name="answer",
                              description="reply to the user")

    response_schemas = [emotions,
                        wellbeing_level,
                        chat_answer]


    # FORMAT OUTPUT 
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    # MAIN PROMPT TEMPLATE FOR ADVICE GPT
    template = """{personality}
    {tasks}
    {format_instructions}
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


    #CHAIN DEFINITION using randomness parameter as temperature 
    chain = LLMChain(
    llm=ChatOpenAI(temperature = randomness, openai_api_key="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"),
    prompt=chat_prompt,
    )


    #DICCIONARY AS DICCIONARY
    with get_openai_callback() as cb:
        response_as_dic = output_parser.parse(chain.run({
            'personality': template_personalities[personality],
            'tasks': templates.tasks,
            'text' : input_text,
            'format_instructions': format_instructions
            }))
        #ADD number of tokens used
        response_as_dic["tokens"] = int(cb.total_tokens)
        #print(response_as_dic)


    return response_as_dic











