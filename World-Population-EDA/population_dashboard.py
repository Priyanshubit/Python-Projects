import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="🌍 World Population Dashboard", layout="wide")
st.title("🌍 World Population EDA Dashboard")
st.markdown("Interactively explore global‑population trends from **1970 to 2022**.")

@st.cache_data
def load_data():
    df_wide = pd.read_csv("cleaned_population_data.csv")
    pop_cols = [c for c in df_wide.columns if c[:4].isdigit() and "Population" in c]
    df_long = df_wide.melt(
        id_vars=["Country", "Continent"],
        value_vars=pop_cols,
        var_name="Year",
        value_name="Population"
    )
    df_long["Year"] = df_long["Year"].str.extract(r"(\d{4})").astype(int)
    df_long["Population"] = pd.to_numeric(df_long["Population"], errors="coerce")
    df_long.dropna(subset=["Population"], inplace=True)
    return df_wide, df_long

df, df_long = load_data()

if st.checkbox("📄  Show raw data table"):
    st.dataframe(df)

st.subheader("🏆  Top 10 Countries by Population (2022)")
top10 = df[["Country", "2022 Population"]].sort_values("2022 Population", ascending=False).reset_index(drop=True)
st.dataframe(top10, height=260)

st.subheader("🔗  Correlation Between Census Years")
heat_cols = ["2022 Population", "2020 Population", "2015 Population", "2010 Population",
             "2000 Population", "1990 Population", "1980 Population", "1970 Population"]
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.heatmap(df[heat_cols].corr(), annot=True, cmap="coolwarm", ax=ax1)
st.pyplot(fig1)
plt.close(fig1)

st.subheader("📈  Population Growth by Continent (1970‑2022)")
all_continents = df_long["Continent"].unique()
chosen_continents = st.multiselect("Select continents to display", all_continents, default=list(all_continents))
plot_data = df_long[df_long["Continent"].isin(chosen_continents)]
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=plot_data, x="Year", y="Population", hue="Continent", ax=ax2, marker="o")
ax2.set_ylabel("Population")
st.pyplot(fig2)
plt.close(fig2)

st.subheader("🚨  Outlier Detection by Continent")
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.boxplot(data=plot_data, x="Continent", y="Population", ax=ax3)
ax3.tick_params(axis="x", rotation=45)
st.pyplot(fig3)
plt.close(fig3)

st.markdown("---")
st.success("✅ Dashboard ready – explore, filter, and gain insights!")