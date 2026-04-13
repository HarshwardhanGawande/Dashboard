import streamlit as st
import requests
import json
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Zerodha Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* Reset & Base */
.stApp {
    background: #0a0c10;
}

.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1200px !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header, .stDeployButton {
    display: none !important;
}

/* Typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Headers */
.main-header {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00e5a0 0%, #00b8ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.sub-header {
    font-size: 0.75rem;
    color: #4a5060;
    margin-bottom: 1rem;
}

/* Section styling */
.section-card {
    background: #111318;
    border: 1px solid #1e2128;
    border-radius: 10px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}

.section-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4a5060;
    margin-bottom: 0.75rem;
}

/* Input styling */
.stSelectbox [data-baseweb="select"] {
    background-color: #0a0c10;
    border-color: #1e2128;
}

.stNumberInput input, .stTextInput input {
    background-color: #0a0c10 !important;
    border-color: #1e2128 !important;
    color: #e8eaf0 !important;
}

/* Button styling - FIXED ARRANGEMENT */
.stButton button {
    font-weight: 600 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
}

/* Primary action button */
.primary-button button {
    background: linear-gradient(135deg, #00e5a0 0%, #00b8ff 100%) !important;
    color: #000 !important;
}

/* Secondary buttons */
.secondary-button button {
    background: #1e2128 !important;
    color: #e8eaf0 !important;
    border: 1px solid #2a3040 !important;
}

.secondary-button button:hover {
    background: #2a3040 !important;
}

/* Order type buttons container */
.order-buttons-container {
    display: flex;
    gap: 0.5rem;
    margin: 0.5rem 0;
}

.order-btn {
    flex: 1;
    text-align: center;
    padding: 0.5rem;
    background: #0a0c10;
    border: 1px solid #1e2128;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.2s ease;
}

.order-btn.active {
    background: rgba(0,229,160,0.1);
    border-color: #00e5a0;
    color: #00e5a0;
}

.order-btn:hover {
    border-color: #00e5a0;
}

/* Metrics */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-top: 0.75rem;
}

.metric-card {
    background: #0a0c10;
    border: 1px solid #1e2128;
    border-radius: 8px;
    padding: 0.75rem;
    text-align: center;
}

