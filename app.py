import streamlit as st
from openai import OpenAI
from finance_agent import get_stock_info

# Configurazione pagina Streamlit
st.set_page_config(page_title="Financial AI Advisor", page_icon="📈", layout="centered")
st.title("📈 Financial AI Assistant")
st.caption("Analisi finanziaria in tempo reale potenziata dall'Intelligenza Artificiale")

# RECUPERA LA CHIAVE IN AUTOMATICO DAI SECRETS (Niente più barra laterale!)
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Inizializzazione della cronologia dei messaggi
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ciao! Chiedimi pure un'analisi su un'azione (es. 'Come sta andando NVDA?')."}
    ]

# Mostra i messaggi precedenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dell'utente
if user_input := st.chat_input("Scrivi qui la tua domanda finanziaria..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Inizializzazione client OpenAI
    client = OpenAI(api_key=openai_api_key)

    # Logica di elaborazione (Risposta dell'assistente)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        system_prompt = (
            "Sei un assistente finanziario esperto, analitico e prudente. "
            "Fornisci risposte basate su dati. Se l'utente menziona un ticker azionario (es. AAPL, NVDA, TSLA), "
            "usa i dati di contesto forniti per commentare le metriche. Non fornire mai consigli di investimento diretti."
        )
        
        context_data = ""
        words = user_input.upper().split()
        for word in words:
            clean_word = "".join(filter(str.isalnum, word))
            if len(clean_word) <= 5 and clean_word.isalpha():
                data = get_stock_info(clean_word)
                if "Errore" not in data:
                    context_data = f"\nDati attuali per {clean_word}: {str(data)}"
                    st.json(data) # Mostra il widget con i dati estratti
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
