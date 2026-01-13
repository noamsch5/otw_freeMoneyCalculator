import streamlit as st
import pandas as pd

# --- Security Check (Simple Internal Password) ---
def check_password():
    """Returns `True` if the user had the correct password."""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    st.title("🔐 Internal Access Only")
    password = st.text_input("Enter Label Password", type="password")
    
    # Set your internal password here (e.g., 'otw2026')
    if st.button("Login"):
        if password == "otw2026": 
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Incorrect password")
    return False

if not check_password():
    st.stop()

# --- Main Application ---
st.title('Spotify "Free Money" Calculator 💰')
st.caption("Internal Tool for On The Way Records - Passive Revenue Analysis")

st.write("---")

# --- Section 1: Inputs ---
st.sidebar.header('Global Settings')

# Input: Total Streams
total_streams = st.sidebar.number_input(
    'Total Streams (28 Days)', 
    min_value=0, 
    value=28000, 
    step=100,
    help="Enter the total number of streams from the Spotify for Artists dashboard."
)

# Input: Rate Per Stream
rate_per_stream = st.sidebar.number_input(
    'Avg. Rate Per Stream ($)', 
    min_value=0.0000, 
    value=0.0024, 
    format="%.4f",
    help="Standard average is often between $0.003 and $0.005, adjust based on your actual payouts."
)

# --- Section 2: Traffic Sources Breakdown ---
st.header('1. Traffic Sources Breakdown')
st.info('Please enter the percentages found in the "Source of Streams" tab.')

col1, col2 = st.columns(2)

# Passive Sources
with col1:
    st.subheader("🟢 Passive Sources (Free Money)")
    st.markdown("Algorithmic & Editorial")
    
    algo_pct = st.number_input('Algorithmic % (Discover Weekly, Radio, etc.)', 0, 100, 15)
    edit_pct = st.number_input('Editorial % (Official Playlists)', 0, 100, 12)

# Active Sources
with col2:
    st.subheader("🔴 Active Sources (Owned)")
    st.markdown("Profile, Library & User Playlists")
    
    library_pct = st.number_input('Artist Profile & Catalog %', 0, 100, 40)
    user_playlist_pct = st.number_input("Listener's Playlists %", 0, 100, 22)
    other_pct = st.number_input('Other / External Sources %', 0, 100, 11)

# Validation
total_pct = algo_pct + edit_pct + library_pct + user_playlist_pct + other_pct
if total_pct != 100:
    st.warning(f'⚠️ Notice: Total percentage is {total_pct}% (Should be 100%)')

# --- Section 3: Logic & Calculations ---
# Calculate Streams based on %
algo_streams = total_streams * (algo_pct / 100)
edit_streams = total_streams * (edit_pct / 100)
passive_streams = algo_streams + edit_streams

active_streams = total_streams - passive_streams

# Logic: Free Money Percentage
# Formula: (Algorithmic + Editorial) / Total * 100
free_money_percentage = (passive_streams / total_streams) * 100 if total_streams > 0 else 0

# Logic: Revenue Estimation
total_revenue = total_streams * rate_per_stream
passive_revenue = passive_streams * rate_per_stream 
active_revenue = total_revenue - passive_revenue

# --- Section 4: Dashboard Output ---
st.write("---")
st.header('2. Revenue Analysis')

# KPIs
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Est. Revenue", f"${total_revenue:,.2f}")
kpi2.metric("Free Money %", f"{free_money_percentage:.1f}%", help="Percentage of streams coming from Spotify's recommendation engines.")
kpi3.metric("Passive Profit (Free Money)", f"${passive_revenue:,.2f}", delta_color="normal")

# Detailed Table
st.subheader("Detailed Breakdown")
data = {
    "Source Category": ["Algorithmic", "Editorial", "Active/Owned/Other", "Total"],
    "Type": ["Passive (Free Money)", "Passive (Free Money)", "Active Effort", "-"],
    "Share (%)": [f"{algo_pct}%", f"{edit_pct}%", f"{100 - algo_pct - edit_pct}%", "100%"],
    "Calculated Streams": [f"{int(algo_streams):,}", f"{int(edit_streams):,}", f"{int(active_streams):,}", f"{int(total_streams):,}"],
    "Est. Revenue ($)": [f"${algo_streams * rate_per_stream:,.2f}", f"${edit_streams * rate_per_stream:,.2f}", f"${active_streams * rate_per_stream:,.2f}", f"${total_revenue:,.2f}"]
}
df = pd.DataFrame(data)
st.table(df)

# Footer
st.markdown("---")
st.caption("Developed for On The Way Records | Data based on Spotify for Artists 28-day cycle.")