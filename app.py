import streamlit as st
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv("processed_ml_data.csv")


df.drop_duplicates(inplace=True)

df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

df.dropna(inplace=True)

df["title"] = df["title"].astype(str).str.lower()
df["Skills"] = df["Skills"].astype(str).str.lower()
df["state"] = df["state"].astype(str).str.lower()
df["experienceLevel"] = df["experienceLevel"].astype(str).str.lower()


df["features"] = (
    df["title"] + " " +
    df["Skills"] + " " +
    df["state"] + " " +
    df["experienceLevel"]
)


vectorizer = TfidfVectorizer(stop_words="english")

X = vectorizer.fit_transform(df["features"])

y = df["title"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier()

model.fit(X_train, y_train)


st.title("ML Job Recommendation System")

st.write("Enter your details to get job recommendations")


job = st.text_input("Job Title")
skills = st.text_input("Skills")
state = st.text_input("State")
exp = st.text_input("Experience Level")


if st.button("Recommend Jobs"):

    job = job.lower()
    skills = skills.lower()
    state = state.lower()
    exp = exp.lower()

    
    recommended_jobs = df[
        (df["title"].str.contains(job, na=False)) &
        (df["Skills"].str.contains(skills, na=False)) &
        (df["state"].str.contains(state, na=False)) &
        (df["experienceLevel"].str.contains(exp, na=False))
    ]

    if recommended_jobs.empty:
        st.warning("No jobs found matching all filters.")

    else:
        st.subheader("Recommended Jobs")

        st.dataframe(
            recommended_jobs[
                ["companyName", "Salary", "contractType", "city", "state"]
            ]
        )
