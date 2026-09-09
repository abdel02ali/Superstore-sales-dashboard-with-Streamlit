import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

df = pd.read_csv('cleaned_superstore.csv')
df["Order Date"] = pd.to_datetime(df["Order Date"])

st.sidebar.header("Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options = df["Region"].unique(),
    default= df["Region"].unique()
)
selected_category = st.sidebar.multiselect(
        "Select Category",
    options = df["Category"].unique(),
    default= df["Category"].unique()
)

df_filtered = df[(df['Region'].isin(selected_region)) & (df['Category'].isin(selected_category))]


st.title("📊 Superstore Sales Dashboard")
st.write("Interactive analysis of sales, profit, and discount patterns.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${df_filtered['Profit'].sum():,.0f}")
col3.metric("Avg Discount", f"{df_filtered['Discount'].mean()*100:.1f}%")




st.subheader("Profit Margin by Category")
margin = df_filtered.groupby('Category').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum')
).reset_index()
margin['Margin_pct'] = margin['Total_Profit'] / margin['Total_Sales'] * 100


fig, ax = plt.subplots()
ax.bar(margin['Category'], margin['Margin_pct'], color=['#e74c3c','#3498db','#2ecc71'])
ax.set_ylabel('Margin %')
st.pyplot(fig)
st.subheader("Profit Margin By Category")
margin = df.groupby('Category').apply(lambda x:pd.Series({"Margin_pct":x['Profit'].sum()/x["Sales"].sum() * 100})).reset_index()
fig , ax = plt.subplots()
ax.bar(margin['Category'], margin['Margin_pct'],color=['#e74c3c','#3498db','#2ecc71'])
ax.set_ylabel("Margin %")
st.pyplot(fig)


st.subheader("Profit VS Discount")
fig2 , ax2 = plt.subplots()
ax2.scatter(df_filtered['Discount'], df_filtered['Profit'], alpha=0.3, c=df_filtered['Discount'], cmap='coolwarm')
ax.set_ylabel("Discount")
st.pyplot(fig2)

st.info("💡 **Key Insight:** Furniture has a 2.5% profit margin — far lower than Office Supplies (17.0%) and Technology (17.4%) — driven by a higher average discount rate (17.4% vs ~13-16%).")

