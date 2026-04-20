import streamlit as st
import pandas as pd

st.set_page_config(page_title="BDU Result Calculator", layout="wide")

# CSS - ለሞባይል እይታ የተስተካከለ
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #2C3E50; }
    
    /* በስልክ ላይ ኮለሞችን ጎን ለጎን ለማድረግ */
    [data-testid="column"] {
        display: flex;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 5px !important;
    }
    
    /* የሳጥኖቹን ስፋት ማስተካከል */
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        width: 100% !important;
    }

    div.stButton > button:first-child {
        background-color: #1A365D !important;
        color: white !important;
        border-radius: 10px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: bold !important;
    }

    .result-slip {
        background-color: white;
        padding: 20px;
        border: 2px solid #1A365D;
        border-radius: 15px;
        color: #1A365D;
        margin-top: 20px;
        overflow-x: auto; /* ለትናንሽ ስልኮች ሰንጠረዡ እንዳይቆረጥ */
    }
    .slip-header { text-align: center; border-bottom: 2px solid #1A365D; padding-bottom: 10px; margin-bottom: 20px; }
    .slip-table { width: 100%; border-collapse: collapse; font-size: 14px; }
    .slip-table th, .slip-table td { text-align: left; padding: 8px; border-bottom: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

def get_grade_info(mark):
    if mark >= 90: return 4.0, "A+"
    elif mark >= 85: return 4.0, "A"
    elif mark >= 80: return 3.75, "A-"
    elif mark >= 75: return 3.5, "B+"
    elif mark >= 70: return 3.0, "B"
    elif mark >= 65: return 2.75, "B-"
    elif mark >= 60: return 2.5, "C+"
    elif mark >= 50: return 2.0, "C"
    elif mark >= 45: return 1.75, "C-"
    elif mark >= 40: return 1.0, "D"
    elif mark >= 30: return 0.0, "FX"
    else: return 0.0, "F"

st.title("🎓 BDU Result Calculator")

num_courses = 10
course_data = []

# የርዕስ ክፍሎች በስልክ ላይ እንዳይዝረከረኩ
h1, h2, h3, h4, h5 = st.columns([2.5, 1, 1.2, 0.8, 1])
h1.caption("ኮርስ")
h2.caption("ECTS")
h3.caption("ውጤት")
h4.caption("Gr")
h5.caption("Pt")

for i in range(num_courses):
    col1, col2, col3, col4, col5 = st.columns([2.5, 1, 1.2, 0.8, 1])
    with col1: c_name = st.text_input(f"C{i}", key=f"n_{i}", label_visibility="collapsed", placeholder=f"ኮርስ {i+1}")
    with col2: ects = st.number_input(f"E{i}", min_value=1.0, value=5.0, key=f"e_{i}", label_visibility="collapsed")
    with col3: mark = st.number_input(f"M{i}", min_value=0.0, max_value=100.0, value=0.0, key=f"m_{i}", label_visibility="collapsed")
    
    ng, letter = get_grade_info(mark)
    gp = ects * ng
    
    with col4: st.write(f"**{letter}**" if mark > 0 else "-")
    with col5: st.write(f"**{gp:.1f}**" if mark > 0 else "-")
    
    if mark > 0:
        course_data.append({"Course": c_name if c_name else f"Course {i+1}", "ECTS": ects, "Mark": mark, "Grade": letter, "GP": gp})

if st.button("ውጤቴን አስላ"):
    if course_data:
        total_ects = sum(c['ECTS'] for c in course_data)
        total_gp = sum(c['GP'] for c in course_data)
        gpa = total_gp / total_ects
        
        st.balloons()
        
        rows_html = ""
        for c in course_data:
            rows_html += f"<tr><td>{c['Course']}</td><td>{c['ECTS']}</td><td>{c['Mark']}</td><td><b>{c['Grade']}</b></td></tr>"

        slip_content = f"""
        <div class="result-slip">
            <div class="slip-header">
                <h3 style="margin:0;">BAHIR DAR UNIVERSITY</h3>
                <p style="margin:0; font-size:12px; color: #718096;">Unofficial Semester Result Slip</p>
            </div>
            <table class="slip-table">
                <tr><th>Course</th><th>ECTS</th><th>Mark</th><th>Grade</th></tr>
                {rows_html}
            </table>
            <div style="display: flex; justify-content: space-between; margin-top: 15px; font-size: 14px; font-weight: bold;">
                <div>ECTS: {int(total_ects)}</div>
                <div style="color: #1A365D; font-size: 18px;">GPA: {gpa:.2f}</div>
            </div>
        </div>
        """
        st.markdown(slip_content, unsafe_allow_html=True)
    else:
        st.warning("እባክህ መጀመሪያ ውጤት አስገባ።")

st.markdown(f"<p style='text-align:center; color:#718096; font-size:10px;'>Developer: Belachew Damtie</p>", unsafe_allow_html=True)
