import streamlit as st
import pandas as pd

# ገጹን በሰፊው እና በ Blue-Black ዲዛይን ማዋቀር
st.set_page_config(page_title="BDU Result Calculator", layout="wide")

# Custom CSS for Blue-Black Theme
st.markdown("""
    <style>
    /* ጠቆር ያለ ሰማያዊ ዳራ */
    .stApp {
        background-color: #010B13;
        color: #E0E6ED;
    }
    
    /* Input ሳጥኖች */
    div[data-baseweb="input"] > div {
        background-color: #0A1929 !important;
        color: #FFFFFF !important;
        border: 1px solid #1E3A5F !important;
        border-radius: 8px !important;
    }

    /* የጽሁፍ ሳጥኖች ውስጥ ያለ ጽሁፍ */
    div[data-baseweb="input"] input {
        color: #FFFFFF !important;
    }

    /* አስላ የሚለውን ቁልፍ ዲዛይን (Electric Blue) */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #0078D4;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.4s;
    }
    
    .stButton>button:hover {
        background-color: #005A9E;
        box-shadow: 0 0 15px rgba(0, 120, 212, 0.6);
        border: 1px solid #00BCF2;
    }

    /* ውጤት ማሳያ ካርዶች (Deep Navy) */
    div[data-testid="stMetric"] {
        background-color: #0A1929;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #1E3A5F;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }

    /* የሜትሪክ ጽሁፍ ቀለሞች */
    div[data-testid="stMetricValue"] {
        color: #00BCF2 !important;
    }

    /* የዲቨሎፐር ክሬዲት */
    .developer-credit {
        text-align: center;
        padding-top: 50px;
        font-size: 15px;
        color: #5C7080;
        letter-spacing: 1px;
    }
    
    h1 {
        color: #00BCF2;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# የውጤት መለኪያ Logic
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

# ርዕስ
st.title("🎓 BDU Result Calculator")
st.write("<p style='text-align: center; color: #5C7080;'>የኮርሱን ECTS እና ውጤት በማስገባት የሴሚስተር GPAዎን ያሰሉ</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ርዕሶች
h1, h2, h3, h4, h5 = st.columns([3, 1, 1, 1, 1])
h1.markdown("<p style='color: #00BCF2;'><b>የኮርሱ ስም</b></p>", unsafe_allow_html=True)
h2.markdown("<p style='color: #00BCF2;'><b>ECTS</b></p>", unsafe_allow_html=True)
h3.markdown("<p style='color: #00BCF2;'><b>ውጤት (100)</b></p>", unsafe_allow_html=True)
h4.markdown("<p style='color: #00BCF2;'><b>Grade</b></p>", unsafe_allow_html=True)
h5.markdown("<p style='color: #00BCF2;'><b>Points</b></p>", unsafe_allow_html=True)

num_courses = 10
course_list = []

for i in range(num_courses):
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
    with col1:
        c_name = st.text_input(f"ኮርስ {i+1}", key=f"name_{i}", label_visibility="collapsed", placeholder=f"ኮርስ {i+1}")
    with col2:
        ects = st.number_input(f"ECTS_{i}", min_value=1.0, value=5.0, key=f"ects_{i}", label_visibility="collapsed")
    with col3:
        mark = st.number_input(f"Mark_{i}", min_value=0.0, max_value=100.0, value=0.0, key=f"mark_{i}", label_visibility="collapsed")
    
    ng, letter = get_grade_info(mark)
    gp = ects * ng
    
    with col4:
        st.write(f"<p style='padding-top: 10px; color: #00BCF2;'><b>{letter}</b></p>" if mark > 0 else "-", unsafe_allow_html=True)
    with col5:
        st.write(f"<p style='padding-top: 10px; color: #FFFFFF;'><b>{gp:.2f}</b></p>" if mark > 0 else "-", unsafe_allow_html=True)
        
    if mark > 0:
        course_list.append({"ECTS": ects, "Mark": mark, "NG": ng, "GP": gp})

st.markdown("<br>", unsafe_allow_html=True)

if st.button("ውጤቴን አስላ"):
    if course_list:
        df = pd.DataFrame(course_list)
        total_ects = df["ECTS"].sum()
        total_gp = df["GP"].sum()
        gpa = total_gp / total_ects
        
        st.markdown("---")
        m1, m2, m3 = st.columns(3)
        m1.metric("ጠቅላላ ECTS", f"{int(total_ects)}")
        m2.metric("ጠቅላላ GP", f"{total_gp:.2f}")
        m3.metric("GPA (ANG)", f"{gpa:.2f}")
        
        if gpa >= 2.0:
            st.balloons()
            st.success(f"ደረጃህ 'Pass' ነው። GPA: {gpa:.2f} ✅")
        else:
            st.error(f"ደረጃህ 'Warning' ላይ ነው። GPA: {gpa:.2f} ⚠️")
    else:
        st.warning("እባክህ መጀመሪያ ውጤት አስገባ።")

st.markdown(f"<p class='developer-credit'>Developed by: <b>Belachew Damtie</b></p>", unsafe_allow_html=True)
