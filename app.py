import streamlit as st
from openai import OpenAI
from finance_agent import get_stock_info

st.set_page_config(page_title="Financial AI Advisor", page_icon="📈")
st.title("📈 Financial AI Assistant")

with st.sidebar:
    openai_api_key = st.text_input("Inserisci la tua OpenAI API Key", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ciao! Chiedimi pure un'analisi su un'azione (es. 'Come sta andando AAPL?')."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Scrivi qui la tua domanda..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if not openai_api_key:
        st.info("Per favore, inserisci la tua OpenAI API Key nella barra laterale.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        system_prompt = "Sei un assistente finanziario esperto. Usa i dati forniti per commentare le metriche."
        context_data = ""
        words = user_input.upper().split()
        for word in words:
            clean_word = "".join(filter(str.isalnum, word))
            if len(clean_word) <= 5 and clean_word.isalpha():
                data = get_stock_info(clean_word)
                if "Errore" not in data:
                    context_data = f"\nDati attuali per {clean_word}: {str(data)}"
                    st.json(data)
                    break

        messages_api = [{"role": "system", "content": system_prompt + context_data}]
        for m in st.session_state.messages:
            messages_api.append({"role": m["role"], "content": m["content"]})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_api
        )
        
        full_response = response.choices.message.content
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
