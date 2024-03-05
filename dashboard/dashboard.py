import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


def create_by_hour_df(df):
    hour_df = df.groupby(by="hour").agg({
        "PM2.5": "mean",
        "PM10": "mean",
    })

    hour_df = hour_df.reset_index()

    return hour_df


def create_by_last_month_df(df):
    last_year_df = df.loc[(df["year"] == df["year"].max())]
    last_month_df = last_year_df.loc[(last_year_df["month"] == last_year_df["month"].max())]

    last_month_df = last_month_df.groupby(by="station").agg({
        "PM2.5": "mean",
    })

    last_month_df = last_month_df.sort_values(by="PM2.5")

    last_month_df = last_month_df.reset_index()

    return last_month_df


all_df = pd.read_csv("all_data.csv")

all_df["date"] = pd.to_datetime(all_df["date"])

min_date = all_df["date"].min()
max_date = all_df["date"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["date"] >= str(start_date)) & (all_df["date"] <= str(end_date))]

hour_df = create_by_hour_df(main_df)
last_month_df = create_by_last_month_df(main_df)

st.header('Dashboard Kualitas Udara :sparkles:')

st.subheader('Kualitas Harian')

col1, col2 = st.columns(2)

with col1:
    pm25 = round(main_df["PM2.5"].mean(), 2)
    st.metric("PM2.5", value=pm25)

with col2:
    pm10 = round(main_df["PM10"].mean(), 2)
    st.metric("PM10", value=pm10)

st.subheader('Kadar PM2.5 Terhadap Jam')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    hour_df["hour"],
    hour_df["PM2.5"],
)

st.pyplot(fig)

st.subheader('Kadar PM10 Terhadap Jam')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    hour_df["hour"],
    hour_df["PM10"],
)

st.pyplot(fig)

st.subheader('Kadar PM10 Terhadap Station pada Bulan Terakhir')

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(y="PM2.5", x="station", data=last_month_df)

st.pyplot(fig)