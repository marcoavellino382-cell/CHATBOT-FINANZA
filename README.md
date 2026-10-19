# 📈 Financial AI Assistant

Un chatbot intelligente per l'analisi finanziaria sviluppato in **Python** e **Streamlit**. L'applicazione integra dati di mercato in tempo reale tramite l'API di Yahoo Finance (`yfinance`) e sfrutta la potenza dei modelli di linguaggio **OpenAI (GPT-4o-mini)** per fornire analisi descrittive e risposte contestualizzate sui titoli azionari.

---

## ✨ Funzionalità principali
- **Dati Finanziari in Tempo Reale:** Estrazione automatica di metriche chiave come Prezzo Corrente, P/E Ratio, Market Cap, Fatturato e Margini di profitto semplicemente menzionando il ticker di un'azienda (es. *AAPL*, *NVDA*, *TSLA*).
- **Analisi basata su AI:** Un assistente virtuale specializzato che commenta i dati finanziari e risponde a domande complesse sul mercato.
- **Interfaccia Chat Fluida:** Interfaccia utente nativa e interattiva grazie ai componenti chat di Streamlit.
- **Sicurezza:** Gestione sicura delle credenziali tramite i Secret di Streamlit Cloud.

---

## 🛠️ Stack Tecnologico
- **Linguaggio:** Python 3.10+
- **Interfaccia Utente:** Streamlit
- **Dati Finanziari:** Yahoo Finance API (`yfinance`)
- **Modello AI:** OpenAI API (`gpt-4o-mini`)

---


## 🌐 Deploy su Streamlit Community Cloud
L'applicazione è pronta per il deploy immediato su Streamlit Cloud:
1. Connetti il tuo account GitHub a Streamlit Cloud.
2. Seleziona questa repository e il file principale `app.py`.
3. Nei **Secrets** dell'app su Streamlit, inserisci la tua chiave API in questo formato:
   ```toml
   OPENAI_API_KEY = "la_tua_chiave_segreta_qui"
   ```

---

## ⚠️ Disclaimer Finanziario
Questo software è sviluppato esclusivamente a scopo didattico e informativo. Non costituisce in alcun modo un servizio di consulenza finanziaria né un invito o una raccomandazione al pubblico risparmio o all'investimento.
