import streamlit as st
from finance_agent import get_stock_info

# Configurazione pagina Streamlit
st.set_page_config(page_title="Financial Data Dashboard", page_icon="📈", layout="centered")

# ==========================================
#  BARRA LATERALE: INFORMAZIONI SVILUPPATORE
# ==========================================
with st.sidebar:
    st.title("👨‍💻 Developer Info")
    st.write("**Sviluppatore:** [Marco Avellino](https://linkedin.com/in/marco-avellino-1a0918411)")
    
    
    st.markdown("---")
    st.markdown("### 🤖 Info sul Bot")
    st.write(
        "Questo assistente estrae dati grezzi direttamente dai mercati finanziari. "
        "Le risposte vengono mostrate in formato JSON, garantendo la massima trasparenza, "
        "leggibilità informatica e assenza di allucinazioni da intelligenza artificiale."
    )
    st.markdown("---")
    st.markdown("### 💡 Ticker di Esempio:")
    st.write("- **TSLA** (Tesla)\n- **RACE.MI** (Ferrari)\n- **BTC-USD** (Bitcoin)\n- **AAPL** (Apple)")

# ==========================================
#          CORPO PRINCIPALE DELL'APP
# ==========================================
st.title("📈 Financial Data Assistant")
st.caption("Dati e metriche di mercato in tempo reale estratti da Yahoo Finance")

# Inizializzazione della cronologia dei messaggi nella chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ciao! Scrivi il nome di un'azione o il suo ticker (es. 'AAPL', 'RACE.MI', 'BTC-USD') per vedere le sue metriche finanziarie."}
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
        
        # Se l'utente scrive una sola parola (es. "MSFT"), la consideriamo direttamente il ticker
        if len(words) == 1:
            ticker_to_check = "".join([c for c in words[0] if c.isalnum() or c in ".-"])
            tickers = [ticker_to_check]
        else:
            # Se scrive una frase, analizziamo le singole parole escludendo quelle di comando comuni
            comandi_comuni = ["ANALIZZAMI", "CERCA", "CONTROLLA", "MOSTRA", "TROVA"]
            tickers = ["".join([c for c in w if c.isalnum() or c in ".-"]) for w in words if w not in comandi_comuni]

        for clean_word in tickers:
            if 1 <= len(clean_word) <= 10:
                with st.spinner(f"Estrazione dati per {clean_word}..."):
                    data = get_stock_info(clean_word)
                
                # Se Yahoo Finance risponde con un errore o non trova il nome aziendale, passa oltre
                if "Errore" in data or data.get("Nome") == clean_word or data.get("Prezzo Attuale") == "$N/D":
                    continue
                
                # Mostra la tabella se il titolo è valido
                st.success(f"Ecco i dati finanziari aggiornati per {clean_word}:")
                st.json(data)
                st.session_state.messages.append({"role": "assistant", "content": data})
                found_data = True
                break
        
        if not found_data:
            errore_msg = "Non sono riuscito a trovare un ticker azionario valido. Riprova inserendo solo il simbolo (es. MSFT, AAPL, ENI.MI)."
            st.warning(errore_msg)
            st.session_state.messages.append({"role": "assistant", "content": errore_msg})
