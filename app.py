import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-commerce Customer Analytics", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_transactions.csv', parse_dates=['InvoiceDate'])
    rfm = pd.read_csv('customer_rfm_segments.csv')
    monthly = pd.read_csv('monthly_summary.csv')
    return df, rfm, monthly

df, rfm, monthly = load_data()

st.title("📊 E-commerce Sales & Customer Analytics")
st.markdown("Analysis of UK online retailer transactions (2009–2011)")

# Sidebar Filters
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Country",
    options=df['Country'].unique(),
    default=['United Kingdom']
)

segments = st.sidebar.multiselect(
    "Customer Segment",
    options=rfm['Segment'].unique(),
    default=rfm['Segment'].unique()
)

df_filtered = df[df['Country'].isin(countries)]
rfm_filtered = rfm[rfm['Segment'].isin(segments)]

# KPI Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"£{df_filtered['TotalPrice'].sum():,.0f}")
col2.metric("Total Orders", f"{df_filtered['Invoice'].nunique():,}")
col3.metric("Unique Customers", f"{df_filtered['Customer ID'].nunique():,}")
col4.metric("Avg Order Value", f"£{df_filtered.groupby('Invoice')['TotalPrice'].sum().mean():,.2f}")

# Monthly Revenue Chart
st.subheader("Monthly Revenue Trend")
monthly_filtered = df_filtered.groupby(df_filtered['InvoiceDate'].dt.to_period('M').astype(str))['TotalPrice'].sum().reset_index()
monthly_filtered.columns = ['Month', 'Revenue']

fig = px.line(monthly_filtered, x='Month', y='Revenue', markers=True)
st.plotly_chart(fig, use_container_width=True)

# RFM Segment Visuals
st.subheader("Customer Segments")
col1, col2 = st.columns(2)

with col1:
    seg_counts = rfm_filtered['Segment'].value_counts().reset_index()
    fig1 = px.bar(seg_counts, x='Segment', y='count', title="Customers by Segment")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    seg_value = rfm_filtered.groupby('Segment')['Monetary'].sum().reset_index()
    fig2 = px.pie(seg_value, names='Segment', values='Monetary', title="Revenue Share by Segment")
    st.plotly_chart(fig2, use_container_width=True)
    
# Top Products Table
st.subheader("Top 10 Products by Revenue")
top_products = df_filtered.groupby('Description')['TotalPrice'].sum().nlargest(10).reset_index()
st.dataframe(top_products, use_container_width=True)