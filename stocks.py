import streamlit as st
import yfinance as yf
import datetime

last_ticker = None

ticker = st.text_input(label="Ticker")

st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.write("Start:")
    start_date = st.date_input(label="Start Datum")
    start_time = st.time_input(label="Start Zeit", step=3600)

with col2:
    st.write("Ende:")
    end_date = st.date_input(label="Ende Datum")
    end_time = st.time_input(label="Ende Zeit")

st.write("---")

col3, col4 = st.columns(2)

with col3:
    buy_threshold = st.number_input(label="Buy Threshold")
    sell_threshold = st.number_input(label="Sell Threshold")

with col4:
    bankroll = st.number_input(label="Kapital", step=100)
    fee = st.number_input(label="Gebuehren")

submit = st.button(label="Submit")

if submit:   

    start_datetime = datetime.datetime.combine(start_date, start_time)
    end_datetime = datetime.datetime.combine(end_date, end_time)

    if ticker != last_ticker:
        data = yf.Ticker(ticker)

    st.write("Ausgewaehlte Aktie:", data.info["shortName"])
    
    try:   
        history = data.history(start=start_datetime, end=end_datetime, interval="60m")     
        st.write(history)

    except Exception as e:
        st.warning(e)
    