.metric-label {
    font-size: 0.65rem;
    color: #4a5060;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

.metric-value {
    font-size: 1.2rem;
    font-weight: 700;
    color: #00e5a0;
}

.metric-value.red {
    color: #ff4d6d;
}

/* Info box */
.info-box {
    background: rgba(0,229,160,0.05);
    border-left: 3px solid #00e5a0;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    margin: 0.75rem 0;
    font-size: 0.85rem;
}

/* Log */
.log-container {
    background: #0a0c10;
    border: 1px solid #1e2128;
    border-radius: 8px;
    padding: 0.75rem;
    max-height: 150px;
    overflow-y: auto;
    font-size: 0.75rem;
    font-family: monospace;
}

.log-entry {
    padding: 0.25rem 0;
    border-bottom: 1px solid #1e2128;
    color: #8890a0;
}

.log-success {
    color: #00e5a0;
}

.log-error {
    color: #ff4d6d;
}

/* Expander */
.streamlit-expanderHeader {
    background: #111318 !important;
    border-radius: 8px !important;
}

/* Divider */
hr {
    border-color: #1e2128;
    margin: 1rem 0;
}

/* Layout helpers */
.flex-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.gap-2 {
    gap: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Config ───────────────────────────────────────────────────────────────────

BASE_URL = 'https://kite.zerodha.com'
LOGIN_URL = f'{BASE_URL}/api/login'
TWOFA_URL = f'{BASE_URL}/api/twofa'
ORDER_URL = f'{BASE_URL}/oms/orders'
HIST_URL = f'{BASE_URL}/oms/instruments/historical/{{instrument_id}}/{{interval}}'

TOKEN_CSV = r"C:\Users\harsh\Dropbox\Trading_2026\Dashboard\symbol_data\token_ids.csv"

@st.cache_data
def load_token_map(path: str = TOKEN_CSV):
    if not os.path.exists(path):
        st.error(f"❌ Token file not found: {path}")
        st.stop()
    df = pd.read_csv(path, dtype={"symbol": str, "token": int})
    df.columns = df.columns.str.strip().str.lower()
    token_dict = dict(zip(df["symbol"], df["token"]))
    return sorted(token_dict.keys()), token_dict

SYMBOLS, TOKEN_MAP = load_token_map()

# ─── Session State ────────────────────────────────────────────────────────────

if "enctoken" not in st.session_state:
    st.session_state.enctoken = os.getenv("ENCTOKEN", "")
if "user_id" not in st.session_state:
    st.session_state.user_id = os.getenv("USER_ID", "")
if "order_log" not in st.session_state:
    st.session_state.order_log = []
if "ltp_cache" not in st.session_state:
    st.session_state.ltp_cache = {}
if "selected_order" not in st.session_state:
    st.session_state.selected_order = "MARKET"

# ─── Helper Functions ─────────────────────────────────────────────────────────

def _session():
    s = requests.Session()
    s.headers.update({
        "authorization": f"enctoken {st.session_state.enctoken}",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    return s

def _log(msg, kind="info"):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.order_log.insert(0, {"ts": ts, "msg": msg, "kind": kind})

def check_token():
    if not st.session_state.enctoken:
        return False
    s = _session()
    resp = s.get(HIST_URL.format(instrument_id=86529, interval="minute"),
                 params={"user_id": st.session_state.user_id, "oi": "1",
                        "from": "2026-03-25", "to": "2026-03-25"})
    return resp.status_code == 200

def do_login(password, twofa):
    s = requests.Session()
    s.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
    r = s.post(LOGIN_URL, data={"user_id": st.session_state.user_id, "password": password})
    if r.status_code != 200:
        return False
    request_id = r.json()["data"]["request_id"]
    s.post(TWOFA_URL, data={"user_id": st.session_state.user_id,
                           "request_id": request_id, "twofa_value": twofa})
    cookies = requests.utils.dict_from_cookiejar(s.cookies)
    if "enctoken" in cookies:
        st.session_state.enctoken = cookies["enctoken"]
        return True
    return False

def fetch_ltp(ticker):
    instrument_id = TOKEN_MAP.get(ticker)
    if not instrument_id:
        return None
    today = datetime.now().strftime("%Y-%m-%d")
    s = _session()
    resp = s.get(HIST_URL.format(instrument_id=instrument_id, interval="minute"),
                 params={"user_id": st.session_state.user_id, "oi": "1",
                        "from": today, "to": today})
    if resp.status_code == 200:
        candles = resp.json().get("data", {}).get("candles", [])
        if candles:
            return float(candles[-1][4])
    return None

def place_market_order(tradingsymbol, transaction_type, quantity, exchange="NSE"):
    s = _session()
    payload = {
        "exchange": exchange, "tradingsymbol": tradingsymbol,
        "transaction_type": transaction_type, "quantity": quantity,
        "product": "MIS", "validity": "DAY", "variety": "regular",
        "order_type": "MARKET", "price": 0, "trigger_price": 0,
        "user_id": st.session_state.user_id,
    }
    resp = s.post(f"{ORDER_URL}/regular", data=payload)
    return resp.json()

def place_limit_order(tradingsymbol, transaction_type, quantity, price, exchange="NSE"):
    s = _session()
    payload = {
        "exchange": exchange, "tradingsymbol": tradingsymbol,
        "transaction_type": transaction_type, "quantity": quantity,
        "product": "MIS", "validity": "DAY", "variety": "regular",
        "order_type": "LIMIT", "price": price, "trigger_price": 0,
        "user_id": st.session_state.user_id,
    }
    resp = s.post(f"{ORDER_URL}/regular", data=payload)
    return resp.json()

def place_cover_market_order(tradingsymbol, transaction_type, quantity, trigger_price, exchange="NSE"):
    s = _session()
    payload = {
        "exchange": exchange, "tradingsymbol": tradingsymbol,
        "transaction_type": transaction_type, "quantity": quantity,
        "product": "MIS", "validity": "DAY", "variety": "co",
        "order_type": "MARKET", "price": 0, "trigger_price": trigger_price,
        "user_id": st.session_state.user_id,
    }
    resp = s.post(f"{ORDER_URL}/co", data=payload)
    return resp.json()

def place_cover_limit_order(tradingsymbol, transaction_type, quantity, price, trigger_price, exchange="NSE"):
    s = _session()
    payload = {
        "exchange": exchange, "tradingsymbol": tradingsymbol,
        "transaction_type": transaction_type, "quantity": quantity,
        "product": "MIS", "validity": "DAY", "variety": "co",
        "order_type": "LIMIT", "price": price, "trigger_price": trigger_price,
        "user_id": st.session_state.user_id,
    }
    resp = s.post(f"{ORDER_URL}/co", data=payload)
    return resp.json()

def compute_trigger(ltp, transaction_type, sl_pct):
    if transaction_type == "BUY":
        return round(ltp * (1 - sl_pct / 100), 2)
    else:
        return round(ltp * (1 + sl_pct / 100), 2)

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown('<div class="main-header">ZERODHA TRADING DASHBOARD</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{len(SYMBOLS)} symbols loaded • MIS • Intraday</div>', unsafe_allow_html=True)

# ─── Authentication ───────────────────────────────────────────────────────────

with st.expander("🔐 Authentication", expanded=not bool(st.session_state.enctoken)):
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("User ID", key="auth_user", value=st.session_state.user_id)
        st.session_state.user_id = st.session_state.auth_user
        st.text_input("Enctoken", key="auth_enc", value=st.session_state.enctoken, type="password")
        st.session_state.enctoken = st.session_state.auth_enc
        if st.button("✓ Validate Token", use_container_width=True):
            if check_token():
                st.success("✅ Token valid")
                _log("Token validated", "success")
            else:
                st.error("❌ Token invalid")
    with col2:
        st.text_input("Password", type="password", key="auth_pwd")
        st.text_input("2FA/TOTP", key="auth_2fa")
        if st.button("🔑 Login", use_container_width=True):
            if do_login(st.session_state.auth_pwd, st.session_state.auth_2fa):
                st.success("✅ Login successful")
                _log("Login successful", "success")
                st.rerun()
            else:
                st.error("❌ Login failed")

st.markdown("<hr>", unsafe_allow_html=True)

# ─── Main Trading Interface ───────────────────────────────────────────────────

# Row 1: Symbol, Exchange, Transaction
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='section-title'>SYMBOL</div>", unsafe_allow_html=True)
    ticker = st.selectbox("symbol", SYMBOLS, index=SYMBOLS.index("RELIANCE") if "RELIANCE" in SYMBOLS else 0,
                         label_visibility="collapsed")
with col2:
    st.markdown("<div class='section-title'>EXCHANGE</div>", unsafe_allow_html=True)
    exchange = st.selectbox("exchange", ["NSE", "BSE"], label_visibility="collapsed")
with col3:
    st.markdown("<div class='section-title'>TRANSACTION</div>", unsafe_allow_html=True)
    txn_type = st.radio("txn", ["BUY", "SELL"], horizontal=True, label_visibility="collapsed")

# Auto-fetch LTP on symbol change
if st.session_state.get("last_ticker") != ticker:
    st.session_state["last_ticker"] = ticker
    ltp = fetch_ltp(ticker)
    if ltp:
        st.session_state.ltp_cache[ticker] = ltp
        _log(f"LTP: ₹{ltp:,.2f} for {ticker}", "success")

ltp_now = st.session_state.ltp_cache.get(ticker)

# Row 2: LTP and Fetch button
col_ltp, col_fetch = st.columns([3, 1])
with col_ltp:
    if ltp_now:
        st.metric("LAST TRADED PRICE", f"₹{ltp_now:,.2f}")
    else:
        st.warning("Click Fetch LTP")
with col_fetch:
    st.markdown("<div style='margin-top: 1.8rem'></div>", unsafe_allow_html=True)
    if st.button("🔄 FETCH LTP", use_container_width=True):
        ltp = fetch_ltp(ticker)
        if ltp:
            st.session_state.ltp_cache[ticker] = ltp
            st.success(f"LTP: ₹{ltp:,.2f}")
            _log(f"LTP fetched: ₹{ltp:,.2f}", "success")
        else:
            st.error("Failed to fetch LTP")

# Row 3: Quantity Configuration
st.markdown("<div class='section-title'>QUANTITY</div>", unsafe_allow_html=True)
col_qmode, col_bal, col_qty = st.columns(3)
with col_qmode:
    qty_mode = st.radio("mode", ["Manual", "Balance", "SLAMT"], horizontal=True, label_visibility="collapsed")
with col_bal:
    if qty_mode in ["Balance", "SLAMT"]:
        available_balance = st.number_input("Balance (₹)", min_value=0.0, value=10000.0, step=1000.0, format="%.0f")
with col_qty:
    if qty_mode == "Balance" and ltp_now:
        computed_qty = max(1, int((available_balance / ltp_now) * 5))
    elif qty_mode == "SLAMT" and ltp_now:
        sl_amount = st.number_input("SL Amount (₹)", min_value=1.0, value=1000.0, step=100.0, format="%.0f")
        computed_qty = max(1, int(sl_amount / (ltp_now * 0.01)))
    else:
        computed_qty = 1
    quantity = st.number_input("Shares", min_value=1, value=computed_qty, step=1)

# Row 4: Order Type Buttons - CLEAN ARRANGEMENT
st.markdown("<div class='section-title'>ORDER TYPE</div>", unsafe_allow_html=True)

# Create 4 buttons in a row
order_col1, order_col2, order_col3, order_col4 = st.columns(4)

with order_col1:
    if st.button("📊 MARKET", use_container_width=True,
                 type="primary" if st.session_state.selected_order == "MARKET" else "secondary"):
        st.session_state.selected_order = "MARKET"
        st.rerun()

with order_col2:
    if st.button("💰 LIMIT", use_container_width=True,
                 type="primary" if st.session_state.selected_order == "LIMIT" else "secondary"):
        st.session_state.selected_order = "LIMIT"
        st.rerun()

with order_col3:
    if st.button("🛡️ COVER MARKET", use_container_width=True,
                 type="primary" if st.session_state.selected_order == "COVER_MARKET" else "secondary"):
        st.session_state.selected_order = "COVER_MARKET"
        st.rerun()

with order_col4:
    if st.button("⚡ COVER LIMIT", use_container_width=True,
                 type="primary" if st.session_state.selected_order == "COVER_LIMIT" else "secondary"):
        st.session_state.selected_order = "COVER_LIMIT"
        st.rerun()

# Row 5: Order-specific inputs
limit_price = None
trigger_price = None
sl_pct = None

if st.session_state.selected_order in ["LIMIT", "COVER_LIMIT"]:
    col_price, _ = st.columns([1, 2])
    with col_price:
        st.markdown("<div class='section-title'>LIMIT PRICE (₹)</div>", unsafe_allow_html=True)
        default_limit = ltp_now if ltp_now else 0.01
        limit_price = st.number_input("limit", min_value=0.01, value=default_limit, step=0.5, format="%.2f", label_visibility="collapsed")

if st.session_state.selected_order in ["COVER_MARKET", "COVER_LIMIT"]:
    col_sl1, col_sl2 = st.columns(2)
    with col_sl1:
        st.markdown("<div class='section-title'>STOP LOSS %</div>", unsafe_allow_html=True)
        sl_pct = st.number_input("slpct", min_value=0.1, max_value=10.0, value=1.0, step=0.1, format="%.1f", label_visibility="collapsed")
        if ltp_now:
            trigger_price = compute_trigger(ltp_now, txn_type, sl_pct)
            st.caption(f"Calculated: ₹{trigger_price:,.2f}")
    with col_sl2:
        st.markdown("<div class='section-title'>OVERRIDE TRIGGER (₹)</div>", unsafe_allow_html=True)
        manual_trigger = st.number_input("manual", min_value=0.0, value=0.0, step=0.5, format="%.2f", label_visibility="collapsed")
        if manual_trigger > 0:
            trigger_price = manual_trigger

# Row 6: Order Preview & Metrics
if ltp_now:
    # Preview
    preview_text = f"{txn_type} • {quantity} × {ticker}"
    if st.session_state.selected_order in ["LIMIT", "COVER_LIMIT"] and limit_price:
        preview_text += f" @ ₹{limit_price:,.2f}"
    else:
        preview_text += f" @ MARKET"
    if st.session_state.selected_order in ["COVER_MARKET", "COVER_LIMIT"] and trigger_price:
        preview_text += f" • SL: ₹{trigger_price:,.2f}"
        if sl_pct:
            preview_text += f" ({sl_pct}%)"

    st.markdown(f'<div class="info-box">📋 {preview_text} • MIS • Intraday</div>', unsafe_allow_html=True)

    # Metrics for cover orders
    if st.session_state.selected_order in ["COVER_MARKET", "COVER_LIMIT"] and trigger_price and ltp_now:
        sl_amt = abs(ltp_now - trigger_price)
        total_sl = sl_amt * quantity

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">LTP</div>
                <div class="metric-value">₹{ltp_now:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">SL TRIGGER</div>
                <div class="metric-value red">₹{trigger_price:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">MAX LOSS</div>
                <div class="metric-value red">₹{total_sl:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Click 'FETCH LTP' to continue")

# Row 7: Action Buttons
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    place_order = st.button("▶ PLACE ORDER", use_container_width=True, type="primary")
with col_btn2:
    clear_log = st.button("🗑️ CLEAR LOG", use_container_width=True)

if clear_log:
    st.session_state.order_log = []

# Place Order Logic
if place_order:
    if not st.session_state.enctoken:
        st.error("❌ Please authenticate first")
    elif not ltp_now:
        st.error("❌ Please fetch LTP first")
    elif st.session_state.selected_order in ["LIMIT", "COVER_LIMIT"] and (not limit_price or limit_price <= 0):
        st.error("❌ Please enter valid limit price")
    elif st.session_state.selected_order in ["COVER_MARKET", "COVER_LIMIT"] and (not trigger_price or trigger_price <= 0):
        st.error("❌ Please set valid trigger price")
    else:
        with st.spinner("Placing order..."):
            try:
                if st.session_state.selected_order == "MARKET":
                    result = place_market_order(ticker, txn_type, quantity, exchange)
                    desc = f"MARKET {txn_type}"
                elif st.session_state.selected_order == "LIMIT":
                    result = place_limit_order(ticker, txn_type, quantity, limit_price, exchange)
                    desc = f"LIMIT {txn_type} @ ₹{limit_price:,.2f}"
                elif st.session_state.selected_order == "COVER_MARKET":
                    result = place_cover_market_order(ticker, txn_type, quantity, trigger_price, exchange)
                    desc = f"COVER MARKET {txn_type} (SL: ₹{trigger_price:,.2f})"
                elif st.session_state.selected_order == "COVER_LIMIT":
                    result = place_cover_limit_order(ticker, txn_type, quantity, limit_price, trigger_price, exchange)
                    desc = f"COVER LIMIT {txn_type} @ ₹{limit_price:,.2f} (SL: ₹{trigger_price:,.2f})"

                if result.get("status") == "success":
                    oid = result.get("data", {}).get("order_id", "N/A")
                    st.success(f"✅ Order placed! ID: {oid}")
                    _log(f"✅ {desc} | {quantity}×{ticker} | ID: {oid}", "success")
                else:
                    msg = result.get("message", str(result))
                    st.error(f"❌ Order failed: {msg}")
                    _log(f"❌ {desc} failed: {msg}", "error")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                _log(f"❌ Error: {str(e)}", "error")

st.markdown("<hr>", unsafe_allow_html=True)

# ─── Activity Log ────────────────────────────────────────────────────────────

st.markdown("<div class='section-title'>📋 ACTIVITY LOG</div>", unsafe_allow_html=True)

if st.session_state.order_log:
    log_html = '<div class="log-container">'
    for entry in st.session_state.order_log[:20]:
        cls = "log-success" if entry["kind"] == "success" else "log-error" if entry["kind"] == "error" else "log-entry"
        log_html += f'<div class="{cls}">[{entry["ts"]}] {entry["msg"]}</div>'
    log_html += '</div>'
    st.markdown(log_html, unsafe_allow_html=True)
else:
    st.caption("No activity yet")