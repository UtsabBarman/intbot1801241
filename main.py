
import os
import json
import streamlit as st
from dotenv import load_dotenv
from itertools import zip_longest
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from ChatGPT35TurboZeroShotPrompts import ChatGPT35

from LinkedinModel import LinkedinInstance

os.environ["OPENAI_API_KEY"] = "OPEN_API_KEY"

chat = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo"
)

IDX = 0

def build_message_list(question:str):
    zipped_messages = [
        SystemMessage(
            content= "You will be provided with a set of questions for a job interview. "
                      "Your task is to ask three interview questions as an interviewer. Only ask from the given target questions."
                     f"Start by greeting the candidate by saying - Hello, I am Interview bot ... "
                     f'target questions:{question}')
    ]
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if ai_msg is not None:
            zipped_messages.append(
                AIMessage(content=ai_msg)
            )
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg)
            )
    return zipped_messages


def generate_response(question:str):
    zipped_messages = build_message_list(question=question)
    ai_response = chat(zipped_messages)
    return ai_response.content


def submit():
    global IDX
    st.session_state.entered_prompt = st.session_state.prompt_input
    st.session_state.prompt_input = ""
    IDX += 1


def get_questions():
    load_dotenv()
    with open("./config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    gpt = ChatGPT35()
    gpt.inits(key=config.get("openai_api_key"))

    # Set streamlit page configuration

    profile = None
    linkdin_inst = LinkedinInstance(
        usr="LINKEDIN_USERNAME",
        pwd="LINKEDIN_PASSWORD",
        gpt=gpt
    )
    if os.path.exists("./profile.json"):
        st.write("Profile Exists ...")
        with open("./profile.json", 'r', encoding="utf-8") as f:
            profile = json.load(f)

    else:
        st.write("Creating Profile from Linkedin ...")
        p = linkdin_inst.get_linkedin_data(pub_url="https://www.linkedin.com/in/utsabbarman/")
        profile = linkdin_inst.get_refined_profile(profile=p, temp=0.5, wc=500)
        with open("./profile.json", "w", encoding="utf-8") as f:
            json.dump(profile, f)

    job_des = linkdin_inst.get_job_description(
        jobid="3780193875"
    )

    questions = gpt.generate_interview_questions(
        your_profile=profile,
        job_des=job_des,
        temp=0.6,
        wc=800,
        extra_text=""
    )
    return [e.get("q") for e in eval(questions)][:3]

if __name__ == '__main__':

    st.set_page_config(page_title="OpenAIInterviewBot")
    st.title("Interview Bot")
    st.subheader("Try to answer with more context. If you want to switch to new question ask -'next question', if you want to end the interview ask -'end the interview'")
    questions = get_questions()

    # Initialize session state variables
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []  # Store AI generated responses

    if 'past' not in st.session_state:
        st.session_state['past'] = []  # Store past user inputs

    if 'entered_prompt' not in st.session_state:
        st.session_state['entered_prompt'] = ""  # Store the latest user input


    st.text_input('Your Response: ', key='prompt_input', on_change=submit)


    if st.session_state.entered_prompt != "":
        # Get user query
        user_query = st.session_state.entered_prompt


        # Append user query to past queries
        st.session_state.past.append(user_query)


        # Generate response
        output = generate_response(question=questions[IDX])


        if IDX == len(questions):
            output = "Many Thanks. Lets the end of this interview."
        # Append AI response to generated responses
        st.session_state.generated.append(output)


    # Display the chat history
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            # Display user message
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            # Display AI response
            message(st.session_state["generated"][i], key=str(i))
