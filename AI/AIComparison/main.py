from openai import OpenAI
from google import genai
from anthropic import Anthropic
from huggingface_hub import InferenceClient
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
# from huggingface import HuggingFace
# from azure import Azure
# from cohere import Cohere
# from ai21 import AI21
# from llama import Llama
# from xgen import XGen
# from llama_cpp import LlamaCpp
from dotenv import load_dotenv
import os

load_dotenv()

# print("Environment Variables Loaded: ", env)

def openai_api_chat(model="gpt-4.1", api_key=os.getenv("OPENAI_KEY"), input_text=""):
    
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model,
        input=input_text
    )

    print("OpenAI ChatGPT reponse: ", response.output_text, "\n")
    return model, response, response.output_text, input_text

def google_api_chat(model="gemini-2.0-flash", api_key=os.getenv("GOOGLE_KEY"), input_text=""):

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model, contents=input_text
    )
    print("Google Gemini reponse: ", response.text, "\n")
    return model, response, response.text, input_text

def anthropic_api_chat(model="claude-3-7-sonnet-20250219", api_key=os.getenv("ANTHROPIC_KEY"), input_text=""):

    client = Anthropic(
    api_key=api_key,
    )

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello, Claude"}
        ]
    )
    print(message.content)

def huggingface_chats(api_key=os.getenv("HUGGINGFACE_KEY"), prompt= ""):

    client = InferenceClient(
        
        api_key=api_key
    )

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=messages,
        temperature=2,
        max_tokens=600,
        top_p=1,
    )

    print("Meta llama response: ", completion.choices[0].message.content, "\n")

def deepseek_chat(api_key=os.getenv("DEEPSEEK_KEY"), prompt=""):

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    print("Deepseek response: ", response.choices[0].message.content, "\n")

if __name__ == "__main__":
    prompt = "Which ai model is the best?"
    openai_api_chat(input_text=prompt)
    google_api_chat(input_text=prompt)
    huggingface_chats(prompt=prompt)
    deepseek_chat(prompt=prompt)
