import streamlit as st
from finance_agent import get_stock_info

# Configurazione pagina Streamlit
st.set_page_config(page_title="Financial Data Dashboard", page_icon="📈", layout="centered")
st.title("📈 Financial Data Assistant")
st.caption("Dati e metriche di mercato in tempo reale estratti da Yahoo Finance")

# ==========================================
#  BARRA LATERALE: INFORMAZIONI SVILUPPATORE
# ==========================================
with st.sidebar:
    st.markdown("## 👨‍💻 Developer Info")
    st.markdown("**Sviluppatore:** Marco Avellino")
    
       st.markdown("---")
    st.markdown("### 📊 Dettagli Software")
    st.write("- **Versione App:** v1.1.0")
    st.write("- **Licenza:** MIT License")
    st.write("- **Status:** Online & Funzionante")
    
    st.markdown("---")
    st.markdown("### 🤖 Info sul Bot")
    st.markdown(
        "Questo assistente estrae dati grezzi direttamente dai mercati finanziari. "
        "Le risposte vengono mostrate in formato **JSON**, garantendo la massima trasparenza, "
        "leggibilità informatica e assenza di allucinazioni da intelligenza artificiale."
    )
    st.markdown("---")
    st.markdown("### 💡 Ticker di Esempio:")
    st.markdown("- **TSLA** (Tesla)\n- **AAPL** (Apple)\n- **NVDA** (NVIDIA)\n- **MSFT** (Microsoft)")

# Inizializzazione della cronologia dei messaggi nella chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ciao! Scrivi il nome di un'azione o il suo ticker (es. 'AAPL', 'NVDA', 'TSLA') per vedere le sue metriche finanziarie aggiornate."}
    ]

# Mostra i messaggi precedenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], dict):
            st.json(message["content"])
        else:
            st.markdown(message["content"])

# Input dell'utente
if user_input := st.chat_input("Scrivi qui il ticker dell'azienda..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Logica di elaborazione dei dati finanziari
    with st.chat_message("assistant"):
        found_data = False
        words = user_input.upper().split()
        
        for word in words:
            # Rimuove la punteggiatura per isolare il ticker
            clean_word = "".join(filter(str.isalnum, word))
            if len(clean_word) <= 5 and clean_word.isalpha():
                
                with st.spinner(f"Estrazione dati per {clean_word}..."):
                    data = get_stock_info(clean_word)
                
                if "Errore" not in data:
                    st.success(f"Ecco i dati finanziari aggiornati per {clean_word}:")
                    st.json(data) # Mostra la tabella con i dati reali
                    st.session_state.messages.append({"role": "assistant", "content": data})
                    found_data = True
                    break
        
        if not found_data:
            errore_msg = "Non sono riuscito a trovare un ticker azionario valido nella tua richiesta. Riprova indicando un simbolo (es. AAPL)."
            st.warning(errore_msg)
            st.session_state.messages.append({"role": "assistant", "content": errore_msg})
