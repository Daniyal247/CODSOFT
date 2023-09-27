# #!pip install requests beautifulsoup4
# #!pip install autocorrect
import re
import requests
from bs4 import BeautifulSoup
from autocorrect import Speller
import streamlit as st
from datetime import datetime
import random

bot_response = ""

def get_bot_response(prompt):
    resp = "I'm sorry, I don't understand. Can you please rephrase or ask another question?"
    prompt = prompt.lower()
    prompt = spelling_correction(prompt)

    # Define some simple rules and responses
    if re.search(r"(hello|hey|hi)", prompt):
        resp = "Hello! How can I assist you today?"

    elif re.search(r"(how are you|how are you doing|how is everything)", prompt):
        resp = "I'm good thank you, How are you? And how can I help you?"

    elif re.search(r"(weather|clouds|atmosphere|temperature)", prompt):
        url = 'https://www.bbc.com/weather/1174872'
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.text
            # Parse the HTML content
            soup = BeautifulSoup(data, 'html.parser')
            span = soup.find('span', class_="wr-value--temperature--c")
            if span:
                temperature = span.get_text()
                resp = f"The weather is okay and the temperature outside is: {temperature}"

    elif re.search(r"(cold outside\?)", prompt):
        resp = "Well, I'm not really sure, but you can ask for the temperature if you want because judging it is not for me."

    elif re.search(r"(date and time|current time|time|date)", prompt):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        resp = f"The current date and time is: {current_time}"

    elif re.search(r"(bye|goodbye)", prompt):
        resp = "Goodbye! Have a great day!"

    elif re.search(r"(okay|ohkayy|ohkay|ok|k)", prompt):
        resp = "yepp it is what it is."

    elif re.search(r"(legend|name of legend)", prompt):
        resp = "There are many legends throughout the history of this planet but my personal favorites are *Jaun Elia* and Nusrat *Fateh Ali Khan*."

    elif re.search(r"(how many pillars of islam)", prompt):
        resp = "there Five Pillars of Islam: Shahada, Salah, Zakat, Sawm, and Hajj."

    elif re.search(r"(a peice of jaun|work of Jhon Elia|some poetry|some piece of art|poetry)", prompt):
        num = random.randint(0, 4)
        poetry = ["Har Haal meh hasne ka hunar paas tha jinke,  \t Woh rone lage hain toh koi baat toh hogi", 
                  "Yeh hain Ehl-e-dunya k Dilchasp Dhoke,  \t Yahaan kisi ko kisi seh muhabbat nhi hai!", 
                  "Mein ehem tha,  \t yehi wehem tha", 
                  "Itna karee hogaya tha,  \t Mujhe laga mera hogaya tha", 
                  "sookhe patto ki tarha bikhre hue thei hum,  \t kisi neh sameta bhi toh sirf jalane k liye"]
        resp = poetry[num]

    elif re.search(r"(what\s+is\s+your\s+name)", prompt):
        resp = "Well, I don't really have a name, but I'm DaniBot."

    elif re.search(r"(how\s+to\s+stay\s+calm\s+and\s+positive)", prompt):
        resp = "To stay calm and positive, you can try the following:\n1. Practice mindfulness and meditation.\n2. Exercise regularly to release endorphins.\n3. Maintain a healthy diet.\n4. Get enough sleep.\n5. Engage in hobbies and activities you enjoy.\n6. Practice deep breathing exercises.\n7. Surround yourself with positive people.\n8. Focus on gratitude and positive thinking."

    elif re.search(r"(my\s+name\s+is\s+(\w+))", prompt):
        match = re.search(r"(my\s+name\s+is\s+(\w+))", prompt)
        if match:
            user_name = match.group(2)
            resp = f"Oh, nice to meet you, {user_name}!"

    return resp

def spelling_correction(user_input):
    spell = Speller(lang='en')
    user_input = spell(user_input)
    return user_input

st.title("Dani Chat Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Enter Text")

if not st.session_state.get("greeted", False):
    resp = "Hello! I am Dani, your friendly chatbot. How can I assist you today?"
    st.session_state.greeted = True
else:
    bot_response = get_bot_response(prompt)

if prompt:
    # Display user input in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})


if prompt and prompt.lower() == "exit":
    bot_response = "Goodbye! Have a great day!"

if bot_response:
    response = f"Chatbot: {bot_response}"
else:
    response = "Chatbot: Hello! I am Dani, your friendly chatbot. How can I assist you today?"

# Display assistant response in chat message
with st.chat_message("assistant"):
    st.markdown(response)
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})
