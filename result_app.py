import streamlit as st
import pandas as pd

st.set_page_config(page_title="BDU Result Calculator", layout="wide")

# CSS - ለዋናው ገጽ እና ለ Slip ዲዛይን
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #2C3E50; }
    
    /* የአስላ Button */
    div.stButton > button:first-child {
        background-color: #1A365D !important;
        color: white !important;
        border-radius: 10px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: bold !important;
    }

    /* ለ Screen Shot የሚመቸው Slip ዲዛይን */
    .result-slip {
        background-color: white;
        padding: 30px;
        border: 2px solid #1A365D;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #1A365D;
        margin-top: 20px;
        font-family: 'Arial', sans-serif;
    }
    .slip-header {
        text-align: center;
        border-bottom: 2px solid #1A365D;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .slip-footer {
        text-align: center;
        margin-top: 30px;
        font-size: 12px;
        color: #718096;
        border-top: 1px solid #E2E8F0;
        padding-top: 10px;
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
course_list = []

# የግብዓት ርዕሶች
h1, h2, h3, h4, h5 = st.columns([3, 1, 1, 1, 1])
h1.markdown("<b>የኮርሱ ስም</b>", unsafe_allow_html=True)
h2.markdown("<b>ECTS</b>", unsafe_allow_html=True)
h3.markdown("<b>ውጤት (100)</b>", unsafe_allow_html=True)
h4.markdown("<b>Grade</b>", unsafe_allow_html=True)
h5.markdown("<b>Points</b>", unsafe_allow_html=True)

for i in range(num_courses):
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
    with col1:
        c_name = st.text_input(f"C_{i}", key=f"n_{i}", label_visibility="collapsed", placeholder=f"ኮርስ {i+1}")
    with col2:
        ects = st.number_input(f"E_{i}", min_value=1.0, value=5.0, key=f"e_{i}", label_visibility="collapsed")
    with col3:
        mark = st.number_input(f"M_{i}", min_value=0.0, max_value=100.0, value=0.0, key=f"m_{i}", label_visibility="collapsed")
    
    ng, letter = get_grade_info(mark)
    gp = ects * ng
    
    with col4: st.write(f"**{letter}**" if mark > 0 else "-")
    with col5: st.write(f"**{gp:.2f}**" if mark > 0 else "-")
    
    if mark > 0:
        course_list.append({"Course": c_name if c_name else f"Course {i+1}", "ECTS": ects, "Mark": mark, "Grade": letter, "GP": gp})

st.markdown("<br>", unsafe_allow_html=True)

if st.button("ውጤቴን አስላ"):
    if course_list:
        df_res = pd.DataFrame(course_list)
        total_ects = df_res["ECTS"].sum()
        total_gp = df_res["GP"].sum()
        gpa = total_gp / total_ects
        
        st.balloons()
        
        # --- እዚህ ጋር ነው ለ Screen Shot የሚመቸው Slip የሚጀምረው ---
        st.markdown(f"""
            <div class="result-slip">
                <div class="slip-header">
                    <h2 style="margin:0;">BAHIR DAR UNIVERSITY</h2>
                    <p style="margin:0; color: #718096;">Unofficial Student Semester Result Slip</p>
                </div>
                
                <table style="width:100%; border-collapse: collapse; margin-bottom: 20px;">
                    <tr style="border-bottom: 2px solid #f0f2f6; text-align: left;">
                        <th style="padding: 10px;">Course Title</th>
                        <th style="padding: 10px;">ECTS</th>
                        <th style="padding: 10px;">Mark</th>
                        <th style="padding: 10px;">Grade</th>
                    </tr>
                    {''.join([f'<tr style="border-bottom: 1px solid #f0f2f6;">'
                              f'<td style="padding: 10px;">{row["Course"]}</td>'
                              f'<td style="padding: 10px;">{row["ECTS"]}</td>'
                              f'<td style="padding: 10px;">{row["Mark"]}</td>'
                              f'<td style="padding: 10px;"><b>{row["Grade"]}</b></td>'
                              f'</tr>' for _, row in df_res.iterrows()])}
                </table>
                
                <div style="display: flex; justify-content: space-between; background: #f8f9fa; padding: 15px; border-radius: 10px;">
                    <div><b>Total ECTS:</b> {int(total_ects)}</div>
                    <div><b>Total Grade Point:</b> {total_gp:.2f}</div>
                    <div style="color: #1A365D; font-size: 20px;"><b>GPA: {gpa:.2f}</b></div>
                </div>
                
                <div class="slip-footer">
                    Generated on 2026 | Developer: <b>Belachew Damtie</b><br>
                    <i>Note: This is an unofficial result slip for personal use.</i>
                </div>
            </div>
            <p style="text-align: center; color: #718096; font-size: 13px; margin-top: 10px;">
                👆 ከላይ ያለውን ምስል Screen Shot በማድረግ መያዝ ትችላለህ።
            </p>
        """, unsafe_allow_html=True)
    else:
        st.warning("እባክህ መጀመሪያ ውጤት አስገባ።")

st.markdown(f"<p style='text-align:center; color:#718096; padding-top:20px;'>Developer: Belachew Damtie</p>", unsafe_allow_html=True)
