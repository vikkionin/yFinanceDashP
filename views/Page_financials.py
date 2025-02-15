from functions import *
from contact import contact_form

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

st.set_page_config(
    page_title="Financials", # The page title, shown in the browser tab.
    page_icon=":material/finance:",
    layout="wide", # How the page content should be laid out.
    initial_sidebar_state="auto", # How the sidebar should start out.
    menu_items={ # Configure the menu that appears on the top-right side of this app.
        "Get help": "https://github.com/LMAPcoder" # The URL this menu item should point to.
    }
)

# ----SESSION STATE -----
all_my_widget_keys_to_keep = {
    'tickers': "MSFT",
    'current_time_financials_page': datetime.datetime.now(st.session_state['timezone']).replace(microsecond=0, tzinfo=None)
}

for key in all_my_widget_keys_to_keep:
    if key not in st.session_state:
        st.session_state[key] = all_my_widget_keys_to_keep[key]

for key in all_my_widget_keys_to_keep:
    st.session_state[key] = st.session_state[key]


# ---- SIDEBAR ----
with st.sidebar:

    TICKERS = st.text_input(
        label="Securities:",
        #value='MSFT',
        key='tickers'
    )

    TICKERS = [item.strip() for item in TICKERS.split(",") if item.strip() != ""]

    TICKERS = remove_duplicates(TICKERS)

    TICKERS = TICKERS[:10]

    _tickers = list()
    for TICKER in TICKERS:
        info = fetch_info(TICKER)
        if info is None:
            st.error(f"{TICKER} is an invalid ticker")
        else:
            QUOTE_TYPE = info.get('quoteType', "")
            if QUOTE_TYPE not in ["EQUITY"]:
                st.error(f"{TICKER} has an invalid quoteType ({QUOTE_TYPE})")
            else:
                _tickers.append(TICKER)

    TICKERS = _tickers

    TIME_PERIOD = st.radio(
        label="Time Period:",
        options=["Annual", "Quarterly"]
    )

    st.write("")
    button = st.button("Refresh data", key="refresh_security")

    if button:
        st.session_state['current_time_financials_page'] = datetime.datetime.now(st.session_state['timezone']).replace(microsecond=0, tzinfo=None)
        fetch_info.clear()
        fetch_balance.clear()
        fetch_income.clear()
        fetch_cash.clear()
        #st.cache_data.clear()

    st.write("Last update:", st.session_state['current_time_financials_page'])

    st.markdown("Made with ❤️ by Leonardo")

    button = st.button("✉️ Contact Me", key="contact")

    if button:
        show_contact_form()

# ---- MAINPAGE ----

st.title("Financials")

if len(TICKERS) == 0:
    st.header(f"Security: None")
    st.error("No valid ticker")
    st.stop()

if len(TICKERS) == 1:

    TICKER = TICKERS[0]

    info = fetch_info(TICKER)

    NAME = info.get('shortName', "")
    st.write(f'{NAME}')

    bs = fetch_balance(TICKER, tp=TIME_PERIOD) #balance sheet
    ist = fetch_income(TICKER, tp=TIME_PERIOD) #income statement
    cf = fetch_cash(TICKER, tp=TIME_PERIOD) #cash flow

    CURRENCY = info.get('financialCurrency', "???")

    #----CAPITAL STRUCTURE-----

    st.header("Capital Structure")

    fig = plot_capital(bs, ticker=TICKER, currency=CURRENCY)

    st.plotly_chart(
        fig,
        use_container_width=True,
        # theme=None
    )

    #----BALANCE SHEET----

    st.header("Balance Sheet")

    st.write("The balance sheet refers to a financial statement that reports "
             "a company's assets, liabilities, and shareholder equity at a specific point in time.")


    fig = plot_balance(bs[bs.columns[::-1]], ticker=TICKER, currency=CURRENCY)

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show components"):

        tab1, tab2, tab3 = st.tabs(["Assets", "Liabilities", "Equity"])

        with tab1:
            fig = plot_assets(bs, ticker=TICKER, currency=CURRENCY)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig = plot_liabilities(bs, ticker=TICKER, currency=CURRENCY)
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            fig = plot_equity(bs, ticker=TICKER, currency=CURRENCY)
            st.plotly_chart(fig, use_container_width=True)



    with st.expander("Show data"):
        st.dataframe(
            data=bs,
            hide_index=False
        )

    #----INCOME STATEMENT----

    st.header("Income Statement")

    st.write("The income statement refers to a financial statement that tracks the "
             "company's revenue, expenses, gains, and losses during a set period.")

    fig = plot_income(ist, ticker=TICKER, currency=CURRENCY)

    st.plotly_chart(fig, use_container_width=True)


    with st.expander("Show data"):
        st.dataframe(
            data=ist,
            hide_index=False
        )

    #----CASH FLOW----

    st.header("Cash Flow")

    st.write("The cash flow statement provides aggregate data regarding all cash inflows and"
             " all cash outflows during a given period")

    fig = plot_cash(cf, ticker=TICKER, currency=CURRENCY)

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show data"):
        st.dataframe(
            data=cf,
            hide_index=False
        )

else:
    # ----CAPITAL STRUCTURE-----

    st.header("Capital Structure")

    fig = plot_capital_multiple(TICKERS, tp=TIME_PERIOD)

    st.plotly_chart(
        fig,
        use_container_width=True,
        # theme=None
    )


    # ----BALANCE SHEET----

    st.header("Balance Sheet")

    fig = plot_balance_multiple(TICKERS, tp=TIME_PERIOD)

    st.plotly_chart(fig, use_container_width=True)

    # ----INCOME STATEMENT----

    st.header("Income Statement")

    fig = plot_income_multiple(TICKERS, tp=TIME_PERIOD)

    st.plotly_chart(fig, use_container_width=True)

    # ----CASH FLOW----

    st.header("Cash Flow")

    fig = plot_cash_multiple(TICKERS, tp=TIME_PERIOD)

    st.plotly_chart(fig, use_container_width=True)