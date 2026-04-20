import streamlit as st
import pandas as pd

st.set_page_config(page_title="BDU Result Calculator", layout="wide")

# CSS - ለስልክ ስክሪን ጎን ለጎን (Horizontal) እንዲሆን ማስገደጃ
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #2C3E50; }
    
    /* በስልክ ላይም ቢሆን ኮለሞችን ጎን ለጎን (Row) ለማድረግ */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        overflow-x: auto !important; /* ጠባብ ስልክ ከሆነ ወደ ጎን እንዲንሸራተት */
    }

    /* እያንዳንዱን ኮለም ጠበብ አድርጎ ጎን ለጎን ለማሳየት */
    [data-testid="column"] {
        min-width: 60px !important;
        flex: 1 1 auto !important;
    }

    /* ኮርስ ስም መጻፊያ ሳጥን ትንሽ ሰፋ እንዲል */
    [data-testid="column"]:nth-of-type(1) {
        min-width: 120px !important;
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
    }
    
    /* በስልክ ላይ ጽሁፎች እንዳይበላሹ መጠናቸውን ማስተካከል */
    @media (max-width: 640px) {
        .stMarkdown p { font-size: 12px !important; }
        input { font-size: 12px !important; }
    }
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

# የርዕስ ክፍሎች - ስልክ ላይ ቦታ እንዲቆጥቡ በአጭሩ
h = st.columns([2.5, 1, 1.2, 0.8, 1])
h[0].write("**ኮርስ**")
h[1].write("**ECTS**")
h[2].write("**ውጤት**")
h[3].write("**Gr**")
h[4].write("**Pt**")

for i in range(num_courses):
    cols = st.columns([2.5, 1, 1.2, 0.8, 1])
    with cols[0]: c_name = st.text_input(f"C{i}", key=f"n_{i}", label_visibility="collapsed", placeholder="ስም")
    with cols[1]: ects = st.number_input(f"E{i}", min_value=1.0, value=5.0, key=f"e_{i}", label_visibility="collapsed")
    with cols[2]: mark = st.number_input(f"M{i}", min_value=0.0, max_value=100.0, value=0.0, key=f"m_{i}", label_visibility="collapsed")
    
    ng, letter = get_grade_info(mark)
    gp = ects * ng
    
    with cols[3]: st.write(f"**{letter}**" if mark > 0 else "-")
    with cols[4]: st.write(f"**{gp:.1f}**" if mark > 0 else "-")
    
    if mark > 0:
        course_data.append({"Course": c_name if c_name else f"Course {i+1}", "ECTS": ects, "Mark": mark, "Grade": letter, "GP": gp})

st.markdown("<br>", unsafe_allow_html=True)

if st.button("ውጤቴን አስላ"):
    if course_data:
        total_ects = sum(c['ECTS'] for c in course_data)
        total_gp = sum(c['GP'] for c in course_data)
        gpa = total_gp / total_ects
        
        st.balloons()
        
        rows_html = "".join([f"<tr><td>{c['Course']}</td><td>{c['ECTS']}</td><td>{c['Mark']}</td><td><b>{c['Grade']}</b></td></tr>" for c in course_data])

        slip_content = f"""
        <div class="result-slip">
            <div style="text-align: center; border-bottom: 2px solid #1A365D; padding-bottom: 10px; margin-bottom: 15px;">
                <h3 style="margin:0;">BAHIR DAR UNIVERSITY</h3>
                <p style="margin:0; font-size:12px; color: #718096;">Unofficial Semester Result Slip</p>
            </div>
            <table style="width:100%; border-collapse: collapse; font-size: 13px;">
                <tr style="border-bottom: 1px solid #1A365D; text-align: left;">
                    <th>Course</th><th>ECTS</th><th>Mark</th><th>Grade</th>
                </tr>
                {rows_html}
            </table>
            <div style="display: flex; justify-content: space-between; margin-top: 15px; font-weight: bold; background: #f8f9fa; padding: 10px; border-radius: 8px;">
                <div>ECTS: {int(total_ects)}</div>
                <div style="color: #1A365D; font-size: 18px;">GPA: {gpa:.2f}</div>
            </div>
            <div style="text-align: center; margin-top: 15px; font-size: 10px; color: #718096; border-top: 1px solid #eee; padding-top: 10px;">
                Developer: <b>Belachew Damtie</b>
            </div>
        </div>
        """
        st.markdown(slip_content, unsafe_allow_html=True)
    else:
        st.warning("እባክህ መጀመሪያ ውጤት አስገባ።")

st.markdown(f"<p style='text-align:center; color:#718096; font-size:10px; margin-top:30px;'>Developer: Belachew Damtie</p>", unsafe_allow_html=True)
