import streamlit as st
import openai
from datetime import datetime

def ask_gpt(prompt, model, apikey):
    client=openai.OpenAI(api_key=apikey)
    response=client.chat.completions.create(
        model=model,
        messages=prompt
    )
    gptResponse=response.choices[0].message.content
    return gptResponse

def main():
    st.set_page_config(
        page_title="음성 비서 프로그램",
        layout="wide")

    st.header("음성 비서 프로그램")

    st.markdown("---")

    with st.expander("음성비서 프로그램에 관하여", expanded=True):
        st.write(
            """
        - 음성 비서 프로그램의 UI는 스트림릿을 활용했습니다.
        - 답변은 OpenAI의 GPT 모델을 활용했습니다.
        """
        )

        st.markdown("")

    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system",
                                         "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]

    with st.sidebar:
        st.session_state["OPENAI_API"] = st.text_input(label="OPEN API 키", placeholder="Enter Your API Key", value="",
                                                      type="password")

        st.markdown("---")

        model = st.radio(label="GPT 모델", options=["gpt-4", "gpt-3.5-turbo"])

        st.markdown("---")

        if st.button(label="초기화"):
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "system",
                                             "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("질문하기")
        question = st.text_input("질문을 입력하세요")
        if st.button("답변 받기"):
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"] + [("user", now, question)]
            st.session_state["messages"] = st.session_state["messages"] + [{"role": "user", "content": question}]

    with col2:
        st.subheader("질문/답변")
        if question:
            response = ask_gpt(st.session_state["messages"], model, st.session_state["OPENAI_API"])
            st.session_state["messages"] = st.session_state["messages"] + [{"role": "system", "content": response}]
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"] + [{"bot", now, response}]

            for sender, time, message in st.session_state["chat"]:
                if sender == "user":
                    st.write(f'User: {message} ({time})')
                else:
                    st.write(f'Bot: {message} ({time})')

if __name__ == "__main__":
    main()
