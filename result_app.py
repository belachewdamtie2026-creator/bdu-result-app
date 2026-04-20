import streamlit as st
import pandas as pd

# ገጹን በሰፊው እና በጠቆር ያለ ዲዛይን ማዋቀር
st.set_page_config(page_title="BDU Result Calculator", layout="wide")

# Custom CSS for Dark Mode Interface
st.markdown("""
    <style>
    /* ሙሉ ዳራውን ጠቆር ያለ ማድረግ */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* የኮርስ መጻፊያ ሳጥኖችን ቀለም መቀየር */
    div[data-baseweb="input"] > div {
        background-color: #1A1C24 !important;
        color: white !important;
        border: 1px solid #30363D !important;
    }

    /* የቁጥር መጻፊያ ሳጥኖች */
    div[data-baseweb="input"] input {
        color: white !important;
    }

    /* አስላ የሚለውን ቁልፍ ዲዛይን */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #FF2B2B;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
    }

    /* ውጤት ማሳያ ካርዶች */
    div[data-testid="stMetric"] {
        background-color: #1A1C24;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363D;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    /* የዲቨሎፐር ክሬዲት */
    .developer-credit {
        text-align: center;
        padding-top: 50px;
        font-size: 16px;
        color: #8B949E;
        font-family: 'Courier New', Courier, monospace;
    }
    
    h1 {
        color: #FF4B4B;
        text-align: center;
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
st.write("<p style='text-align: center; color: #8B949E;'>ውጤትህን ለማስላት የኮርሱን ECTS እና ከመቶ ያመጣኸውን ውጤት አስገባ</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# የኮርሶች ዝርዝር
num_courses = 10
course_list = []

# ርዕሶች
h1, h2, h3, h4, h5 = st.columns([3, 1, 1, 1, 1])
h1.markdown("<p style='color: #FF4B4B;'><b>የኮርሱ ስም</b></p>", unsafe_allow_html=True)
h2.markdown("<p style='color: #FF4B4B;'><b>ECTS</b></p>", unsafe_allow_html=True)
h3.markdown("<p style='color: #FF4B4B;'><b>ውጤት (100)</b></p>", unsafe_allow_html=True)
h4.markdown("<p style='color: #FF4B4B;'><b>Grade</b></p>", unsafe_allow_html=True)
h5.markdown("<p style='color: #FF4B4B;'><b>Points</b></p>", unsafe_allow_html=True)

for i in range(num_courses):
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
    with col1:
        c_name = st.text_input(f"ኮርስ {i+1}", key=f"name_{i}", label_visibility="collapsed", placeholder=f"የኮርስ {i+1} ስም")
    with col2:
        ects = st.number_input(f"ECTS_{i}", min_value=1.0, value=5.0, key=f"ects_{i}", label_visibility="collapsed")
    with col3:
        mark = st.number_input(f"Mark_{i}", min_value=0.0, max_value=100.0, value=0.0, key=f"mark_{i}", label_visibility="collapsed")
    
    ng, letter = get_grade_info(mark)
    gp = ects * ng
    
    with col4:
        st.write(f"<p style='padding-top: 10px;'><b>{letter}</b></p>" if mark > 0 else "-", unsafe_allow_html=True)
    with col5:
        st.write(f"<p style='padding-top: 10px;'><b>{gp:.2f}</b></p>" if mark > 0 else "-", unsafe_allow_html=True)
        
    if mark > 0:
        course_list.append({"ECTS": ects, "Mark": mark, "NG": ng, "GP": gp})

st.markdown("<br>", unsafe_allow_html=True)

# ጠቅላላ ስሌት
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

# የDeveloper ስም
st.markdown(f"<p class='developer-credit'>Developed by: <b>Belachew Damtie</b></p>", unsafe_allow_html=True)
