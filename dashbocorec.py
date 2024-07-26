import streamlit as st 
import plotly.express as px
import pandas as pd
import os
import plotly.figure_factory as ff

# Streamlit setup
st.set_page_config(page_title="Superstore Magazine", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Sample Superstore Magazine Data")
st.header(":chart_with_upwards_trend: Data Science Dashboard")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# File upload and data loading
f1 = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"])
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(f1, encoding="ISO-8859-1")  # Read uploaded file
else:
    # Adjust the path based on your file location
    df = pd.read_csv(r"C:\Users\kidan\OneDrive\Desktop\trainig\Superstores.csv", encoding="ISO-8859-1")

# Ensure 'Order Date' column exists and convert to datetime
if 'Order Date' in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"])

# Sidebar filters
st.sidebar.header("Choose your filters:")
region = st.sidebar.multiselect("Pick your region", df["Region"].unique())
state = st.sidebar.multiselect("Pick the state", df["State"].unique())
city = st.sidebar.multiselect("Pick the city", df["City"].unique())

# Apply filters
filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]
if state:
    filtered_df = filtered_df[filtered_df["State"].isin(state)]
if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]

# Ensure 'month' column exists and populate it
filtered_df["month"] = filtered_df["Order Date"].dt.month_name()

# Category wise sales
category_df = filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()

# Display charts and tables
col1, col2 = st.columns(2)
with col1:
    st.subheader("Category wise sales")
    fig1 = px.bar(category_df, x="Category", y="Sales", text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
                  template='seaborn')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Region wise sales")
    fig2 = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
    fig2.update_traces(text=filtered_df["Region"], textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)

# Time Series Analysis
filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')
linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig3 = px.line(linechart, x="month_year", y="Sales", labels={"Sales": "Amount"}, height=500, width=1000, template="gridon")
st.plotly_chart(fig3, use_container_width=True)

# Additional visualizations and tables
with st.expander("Time Series Data"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv_timeseries = linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download Time Series Data", data=csv_timeseries, file_name="TimeSeries.csv", mime="text/csv")

# Hierarchical view using Treemaps
st.subheader("Hierarchical view of sales using Treemaps")
fig4 = px.treemap(filtered_df, path=["Region", "Category", "Sub-Category"], values="Sales", hover_data=["Sales"], color="Sub-Category")
fig4.update_layout(width=800, height=650)
st.plotly_chart(fig4, use_container_width=True)

# Segment wise sales
col3, col4 = st.columns(2)
with col3:
    st.subheader("Segment wise sales")
    fig5 = px.pie(filtered_df, values="Sales", names="Segment", template="plotly_dark")
    fig5.update_traces(text=filtered_df["Segment"], textposition="inside")
    st.plotly_chart(fig5, use_container_width=True)

with col4:
    st.subheader("Category wise sales")
    fig6 = px.pie(filtered_df, values="Sales", names="Category", template="gridon")
    fig6.update_traces(text=filtered_df["Category"], textposition="inside")
    st.plotly_chart(fig6, use_container_width=True)

# Summary tables and scatter plot
with st.expander("Summary Tables"):
    df_sample = df.head(7)[["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]]
    fig7 = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig7, use_container_width=True)
    st.subheader("Month wise sub-category Table")
    sub_category_year = pd.pivot_table(data=filtered_df, values="Sales", index=["Sub-Category"], columns="month", aggfunc="sum", fill_value=0)
    st.write(sub_category_year.style.background_gradient(cmap="Blues"))

# Scatter plot
scatter_fig = px.scatter(filtered_df, x="Sales", y="Profit", size="Quantity")
scatter_fig.update_layout(title="Relationship between sales and profit using scatter plot",
                          titlefont=dict(size=20),
                          xaxis=dict(title="Sales", titlefont=dict(size=19)),
                          yaxis=dict(title="Profit", titlefont=dict(size=19)))
st.plotly_chart(scatter_fig, use_container_width=True)

# View Data Expander
with st.expander("View Data"):
    st.write(filtered_df.iloc[:800, :].style.background_gradient(cmap="Oranges"))

# Download original dataset
csv_original = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Original Data", data=csv_original, file_name="Data.csv", mime="text/csv")
