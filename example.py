import os

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

from langchain_logger.callback import ChainOfThoughtCallbackHandler
import logging

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


# Set up logging for the example
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create the Chain of Thought callback handler
cot= ChainOfThoughtCallbackHandler(logger=logger)


# Create a new OpenAI instance
llm = OpenAI(callbacks=[cot])


template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)


llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

result = llm_chain.invoke(question)

print(result)

