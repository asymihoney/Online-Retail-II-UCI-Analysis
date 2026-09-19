import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-commerce Customer Analytics", layout="wide")

@st.cache_data
def load_data():
    country_monthly = pd.read_csv('country_monthly_summary.csv')
    product_country = pd.read_csv('product_country_summary.csv')
    rfm = pd.read_csv('customer_rfm_segments.csv')
    return country_monthly, product_country, rfm

country_monthly, product_country, rfm = load_data()

st.title("📊 E-commerce Sales & Customer Analytics")
st.markdown("Analysis of UK online retailer transactions (2009–2011)")

# Sidebar Filters
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Country",
    options=country_monthly['Country'].unique(),
    default=['United Kingdom']
)

segments = st.sidebar.multiselect(
    "Customer Segment",
    options=rfm['Segment'].unique(),
    default=rfm['Segment'].unique()
)

cm_filtered = country_monthly[country_monthly['Country'].isin(countries)]
pc_filtered = product_country[product_country['Country'].isin(countries)]
rfm_filtered = rfm[rfm['Segment'].isin(segments)]

# KPI Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"£{cm_filtered['Revenue'].sum():,.0f}")
col2.metric("Total Orders", f"{cm_filtered['Orders'].sum():,}")
col3.metric("Unique Customers", f"{cm_filtered['Customers'].sum():,}")
avg_order = cm_filtered['Revenue'].sum() / cm_filtered['Orders'].sum() if cm_filtered['Orders'].sum() > 0 else 0
col4.metric("Avg Order Value", f"£{avg_order:,.2f}")

# Monthly Revenue Chart
st.subheader("Monthly Revenue Trend")
monthly_agg = cm_filtered.groupby('Month')['Revenue'].sum().reset_index()
fig = px.line(monthly_agg, x='Month', y='Revenue', markers=True)
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
top_products = pc_filtered.groupby('Description')['Revenue'].sum().nlargest(10).reset_index()
st.dataframe(top_products, use_container_width=True)