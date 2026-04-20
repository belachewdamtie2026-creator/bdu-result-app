import streamlit as st
import pandas as pd

st.set_page_config(page_title="BDU Result Calculator", layout="wide")

# CSS - ዲዛይኑን መጀመሪያ መጫን
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #2C3E50; }
    div.stButton > button:first-child {
        background-color: #1A365D !important;
        color: white !important;
        border-radius: 10px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    .result-slip {
        background-color: white;
        padding: 25px;
        border: 2px solid #1A365D;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #1A365D;
        margin-top: 20px;
    }
    .slip-header { text-align: center; border-bottom: 2px solid #1A365D; padding-bottom: 10px; margin-bottom: 20px; }
    .slip-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
    .slip-table th { text-align: left; padding: 10px; background-color: #f8f9fa; border-bottom: 1px solid #1A365D; }
    .slip-table td { padding: 10px; border-bottom: 1px solid #eee; color: #2C3E50; }
    </style>
    """, unsafe_allow_html=True)

def get_grade_info(mark):
    if mark >= 83: return 4.0, "A"
    elif mark >= 80: return 3.75, "A-"
    elif mark >= 75: return 3.5, "B+"
    elif mark >= 68: return 3.0, "B"
    elif mark >= 65: return 2.75, "B-"
    elif mark >= 60: return 2.5, "C+"
    elif mark >= 50: return 2.0, "C"
    elif mark >= 45: return 1.75, "C-"
    elif mark >= 40: return 1.0, "D"
    else: return 0.0, "F"

st.title("🎓 BDU Result Calculator")

num_courses = 10
course_data = []

h1, h2, h3, h4, h5 = st.columns([3, 1, 1, 1, 1])
h1.write("**የኮርሱ ስም**")
h2.write("**ECTS**")
h3.write("**ውጤት (100)**")
h4.write("**Grade**")
h5.write("**Points**")

for i in range(num_courses):
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
    with col1: c_name = st.text_input(f"C{i}", key=f"n_{i}", label_visibility="collapsed", placeholder=f"ኮርስ {i+1}")
    with col2: ects = st.number_input(f"E{i}", min_value=1.0, value=5.0, key=f"e_{i}", label_visibility="collapsed")
    with col3: mark = st.number_input(f"M{i}", min_value=0.0, max_value=100.0, value=0.0, key=f"m_{i}", label_visibility="collapsed")
    
    ng, letter = get_grade_info(mark)
    gp = ects * ng
    
    with col4: st.write(f"**{letter}**" if mark > 0 else "-")
    with col5: st.write(f"**{gp:.2f}**" if mark > 0 else "-")
    
    if mark > 0:
        course_data.append({"Course": c_name if c_name else f"Course {i+1}", "ECTS": ects, "Mark": mark, "Grade": letter, "GP": gp})

if st.button("ውጤቴን አስላ"):
    if course_data:
        total_ects = sum(c['ECTS'] for c in course_data)
        total_gp = sum(c['GP'] for c in course_data)
        gpa = total_gp / total_ects
        
        st.balloons()
        
        # የሰንጠረዥ ረድፎችን ማዘጋጀት
        rows_html = ""
        for c in course_data:
            rows_html += f"<tr><td>{c['Course']}</td><td>{c['ECTS']}</td><td>{c['Mark']}</td><td><b>{c['Grade']}</b></td></tr>"

        # ሙሉውን Slip በ HTML ማቅረብ
        slip_content = f"""
        <div class="result-slip">
            <div class="slip-header">
                <h2 style="margin:0;">BAHIR DAR UNIVERSITY</h2>
                <p style="margin:0; color: #718096;">Unofficial Student Semester Result Slip</p>
            </div>
            <table class="slip-table">
                <thead>
                    <tr><th>Course Title</th><th>ECTS</th><th>Mark</th><th>Grade</th></tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            <div style="display: flex; justify-content: space-between; background: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee;">
                <div><b>Total ECTS:</b> {int(total_ects)}</div>
                <div><b>Total GP:</b> {total_gp:.2f}</div>
                <div style="color: #1A365D; font-size: 20px;"><b>GPA: {gpa:.2f}</b></div>
            </div>
            <div style="text-align: center; margin-top: 20px; font-size: 11px; color: #718096; border-top: 1px solid #eee; padding-top: 10px;">
                Generated on 2026 | Developer: <b>Belachew Damtie</b>
            </div>
        </div>
        """
        st.markdown(slip_content, unsafe_allow_html=True)
    else:
        st.warning("እባክህ መጀመሪያ ውጤት አስገባ።")

st.markdown("<p style='text-align:center; color:#718096; padding-top:30px;'>Developer: Belachew Damtie</p>", unsafe_allow_html=True)
