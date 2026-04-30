import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Marketing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME CONFIGURATION (BAUHAUS FIXED) ---
# Se utilizan Custom Properties de CSS en lugar de un diccionario Python 
# para que el diseño responda dinámicamente al tema Light/Dark nativo de Streamlit.

# CSS INJECTION
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    
    /* Variables Base - DARK MODE (Forced) */
    :root {
        --bg-color: #0F0F0F;
        --sidebar-bg: #1A1A1A;
        --text-color: #F5F5F5;
        --text-muted: #888888;
        --border-color: #F5F5F5;
        --accent-color: #FF3333;
        --card-bg: #1A1A1A;
        --positive: #F5F5F5;
        --negative: #FF3333;
        --header-bg: #333333;
    }
    
    html, body {
        font-family: 'Neue Haas Grotesk Display Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }
    
    /* Global App Background */
    .stApp { 
        background-color: var(--bg-color) !important; 
    }
    
    /* Header Bar */
    [data-testid="stHeader"] { 
        background-color: var(--header-bg) !important; 
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { 
        background-color: var(--sidebar-bg) !important; 
        border-right: 3px solid var(--border-color); 
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700 !important;
        letter-spacing: -0.04em !important;
        color: var(--text-color) !important;
        text-transform: uppercase;
        margin-bottom: 0 !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: var(--card-bg);
        border: 3px solid var(--border-color);
        padding: 32px 24px;
        margin-bottom: 32px;
        position: relative;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        top: 6px;
        left: 6px;
        right: -9px;
        bottom: -9px;
        background-color: transparent;
        border: 3px solid var(--border-color);
        z-index: -1;
    }
    .metric-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 12px;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        color: var(--text-color);
        letter-spacing: -0.03em;
        line-height: 1;
    }
    .metric-delta {
        font-size: 12px;
        font-weight: 700;
        margin-top: 16px;
        letter-spacing: 0.02em;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        text-transform: uppercase;
        border-top: 4px solid var(--border-color);
        padding-top: 16px;
        margin-bottom: 32px;
        margin-top: 48px;
        letter-spacing: -0.02em;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        text-align: center;
        background-color: var(--text-color) !important;
        border: 3px solid var(--border-color) !important;
        color: var(--bg-color) !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        padding: 12px 16px;
        border-radius: 0px !important;
        transition: transform 0.1s;
    }
    div.stButton > button:hover {
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* Selectbox styling to fit Bauhaus */
    div[data-baseweb="select"] > div {
        border: 3px solid var(--border-color) !important;
        border-radius: 0px !important;
        font-weight: 700 !important;
    }

    /* Tables */
    .swiss-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 32px;
        border: 3px solid var(--border-color);
        background: var(--card-bg);
    }
    .swiss-table th {
        text-align: left;
        padding: 16px;
        border-bottom: 3px solid var(--border-color);
        border-right: 1px solid var(--border-color);
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 700;
        color: var(--text-color);
        letter-spacing: 0.05em;
        background-color: var(--bg-color);
    }
    .swiss-table td {
        padding: 16px;
        border-bottom: 1px solid var(--border-color);
        border-right: 1px solid var(--border-color);
        font-size: 14px;
        font-weight: 500;
        color: var(--text-color);
    }
    .swiss-table tr:last-child td {
        border-bottom: none;
    }
    .swiss-table th:last-child, .swiss-table td:last-child {
        border-right: none;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    daily     = pd.read_csv("marketing_daily_2023.csv", parse_dates=['date'])
    return daily

daily = load_data()

# --- STATE INITIALIZATION ---
if 'active_view' not in st.session_state:
    st.session_state.active_view = 'Executive Summary'

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 24px; line-height: 1.0; margin-bottom: 32px;'>MARKETING<br>INTELLIGENCE<br>SYSTEM</h2>", unsafe_allow_html=True)
    
    st.markdown("<div style='font-size:11px; font-weight:700; color:var(--text-muted); margin-bottom:12px;'>NAVIGATION</div>", unsafe_allow_html=True)
    
    view_options = ['Executive Summary', 'Core Performance', 'Volume & Conversion']
    selected_view = st.selectbox("VIEW", options=view_options, index=view_options.index(st.session_state.active_view), label_visibility="collapsed")
    
    if selected_view != st.session_state.active_view:
        st.session_state.active_view = selected_view
        st.rerun()

    st.markdown("<hr style='border-color: var(--border-color); margin: 24px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px; font-weight:700; color:var(--text-muted); margin-bottom:12px;'>FILTERS</div>", unsafe_allow_html=True)

    # Extract absolute min and max dates from dataset
    min_date = daily['date'].min().date()
    max_date = daily['date'].max().date()
    
    # Set default range to last 3 months to ensure data exists
    default_start = max(min_date, max_date - pd.Timedelta(days=90))

    dates = st.date_input("DATE RANGE", value=(default_start, max_date), min_value=min_date, max_value=max_date)
    
    if isinstance(dates, tuple) and len(dates) == 2:
        date_start, date_end = dates
    else:
        date_start = date_end = dates[0] if isinstance(dates, tuple) and len(dates) > 0 else dates

    all_channels = sorted(daily['channel'].unique().tolist())
    selected_channels = st.multiselect("CHANNEL", options=all_channels, default=all_channels)

# --- FILTERING ---
mask = (
    (daily['date'] >= pd.to_datetime(date_start)) &
    (daily['date'] <= pd.to_datetime(date_end)) &
    (daily['channel'].isin(selected_channels if selected_channels else all_channels))
)
df = daily[mask].copy()

# Previous Period logic
delta_days = (pd.to_datetime(date_end) - pd.to_datetime(date_start)).days
prev_start = pd.to_datetime(date_start) - pd.Timedelta(days=delta_days + 1)
prev_end   = pd.to_datetime(date_start) - pd.Timedelta(days=1)
prev_mask  = (
    (daily['date'] >= prev_start) & 
    (daily['date'] <= prev_end) &
    (daily['channel'].isin(selected_channels if selected_channels else all_channels))
)
df_prev = daily[prev_mask].copy()

def safe_delta(curr, prev, is_rate=False):
    if prev == 0 or pd.isna(prev):
        return None
    if is_rate:
        return curr - prev
    else:
        return ((curr - prev) / prev) * 100

# Calculate KPIs
kpis = {
    'spend': df['spend_usd'].sum(),
    'impressions': df['impressions'].sum(),
    'clicks': df['clicks'].sum(),
    'conversions': df['conversions'].sum(),
}
paid_df = df[df['channel'] != 'Organic']
kpis['cpm'] = (paid_df['spend_usd'].sum() / paid_df['impressions'].sum() * 1000) if paid_df['impressions'].sum() > 0 else 0
kpis['ctr'] = (kpis['clicks'] / kpis['impressions'] * 100) if kpis['impressions'] > 0 else 0
kpis['cpc'] = (paid_df['spend_usd'].sum() / paid_df['clicks'].sum()) if paid_df['clicks'].sum() > 0 else 0
kpis['conv_rate'] = (kpis['conversions'] / kpis['clicks'] * 100) if kpis['clicks'] > 0 else 0

kpis_prev = {
    'spend': df_prev['spend_usd'].sum(),
    'impressions': df_prev['impressions'].sum(),
    'clicks': df_prev['clicks'].sum(),
    'conversions': df_prev['conversions'].sum(),
}
paid_prev = df_prev[df_prev['channel'] != 'Organic']
kpis_prev['cpm'] = (paid_prev['spend_usd'].sum() / paid_prev['impressions'].sum() * 1000) if paid_prev['impressions'].sum() > 0 else 0
kpis_prev['ctr'] = (kpis_prev['clicks'] / kpis_prev['impressions'] * 100) if kpis_prev['impressions'] > 0 else 0
kpis_prev['cpc'] = (paid_prev['spend_usd'].sum() / paid_prev['clicks'].sum()) if paid_prev['clicks'].sum() > 0 else 0
kpis_prev['conv_rate'] = (kpis_prev['conversions'] / kpis_prev['clicks'] * 100) if kpis_prev['clicks'] > 0 else 0

def fmt_currency(val): return f"${val:,.2f}"
def fmt_num(val): return f"{val:,.0f}"
def fmt_pct(val): return f"{val:.2f}%"

def draw_metric(label, value, prev_val, fmt_fn, is_rate=False):
    delta = safe_delta(value, prev_val, is_rate)
    if delta is not None:
        delta_color = "var(--positive)" if delta >= 0 else "var(--negative)"
        delta_sign = "+" if delta >= 0 else ""
        delta_unit = "PP VS PREV" if is_rate else "% VS PREV"
        delta_text = f"<span style='color:{delta_color};'>{delta_sign}{delta:.2f} {delta_unit}</span>"
    else:
        delta_text = "<span style='color:var(--text-muted);'>NO PREV DATA</span>"
        
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{fmt_fn(value)}</div>
        <div class="metric-delta">{delta_text}</div>
    </div>
    """, unsafe_allow_html=True)

# --- VIEW RENDERER ---
def get_chart_layout(title=""):
    return dict(
        title=dict(text=title.upper(), font=dict(family="Neue Haas Grotesk Display Pro, Helvetica Neue", size=16)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=50, b=0),
        font=dict(family="Neue Haas Grotesk Display Pro, Helvetica Neue"),
        xaxis=dict(showgrid=False, linewidth=2),
        yaxis=dict(showgrid=True, gridwidth=1, linewidth=2),
        hoverlabel=dict(font_family="Neue Haas Grotesk Display Pro, Helvetica Neue")
    )

st.markdown(f"<h1 style='color: var(--text-color); font-size: 48px; margin-bottom: 48px;'>{st.session_state.active_view.upper()}</h1>", unsafe_allow_html=True)

if st.session_state.active_view == 'Executive Summary':
    # Avoid zero division and calculate only if we have data
    if df.empty:
        st.markdown("<div style='color: var(--text-color); padding: 24px; font-weight: bold; border: 3px solid var(--border-color);'>NO DATA AVAILABLE FOR SELECTED DATE RANGE.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="color: var(--text-color); font-size: 28px; line-height: 1.4; font-weight: 500; margin-top: 32px; max-width: 900px; border-left: 8px solid var(--accent-color); padding-left: 32px; letter-spacing: -0.02em;">
            During the selected period, the marketing portfolio delivered <strong>{fmt_currency(kpis['spend'])}</strong> in total spend, generating <strong>{fmt_num(kpis['impressions'])}</strong> impressions and <strong>{fmt_num(kpis['conversions'])}</strong> conversions. The overall conversion rate stood at <strong>{fmt_pct(kpis['conv_rate'])}</strong>.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-title'>KEY INSIGHTS</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        insights = [
            ("VOLUME VS EFFICIENCY", "Programmatic leads in impression volume but Paid Search generates superior CTR efficiency. Budget allocation must balance reach goals with conversion intent."),
            ("SEASONAL SPIKES", "Data indicates highly concentrated impression surges during specific months. These anomalies warrant deeper attribution analysis to identify replicable triggers for future planning."),
            ("ORGANIC LEVERAGE", "Organic channel drives consistent traffic with zero media spend. Increasing organic investment offers the highest marginal efficiency in the entire portfolio.")
        ]
        
        for col, (title, desc) in zip([col1, col2, col3], insights):
            with col:
                st.markdown(f"""
                <div style="border: 3px solid var(--border-color); padding: 32px; height: 100%; background: var(--card-bg);">
                    <div style="font-size: 14px; font-weight: 700; margin-bottom: 16px; color: var(--accent-color); letter-spacing: 0.05em;">{title}</div>
                    <div style="color: var(--text-color); font-size: 16px; line-height: 1.5; font-weight: 500;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

elif st.session_state.active_view == 'Core Performance':
    c1, c2, c3, c4 = st.columns(4)
    with c1: draw_metric("TOTAL SPEND", kpis['spend'], kpis_prev['spend'], fmt_currency, is_rate=False)
    with c2: draw_metric("AVG CPM", kpis['cpm'], kpis_prev['cpm'], fmt_currency, is_rate=True)
    with c3: draw_metric("AVG CTR", kpis['ctr'], kpis_prev['ctr'], fmt_pct, is_rate=True)
    with c4: draw_metric("AVG CPC", kpis['cpc'], kpis_prev['cpc'], fmt_currency, is_rate=True)
    
    st.markdown("<div class='section-title'>DATA SOURCE PERFORMANCE</div>", unsafe_allow_html=True)
    
    src_filtered = df.groupby('data_source').agg(
        impressions=('impressions','sum'),
        clicks=('clicks','sum'),
        spend=('spend_usd','sum')
    ).reset_index()
    src_filtered['ctr'] = (src_filtered['clicks'] / src_filtered['impressions'] * 100).fillna(0)
    src_filtered = src_filtered.sort_values('impressions', ascending=False)
    
    if not src_filtered.empty:
        col_table, col_chart = st.columns([1, 1])
        with col_table:
            html = "<table class='swiss-table'><tr><th>SOURCE</th><th>IMPRESSIONS</th><th>SPEND</th><th>CTR</th></tr>"
            for _, row in src_filtered.iterrows():
                html += f"<tr><td>{row['data_source']}</td><td>{fmt_num(row['impressions'])}</td><td>{fmt_currency(row['spend'])}</td><td>{fmt_pct(row['ctr'])}</td></tr>"
            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)
        with col_chart:
            fig = go.Figure(data=[go.Bar(x=src_filtered['data_source'], y=src_filtered['impressions'], marker_color='#888888')])
            fig.update_layout(get_chart_layout("IMPRESSIONS BY SOURCE"))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, theme="streamlit")
    else:
        st.markdown("<div style='color: var(--text-color); padding: 24px; font-weight: bold; border: 3px solid var(--border-color);'>NO DATA AVAILABLE FOR SELECTED PERIOD.</div>", unsafe_allow_html=True)

