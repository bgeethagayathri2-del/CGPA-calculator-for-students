import pandas as pd
import streamlit as st

st.set_page_config(page_title="CGPA Calculator", page_icon="🎓")

# Grade points. CHANGE THESE to match your college's grading scheme.
GRADE_POINTS = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "F": 0}
MAX_POINT = max(GRADE_POINTS.values())

st.title("🎓 CGPA Calculator for Students")
st.caption("A free tool to calculate your SGPA and CGPA and plan your target. "
           "Always check your college's official rules, because grading schemes differ.")

tab1, tab2 = st.tabs(["SGPA / CGPA calculator", "Target planner"])

# ---------- Tab 1: SGPA and CGPA ----------
with tab1:
    st.write("Enter your subjects for each semester: credits and grade. "
             "Click the empty row at the bottom of a table to add more subjects.")
    n_sem = st.number_input("How many semesters do you want to enter?", 1, 8, 1)

    total_points, total_credits = 0.0, 0.0
    for i in range(1, int(n_sem) + 1):
        with st.expander(f"Semester {i}", expanded=(i == 1)):
            default = pd.DataFrame({
                "Subject": [""] * 5,
                "Credits": [0.0] * 5,
                "Grade": [None] * 5,
            })
            edited = st.data_editor(
                default,
                num_rows="dynamic",
                key=f"sem_{i}",
                column_config={
                    "Credits": st.column_config.NumberColumn(min_value=0, max_value=10, step=0.5),
                    "Grade": st.column_config.SelectboxColumn(options=list(GRADE_POINTS)),
                },
            )
            valid = edited.dropna(subset=["Grade", "Credits"])
            valid = valid[valid["Credits"] > 0]
            if valid.empty:
                st.info("Add at least one subject with credits and a grade.")
            else:
                points = (valid["Grade"].map(GRADE_POINTS) * valid["Credits"]).sum()
                credits = valid["Credits"].sum()
                st.metric(f"SGPA (Semester {i})", f"{points / credits:.2f}")
                total_points += points
                total_credits += credits

    st.divider()
    if total_credits > 0:
        st.success(f"🎯 Your CGPA: **{total_points / total_credits:.2f}** "
                   f"(from {total_credits:g} credits)")
    else:
        st.write("Your CGPA will show here once you add subjects.")

# ---------- Tab 2: Target planner ----------
with tab2:
    st.write("Find out the SGPA you need next semester to reach your target CGPA.")
    current = st.number_input("Current CGPA", 0.0, float(MAX_POINT), 7.5, 0.01)
    done = st.number_input("Credits completed so far", 0.0, 300.0, 40.0, 1.0)
    upcoming = st.number_input("Credits in the upcoming semester", 1.0, 40.0, 22.0, 1.0)
    target = st.number_input("Target CGPA", 0.0, float(MAX_POINT), 8.0, 0.01)

    needed = (target * (done + upcoming) - current * done) / upcoming
    if needed > MAX_POINT:
        st.error(f"Not possible in one semester: you would need an SGPA of {needed:.2f}, "
                 f"which is above the maximum of {MAX_POINT}. Try planning over more semesters.")
    elif needed <= 0:
        st.success("You will stay at or above your target even with a low SGPA next semester.")
    else:
        st.info(f"You need an SGPA of at least **{needed:.2f}** next semester "
                f"to reach a CGPA of {target:.2f}.")

st.caption("Unofficial calculator. Results are estimates, so check with your college for official values.")
