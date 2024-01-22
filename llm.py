import sys
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import re
import os
import openai  # pip install openai
import dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationSummaryBufferMemory # summarizes and keeps the conversation in memory
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate
)
from langchain.chains import LLMChain

import whisper
import tiktoken
import json
import transcript

# making chain stateful
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

dotenv.load_dotenv()


def try_whisper():
    model = whisper.load_model("tiny.en")
    result = model.transcribe("audio.mp3")
    print(result["text"])

# @read_file reads a file and returns the text 
def read_file(file_path, data_type="txt"):
  if data_type == "json":
      json_data = None
      with open(file_path, "r") as file:
        json_data = json.load(file)
      return json_data
# for text files which is the default
  with open(file_path, "r") as file:
      text = file.read()
  return text


def get_prompt():
    text = """I will give you a british parliamentary debating speech. You are a note taker, you will write a debate casebook. 
    There might be overlap between the speeches. If there is overlap of the transcript from the previous speaker,
    you should avoid it. Usually the following phrases indicate transition between speakers "Thank you for your speech.
    I would like to call _ of opposition/government/proposition/affirmative. Next speaker. 
    Thank you, Mr/Miss Speaker".
    You will extract a case out of the speech 
    transcript in the following structure. Use the structure for inspiration.Follow it strictly EXCEPT for the Arguments.
    The arguments should be implicitly following the given structure. 
                Stance: What the speaker  supports 
                Burden: What the speaker is aiming to prove
                Setup: How the speaker defines or sets up the debate
                Arguments: Each argument comprises of (Statement, Reasoning, Example) schema. You should be detailed and write an argument with these subpoints. 
                  1. Statement: What the argument is
                  2. Reasoning: Why the argument is true
                  3. Example: An example the speaker gave to support the reasoning
                  But do not write with these tags (statement,reasoning,example). Write these implicitly in your subpoints.
                 
                Premptive: What we say the opposition needs to do. 
                Rebuttal: What we say the opposition said and his counter argument. A rebuttal should have schema (They may/said: , We prempt/say: )
                Try to extract as many argument pairs as you can. Try to be detailed, use original language.
                You always answer the with markdown formatting. 
                You will be penalized if you do not answer with markdown when it would be possible.
                The markdown formatting you support: headings, bold, italic, links, tables, lists,
                code blocks, and blockquotes.
                Instruction on your writing:
                Avoid passive voice like : The speaker argues that change is inevitable.
                Instead write like: Change is inevitable.
    More guideline on style/writing:
    1. Be concise. Prefer short sentences.
    2. Use the speaker's phrases as much as possible.
    3. Write as if you are the speaker. Use first person. Don't write like "the speaker said X is true". 
    Write "X is true"
                Is that clear?
                
                Here's the transcript: {transcript}
                """

    return text



# def getYoutubeTranscript():
#     video_url = "https://www.youtube.com/watch?v=Ys0Sgicnjz4&t=951s"
#     audio_file = (
#         YouTube(video_url)
#         .streams.filter(only_audio=True)
#         .first()
#         .download(filename="audio.mp3")
#     )


def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# takes the filename of a transcript in json {speaker: 1, speech: "text"} and runs llm
def prompting_independently(filename):
  llm = ChatOpenAI()
  prompt_text = get_prompt()
  prompt = PromptTemplate.from_template(prompt_text)
  data = read_file(filename, data_type="json")
  notes = []
  
  for i,item in enumerate(data):
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"transcript": item["speech"]})
    # response = response.replace("\n", "")
    notes.append(f"Speaker {i} \n" + response)
    print("processed ", i, " ", len(response))
    # debug 
    
    
  # transcript.write_output(notes, "summaries/wudc_2016/finals-2.json")
  return notes

# Todo take input parameter of output_file instead of hardcoding
def write_md(notes:list, filename):
  # Define your input string
  input_string = "\n".join(notes)
  # Replace '\n' with line breaks and add indentation
  formatted_text = "\n".join("  " + line.strip() if line.strip() else "" for line in input_string.split("\n"))
  # formatted_text = re.sub(r'(\w+:)', r'\n**\1**', input_string)
   # Use re.sub to find and replace the "Speaker {i}:" format
  
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  # Save the formatted text to a Markdown file
  with open(filename, "w") as markdown_file:
      markdown_file.write(formatted_text)
  print("Formatted text saved to ", filename)

if __name__ == "__main__": # this only runs if this file is run as a main
  if len(sys.argv) != 2:# sys.argv
    raise ValueError("Please provide the filename of the transcript")
  filename = sys.argv[1]
  notes = prompting_independently(filename)
  write_md(notes, "output/" + "sample"  + ".md")
    # getYoutubeTranscript()
    # try_whisper()