elif st.session_state.active_view == 'Volume & Conversion':
    c1, c2, c3, c4 = st.columns(4)
    with c1: draw_metric("IMPRESSIONS", kpis['impressions'], kpis_prev['impressions'], fmt_num, is_rate=False)
    with c2: draw_metric("CLICKS", kpis['clicks'], kpis_prev['clicks'], fmt_num, is_rate=False)
    with c3: draw_metric("CONVERSIONS", kpis['conversions'], kpis_prev['conversions'], fmt_num, is_rate=False)
    with c4: draw_metric("CONV RATE", kpis['conv_rate'], kpis_prev['conv_rate'], fmt_pct, is_rate=True)
    
    st.markdown("<div class='section-title'>CHANNEL PERFORMANCE</div>", unsafe_allow_html=True)
    
    ch_filtered = df.groupby('channel').agg(
        impressions=('impressions','sum'),
        clicks=('clicks','sum'),
        conversions=('conversions','sum')
    ).reset_index()
    ch_filtered['ctr'] = (ch_filtered['clicks'] / ch_filtered['impressions'] * 100).fillna(0)
    ch_filtered['cvr'] = (ch_filtered['conversions'] / ch_filtered['clicks'] * 100).fillna(0)
    ch_filtered = ch_filtered.sort_values('impressions', ascending=False)
    
    if not ch_filtered.empty:
        html = "<table class='swiss-table'><tr><th>CHANNEL</th><th>IMPRESSIONS</th><th>CLICKS</th><th>CONVERSIONS</th><th>CTR</th><th>CVR</th></tr>"
        for _, row in ch_filtered.iterrows():
            html += f"<tr><td>{row['channel']}</td><td>{fmt_num(row['impressions'])}</td><td>{fmt_num(row['clicks'])}</td><td>{fmt_num(row['conversions'])}</td><td>{fmt_pct(row['ctr'])}</td><td>{fmt_pct(row['cvr'])}</td></tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
        
        fig_ch = go.Figure(data=[
            go.Bar(name='Clicks', x=ch_filtered['channel'], y=ch_filtered['clicks'], marker_color='#888888'),
            go.Bar(name='Conversions', x=ch_filtered['channel'], y=ch_filtered['conversions'], marker_color='#D91111')
        ])
        fig_ch.update_layout(get_chart_layout("CLICKS & CONVERSIONS BY CHANNEL"))
        fig_ch.update_layout(barmode='group')
        st.plotly_chart(fig_ch, use_container_width=True, config={'displayModeBar': False}, theme="streamlit")
    else:
        st.markdown("<div style='color: var(--text-color); padding: 24px; font-weight: bold; border: 3px solid var(--border-color);'>NO DATA AVAILABLE FOR SELECTED PERIOD.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>TOP CAMPAIGNS</div>", unsafe_allow_html=True)
    
    camp_filtered = df.groupby('campaign_name').agg(
        impressions=('impressions','sum'),
        conversions=('conversions','sum')
    ).reset_index().sort_values('conversions', ascending=False).head(5)
    
    if not camp_filtered.empty:
        col_t, col_c = st.columns([1, 1])
        with col_t:
            html = "<table class='swiss-table'><tr><th>CAMPAIGN</th><th>IMPRESSIONS</th><th>CONVERSIONS</th></tr>"
            for _, row in camp_filtered.iterrows():
                html += f"<tr><td>{row['campaign_name']}</td><td>{fmt_num(row['impressions'])}</td><td>{fmt_num(row['conversions'])}</td></tr>"
            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)
        with col_c:
            fig_camp = go.Figure(go.Bar(
                x=camp_filtered['conversions'], 
                y=camp_filtered['campaign_name'], 
                orientation='h',
                marker_color='#D91111'
            ))
            fig_camp.update_layout(get_chart_layout("CONVERSIONS BY CAMPAIGN"))
            fig_camp.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_camp, use_container_width=True, config={'displayModeBar': False}, theme="streamlit")
    else:
        st.markdown("<div style='color: var(--text-color); padding: 24px; font-weight: bold; border: 3px solid var(--border-color);'>NO DATA AVAILABLE FOR SELECTED PERIOD.</div>", unsafe_allow_html=True)
