
import streamlit as st 
import openai
from PIL import Image

import uuid
import pickle
from openai import OpenAI
import os 
os.environ["OPENAI_API_KEY"] = ""
client = OpenAI()



avatar_bot = Image.open(r"utils\logo_gold_Icon.png")
avatar_user = Image.open(r"utils\logo_white_icon.png")




def chat_titles(messages):
    user_content = ""
    for message in messages:
        if message['role'] == 'user':
            user_content += message['content']
    if user_content != "":
        promt = f'''- create a conversation thumbail/topic based on the following user request {user_content}
                    super short 
                    - example : for a conversation about python and flask thumbnail should be :  "python flask implementation."
                    - your output should be only the title/thumbnail/topic 
                    - your answerr will be used to name a file so do not use sybbols semi colon and so on'''
        
        params = chat_message([HumanMessage(promt)],temperature = 0,stream=False)
        _thumbnail = client.chat.completions.create(**params)
        thumbnail = _thumbnail.choices[0].message.content
    else:
        thumbnail = "empty chat"
    return thumbnail

    






def chat_message(messages,temperature = 0.5,stream = True):
        

        return {
            "model": "gpt-4-1106-preview",
            "messages": messages,
            
            "max_tokens": 4096,
            "temperature": temperature,
            "stream":stream
        }



def  AIMessage(content):
    return {'role':'assistant', 'content':content}    

def HumanMessage(content):
    return {'role':'user', 'content':content}

def init_page():
    st.set_page_config(
        page_title="MinckaGPT"
    )
    
    st.markdown(
        f"""
        <style>
            body {{
                background-color: #cd0000;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
 



def select_model():
    # model_name = st.sidebar.radio("Choose LLM:",
    #                               ("gpt-3.5-turbo-16k", "gpt-4", "Web Search Agent","PDF Loader","Mincka Agent"))
    temperature = st.sidebar.slider("Temperature:", min_value=0.0,
                                    max_value=1.0, value=0.0, step=0.01)
    return temperature


# Load the image using PIL
logo_image_path = "utils/Gold Logo White Text Transparent.png"
logo_image = Image.open(logo_image_path)

# Specify the desired width while maintaining the aspect ratio
desired_width = 450
aspect_ratio = desired_width / float(logo_image.size[0])
new_height = int(float(logo_image.size[1]) * aspect_ratio)

# Resize the image using high-quality resampling
logo_image_resized = logo_image.resize((desired_width, new_height), Image.LANCZOS)

# Display the resized image in Streamlit
st.image(logo_image_resized, use_column_width=False, channels="RGB")


st.header("MinckaGPT")
st.sidebar.title("Options")


_content = "You are a helpful AI assistant. Respond your answer in mardkown format and in Australina english."
def init_messages(content = _content):
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            # SystemMessage(
            #     content=_content)
            {'role':'system', 'content':content}
        ]

    if clear_button:
        saved_filename = save_conversation()  # Save current conversation
        # st.sidebar.button(f"Conversation {saved_filename}", key=saved_filename)  # Display saved conversation as a button
        st.session_state.messages = [{'role':'system', 'content':content}]


def save_conversation():
    """Saves the current conversation using pickle with a unique filename."""
    if "messages" in st.session_state:
        # try:
        thumbnail = chat_titles(st.session_state.messages)
        # thumbnail = result.choices[0].message.content
        print(thumbnail )
        filename = f"conversations/{thumbnail}.pkl"
        with open(filename, 'wb') as file:
            pickle.dump(st.session_state.messages, file)
        return filename
        # except:
        #     filename = f"conversations/{uuid.uuid4()}.pkl"
        #     with open(filename, 'wb') as file:
        #         pickle.dump(st.session_state.messages, file)
        #     return filename

    return None

def load_conversation(filename):
    """Loads a conversation from a given file."""
    with open(f"{filename}", 'rb') as file:
        return pickle.load(file)

def display_saved_conversations():
    """Displays saved conversations in the sidebar for selection."""
    
    conversation_dir = 'conversations'
    saved_conversations = [f for f in os.listdir(conversation_dir) if f.endswith('.pkl')]
    # Sort files by last modification time, newest first
    saved_conversations.sort(key=lambda x: os.path.getmtime(os.path.join(conversation_dir, x)), reverse=True)
    for file in saved_conversations:
        file_without_extension = file[:-4]
        if st.sidebar.button(file_without_extension, use_container_width=True):
            st.session_state.messages = load_conversation(os.path.join(conversation_dir, file))

def get_last_user_message():
    """
    Function to retrieve the last message sent by a user.
    """
    messages = st.session_state.get("messages", [])
    for message in reversed(messages):
        if message['role'] == 'user':
            return message['content']
    return None  # Return None if no user message is found



def main():
    init_messages()
    temperature = select_model()
    display_saved_conversations()

    # Display chat history
    messages = st.session_state.get("messages", [])
    for message in messages:    
        if message['role'] == 'assistant':
            with st.chat_message("assistant", avatar=avatar_bot):
                print(message)
                st.markdown(message['content'])
        
        if message['role'] == 'user':
            with st.chat_message("user", avatar=avatar_user):
                
                st.markdown(message['content'] )

    if user_input := st.chat_input("Input your question!"):
        st.session_state.messages.append(HumanMessage(user_input))
        with st.chat_message("user", avatar=avatar_user):
            st.markdown(get_last_user_message())

        params = chat_message(messages=st.session_state.messages,temperature=temperature)
        with st.chat_message("assistant", avatar=avatar_bot):
            text_placeholder = st.empty()

            collected_messages = ""
            result = client.chat.completions.create(**params)
            for chunks in result:
                chunk_message = chunks.choices[0].delta.content
                if type(chunk_message) == str:
                    collected_messages += chunk_message
                    # st.markdown(collected_messages)
                    text_placeholder.markdown(collected_messages)
                else:
                    pass

            # answer =result.choices[0].message.content
                answer = collected_messages
                print("result.choices[0].message" , ":" , answer)


        st.session_state.messages.append(AIMessage(answer))
        



if not os.path.exists('conversations'):
    os.makedirs('conversations')
# %% Main  
if __name__ == "__main__":
    main()