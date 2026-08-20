import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep
from pypdf import PdfReader
import streamlit as st
load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)


# Fixed: Changed to a valid open-source model available on Groq
model = "openai/gpt-oss-120b"



def ask_llm(system_prompt,user_prompt):
    sys_msg={
        "role":"system",
        "content": system_prompt
    }
    user_msg={
        "role": "user",
        "content": user_prompt
    }
    messages=[sys_msg, user_msg]
    
    # Fixed: Corrected the typo 'resposne' to 'response' on these two lines
    response=client.chat.completions.create(model=model, messages=messages)
    answer=response.choices[0].message.content
    return answer
    
    # #using streaming
    # stream=client.chat.completions.create(model=model, messages=messages,stream=True)
    # for chunk in stream:
    #     content=chunk.choices[0].delta.content
    #     if content:
    #         #return (content)

def step1_Key(Dos,a):
    print("STEP 1")
    system_prompt=f"""
    You are a Senior Professsor of Python. Extract the {a} key words from the text provided.
    Only return the {a} key words no other information. Do not invent any skills by yourself.
    TAsk:
    Do mot give any other information just extract only {a} key words.Do not give What it means,Why it matters for , and no quick recap .
    Example:
    1.Python.
    2.Decorators.
    Output Format:
    only give the names of {a} Key words should be in next line and with serial number. Just return each on new line concepts do not return any other filler information
    """
    user_prompt=f"""
    Extract only {a} key words from this text.
    {Dos}
    """
    return ask_llm(system_prompt, user_prompt)

def step2_Keyconcept(Keys, a):
    print("STEP 2")
    system_prompt=f"""
    You are a Senior Professsor of Python. take  the {a} key words from the prompt1 provided.
    Only return the explanation in one line no other information. Do not invent any skills by yourself.
    Output Format:
    Explaination should be separated by line and with serial number. Just return one line explaination do not return any other filler information
    """
    user_prompt=f"""
    Explain the all the {a} key concepts from propmt1 only in one line and with no example.
    {Keys}
    """
    return ask_llm(system_prompt, user_prompt)

def step3_examples(Keys_concepts):
    print("STEP 3")
    system_prompt=f"""
    You are a Senior Professsor of Python. Extract the key concepts from the text provided.
    Only return the one examples related no other information. Do not invent any skills by yourself.
    Output Format:
    Examples should be separated by line and with serial number. Just return line separated exaples and do not return any other filler information
    """
    user_prompt=f"""
    Give only examples for previous propmt1 key concepts.
    {Keys_concepts}
    """
    return ask_llm(system_prompt, user_prompt)

def step4_interview(Keys_concepts,a):
    print("STEP 4")
    system_prompt=f"""
    You are a Senior Professsor of Python. Generate {a} intervies questions from key concepts of doc provided.
    Only return the 5 questions no other information. Do not invent any question by yourself.
    Output Format:
    Each question  should be separated by next line and with serial number. Just return line separated questions do not return any other filler information
    """
    user_prompt=f"""
    Generate {a} interview question from the given docs
    {Keys_concepts}
    """
    return ask_llm(system_prompt, user_prompt)

# --- 4. STREAMLIT FRONTEND UI ---
st.title("📚 AI Document Processor")
st.write("Upload a PDF to extract keywords, concepts, examples, and interview questions.")

# Input Widgets
uploaded_file = st.file_uploader("Upload your PDF document", type="pdf")
a = st.number_input("Enter number of Keywords to extract:", min_value=1, max_value=20, value=5)

# Execution Button
if st.button("Process Document"):
    if uploaded_file is not None:
        try:
            # Read PDF directly from Streamlit uploader
            reader = PdfReader(uploaded_file)
            Dos = ""
            for page in reader.pages:
                if page.extract_text():
                    Dos += page.extract_text() + "\n"
            
            if not Dos.strip():
                st.error("Failed to extract text. The PDF might be an image/scanned document.")
            else:
                st.success(f"PDF loaded successfully! Text length: {len(Dos)} characters.")
                
                # Run the AI pipeline
                with st.spinner("Extracting Keywords..."):
                    Keys = step1_Key(Dos, a)
                    st.subheader("🔑 Keywords")
                    st.write(Keys)
                    sleep(2)
                
                with st.spinner("Explaining Concepts..."):
                    Key_concepts = step2_Keyconcept(Keys, a)
                    st.subheader("📖 Concepts")
                    st.write(Key_concepts)
                    sleep(2)
                
                with st.spinner("Generating Examples..."):
                    examples = step3_examples(Key_concepts)
                    st.subheader("💻 Examples")
                    st.write(examples)
                    sleep(2)
                
                with st.spinner("Drafting Interview Questions..."):
                    questions = step4_interview(Key_concepts, a)
                    st.subheader("🎯 Interview Questions")
                    st.write(questions)
                    
                st.balloons() # Adds a nice animation when finished!
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a PDF document first!")