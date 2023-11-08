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


def read_openai_key():
    '''Here you must import your personal private OPENAI_API_KEY at  https://openai.com/product '''
    file_path = "openai_key.txt"  # Replace with the path to your text file
    try:
        with open(file_path, "r") as file:
            # Read the first line
            openai_api_key = file.readline()

            # Close the file
            file.close()

        return openai_api_key
    except FileNotFoundError:
        print("File not found. Please provide a txt file with your openai_api_key.")
    except Exception as e:
        print("An error occurred:", str(e))


def get_reply_chatbot(personality, input_text, randomness = 0.0):
    """ USING LANGCHAIN DEFINE, DESIGN AND EXECUTE PROMPT"""

    # Expect key values of the MAP: emotions, wellbeing_level, answer, tokens
    response_as_dic = {} 

    # DEFINE SCHEMAS for the output parser
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

    # CHAIN DEFINITION using randomness parameter as temperature
    chain = LLMChain(
    llm=ChatOpenAI(temperature = randomness, openai_api_key=read_openai_key()),
    prompt=chat_prompt,
    )

    # DICTIONARY AS DICTIONARY
    with get_openai_callback() as cb:
        response_as_dic = output_parser.parse(chain.run({
            'personality': template_personalities[personality],
            'tasks': templates.tasks,
            'text': input_text,
            'format_instructions': format_instructions
            }))
        # ADD number of tokens used
        response_as_dic["tokens"] = int(cb.total_tokens)

    return response_as_dic











