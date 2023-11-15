
import streamlit as st 
import openai
from PIL import Image


from openai import OpenAI
import os 
os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()



avatar_bot = Image.open(r"utils\logo_gold_Icon.png")
avatar_user = Image.open(r"utils\logo_white_icon.png")



def chat_message(messages,temperature = 0.5):
        

        return {
            "model": "gpt-4-1106-preview",
            "messages": messages,
            
            "max_tokens": 4096,
            "temperature": temperature
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
    
    logo_image = Image.open(r"utils\White_Logo_Black_text_Transparent.png")
    st.image(logo_image, width=300, channels="RGB")

    st.header("MinckaGPT")
    st.sidebar.title("Options")


def select_model():
    # model_name = st.sidebar.radio("Choose LLM:",
    #                               ("gpt-3.5-turbo-16k", "gpt-4", "Web Search Agent","PDF Loader","Mincka Agent"))
    temperature = st.sidebar.slider("Temperature:", min_value=0.0,
                                    max_value=1.0, value=0.0, step=0.01)
    return temperature


logo_image = Image.open(r"utils\White_Logo_Black_text_Transparent.png")
st.image(logo_image, width=300, channels="RGB")

st.header("MinckaGPT")
st.sidebar.title("Options")


_content = "You are a helpful AI assistant. Respond your answer in mardkown format and in Australina english."
def init_messages(content = _content):
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    st.session_state.costs = []
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            # SystemMessage(
            #     content=_content)
            {'role':'system', 'content':content}
        ]

def main():
    init_messages()
    temperature = select_model()
    # Supervise user input
    if user_input := st.chat_input("Input your question!"):
        st.session_state.messages.append( HumanMessage(user_input))
        with st.spinner("MinckaGPT is typing ..."):
            
            params = chat_message(messages=st.session_state.messages,temperature=temperature)

            result = client.chat.completions.create(**params)
            answer =result.choices[0].message.content
            print("result.choices[0].message" , ":" , answer)

                # st.session_state.costs.append(cost)
        st.session_state.messages.append(AIMessage(answer))
        


    # Display chat history
    messages = st.session_state.get("messages", [])
    for message in messages:    
        if message['role'] == 'assistant':
            with st.chat_message("assistant", avatar=avatar_bot):
                print(message)
                st.markdown(message['content'])
        
        elif message['role'] == 'user':
            with st.chat_message("user", avatar=avatar_user):
                
                st.markdown(message['content'] )
        

             
        # if isinstance(message, AIMessage):
        #     with st.chat_message("assistant", avatar=avatar_bot):
        #         st.markdown(message.content)
        # elif isinstance(message, HumanMessage):
        #     with st.chat_message("user", avatar=avatar_user):
        #         st.markdown(message.content)


# %% Main  
if __name__ == "__main__":
    main()