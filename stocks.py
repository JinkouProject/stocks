import streamlit as st
import yfinance as yf
import datetime
import math

def compare_strategies(data, buy_threshold, sell_threshold, starting_bankroll, fee):

  buy_sell_history = []
  hold_history = []

  starting_value = data["Open"][0]
  reference_value = starting_value
  stock_amount = math.floor(starting_bankroll / reference_value)
  bankroll = starting_bankroll - stock_amount * reference_value
  bankroll = bankroll - fee
  needed_gain = reference_value * sell_threshold

  stock_amount_hold = stock_amount
  bankroll_hold = bankroll

  buy_sell_history.append(f"{str(data.index[0])}: KAUF: {stock_amount} Aktien fuer {round(starting_value, 2)}")
  hold_history.append(f"{str(data.index[0])}: KAUF: {stock_amount} Aktien fuer {round(starting_value, 2)}")

  sell = True
  buy = False

  for date, value in data["Open"].items():

    if sell == True and value >= (reference_value + needed_gain):

      buy_sell_history.append(f"{date}: VERKAUF: {stock_amount} Aktien fuer {round(value, 2)}")
      bankroll = bankroll + stock_amount * value
      bankroll = bankroll - fee
      buy_sell_history.append(f"Neuer Kontostand: {round(bankroll)}\n")

      reference_value = value
      needed_loss = reference_value * buy_threshold

      sell = False
      buy = True

    if buy == True and value <= (reference_value - needed_loss):

      stock_amount = math.floor(bankroll / value)
      bankroll = bankroll - stock_amount * value

      buy_sell_history.append(f"{date}: KAUF: {stock_amount} Aktien fuer {round(value, 2)}")

      reference_value = value
      needed_gain = starting_value * sell_threshold

      bankroll = bankroll - fee

      buy = False
      sell = True

  if sell == True:
    bankroll = bankroll + stock_amount * value
    bankroll = bankroll - fee
    buy_sell_history.append(f"{date}: VERKAUF: {stock_amount} Aktien fuer {round(value, 2)}")

  bankroll_hold = bankroll_hold + stock_amount_hold * value
  bankroll_hold = bankroll_hold - fee

  hold_history.append(f"{date}: VERKAUF: {stock_amount_hold} Aktien fuer {round(value, 2)}")

  return buy_sell_history, hold_history, round(bankroll), round(bankroll_hold)

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
    starting_bankroll = st.number_input(label="Kapital", step=100)
    fee = st.number_input(label="Gebuehren")

submit = st.button(label="Submit")

if submit:   

    st.write("---")

    start_datetime = datetime.datetime.combine(start_date, start_time)
    end_datetime = datetime.datetime.combine(end_date, end_time)
    
    try:
        ticker = yf.Ticker(ticker)   
        st.write("#Ausgewaehlte Aktie:", ticker.info["shortName"])
        data = ticker.history(start=start_datetime, end=end_datetime, interval="60m")     
        buy_sell_history, hold_history, bankroll, bankroll_hold = compare_strategies(data, buy_threshold, sell_threshold, starting_bankroll, fee)

        col5, col6 = st.columns(2)
        
        with col5:
            st.subheader("Kaufen/Verkaufen")
            for event in buy_sell_history:
                st.write(event)

        with col6:
            st.subheader("Halten")
            for event in hold_history:
                st.write(event)

        st.write("---")
        st.write("Finaler Kontostand")

        col7, col8 = st.columns(2)

        with col7:
           st.subheader(bankroll)

        with col8:
           st.subheader(bankroll_hold)

    except Exception as e:
        st.warning(e)
    
