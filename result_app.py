import streamlit as st
import pandas as pd

# ገጹን ይበልጥ ማራኪ ለማድረግ CSS እንጠቀማለን
st.set_page_config(page_title="BDU Result Calculator", layout="wide")

# Custom CSS for a better UI (ጥቁር ዳራ እና ማራኪ ቀለሞች)
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #004b91;
        color: white;
        font-weight: bold;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    footer {
        visibility: hidden;
    }
    .developer-credit {
        text-align: center;
        padding: 20px;
        font-size: 14px;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)

# የኢትዮጵያ ዩኒቨርሲቲዎች የውጤት መለኪያ Logic
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

# የርዕስ ክፍል
st.title("🎓 BDU Result Calculator")
st.info("ተማሪ ሆይ፦ እዚህ ጋር ከመቶ ያመጣኸውን ውጤት እና የኮርሱን ECTS ብቻ አስገባ።")

# የኮርሶች ዝርዝር (10 ኮርሶች)
num_courses = 10
course_list = []

# የሰንጠረዥ ርዕሶች
h1, h2, h3, h4, h5 = st.columns([3, 1, 1, 1, 1])
h1.markdown("**የኮርሱ ስም**")
h2.markdown("**ECTS**")
h3.markdown("**ውጤት (0-100)**")
h4.markdown("**Letter Grade**")
h5.markdown("**Grade Point**")

# የ 10 ኮርሶች መጻፊያ ክፍሎች
for i in range(num_courses):
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
    with col1:
        c_name = st.text_input(f"ኮርስ {i+1}", key=f"name_{i}", label_visibility="collapsed", placeholder=f"የኮርስ {i+1} ስም")
    with col2:
        ects = st.number_input(f"ECTS_{i}", min_value=1.0, value=5.0, key=f"ects_{i}", label_visibility="collapsed")
    with col3:
        mark = st.number_input(f"Mark_{i}", min_value=0.0, max_value=100.0, value=0.0, key=f"mark_{i}", label_visibility="collapsed")
    
    # በራሱ ስሌቱን እንዲሰራ
    ng, letter = get_grade_info(mark)
    gp = ects * ng
    
    with col4:
        st.write(f"**{letter}**" if mark > 0 else "-")
    with col5:
        st.write(f"**{gp:.2f}**" if mark > 0 else "-")
        
    if mark > 0:
        course_list.append({"ECTS": ects, "Mark": mark, "NG": ng, "GP": gp})

st.markdown("---")

# ጠቅላላ ስሌት
if st.button("ውጤቴን አስላ"):
    if course_list:
        df = pd.DataFrame(course_list)
        
        total_ects = df["ECTS"].sum()
        total_gp = df["GP"].sum()
        gpa = total_gp / total_ects
        
        # ማጠቃለያ በካርዶች
        m1, m2, m3 = st.columns(3)
        m1.metric("ጠቅላላ ECTS", f"{int(total_ects)}")
        m2.metric("ጠቅላላ Grade Point", f"{total_gp:.2f}")
        m3.metric("GPA (ANG)", f"{gpa:.2f}")
        
        # የውጤት ደረጃ (Remark)
        if gpa >= 2.0:
            st.balloons()
            st.success(f"ደረጃህ 'Pass' ነው። (GPA: {gpa:.2f}) ✅")
        else:
            st.error(f"ደረጃህ 'Warning' ላይ ነው። (GPA: {gpa:.2f}) ⚠️")
    else:
        st.warning("እባክህ መጀመሪያ ቢያንስ የአንድ ኮርስ ውጤት (Mark) አስገባ።")

# የDeveloper ስም መጨረሻ ላይ
st.markdown("<br><hr><p class='developer-credit'>Developed by: <b>Belachew Damtie</b></p>", unsafe_allow_html=True)
