import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- DATA ----------
df = pd.read_csv("student_bersih.csv")

# ---------- SIDEBAR ----------
st.sidebar.header("Filter data")
gender_opt   = st.sidebar.multiselect("Gender", df["gender"].unique(), df["gender"].unique())  
diet_opt     = st.sidebar.multiselect("Diet quality", df["diet_quality"].unique(),
                                      df["diet_quality"].unique())
parent_opt   = st.sidebar.multiselect("Parental education",
                                      df["parental_education_level"].unique(),
                                      df["parental_education_level"].unique())

mask = (df["gender"].isin(gender_opt) &
        df["diet_quality"].isin(diet_opt) &
        df["parental_education_level"].isin(parent_opt))
data = df[mask]

# ---------- LAYOUT ----------
st.title("Student Habits vs Academic Performance")

tab1, tab2, tab3 = st.tabs(["Overview", "Correlations", "Predetermined Charts"])

with tab1:
    st.subheader("Statistik ringkas")
    st.dataframe(data.describe())
    st.write(f"Jumlah data tersaring: **{len(data)} siswa**")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Rata-rata Exam Score", round(data["exam_score"].mean(), 2))
    with col2:
        st.metric("Rata-rata Study Hours", round(data["study_hours_per_day"].mean(), 2))

with tab2:
    st.subheader("Heatmap Korelasi")
    corr = data.select_dtypes(include=["int64", "float64"]).corr()
    fig = px.imshow(corr,
                    text_auto=".2f",
                    color_continuous_scale="RdBu_r",
                    title="Correlation Matrix")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Bar chart: mean exam per gender / diet / parental education
    st.subheader("Bar Chart – Rata Exam Score per Kategori")
    cat = st.selectbox("Pilih kategori:",
                       ["gender", "diet_quality",
                        "parental_education_level"])
    mean_scores = data.groupby(cat)["exam_score"].mean().reset_index()
    fig_bar = px.bar(mean_scores, x=cat, y="exam_score",
                     color=cat, text_auto=".2f",
                     title=f"Mean Exam Score by {cat.replace('_',' ').title()}")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Scatter: study hours vs exam
    fig_sc1 = px.scatter(
        data, x="study_hours_per_day", y="exam_score",
        color="gender", trendline="ols",
        labels={"study_hours_per_day": "Study Hours/Day"}
    )
    fig_sc1.update_yaxes(range=[0, 100])   # paksa 0–100
    st.plotly_chart(fig_sc1, use_container_width=True)

    # Scatter: sleep vs exam
    st.subheader("Scatter – Sleep Hours vs Exam Score")
    fig_sc2 = px.scatter(data, x="sleep_hours", y="exam_score",
                         color="mental_health_rating", trendline="ols",
                         labels={"sleep_hours":"Sleep Hours"})
    st.plotly_chart(fig_sc2, use_container_width=True)

    # Line: attendance vs exam (sorted)
    st.subheader("Line - Attendance % vs Exam Score")
    tmp = data.sort_values("attendance_percentage")
    fig_line = px.line(tmp, x="attendance_percentage", y="exam_score",
                       markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

    # Pie chart: extracurricular participation
    st.subheader("Pie - Extracurricular Participation")
    pie = (
        data["extracurricular_participation"]
        .value_counts()
        .reset_index(name="count")                 # kolom 'count'
        .rename(columns={"index": "extracurricular_participation"})
    )
    fig_pie = px.pie(
        pie,
        names="extracurricular_participation",     # nama kategori
        values="count",                            # jumlahnya
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)