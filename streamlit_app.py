import streamlit as st
import pandas as pd
import datetime

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="غرفة العمليات | إدارة المشكلات", page_icon="🍏", layout="wide")

# --- 2. التصميم (CSS) ودعم خط Rubik ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label, table {
        font-family: 'Rubik', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: bold;
        transition: 0.3s;
    }
    /* لون زر الحل */
    div.stButton > button:first-child {
        background-color: #34C759;
        color: white;
        border: none;
    }
    .main-title { color: #1C1C1E; text-align: center; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام الأمان ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 class='main-title'>🍏 نظام الإدارة الآمن</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        pwd = st.text_input("أدخل كلمة المرور", type="password")
        if st.button("دخول"):
            if pwd == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("كلمة المرور خاطئة")
    st.stop()

# --- 4. إدارة البيانات (سجل المشكلات) ---
if 'issues_data' not in st.session_state:
    # بيانات افتراضية عند التشغيل لأول مرة
    st.session_state.issues_data = [
        {"الوقت والتاريخ": "2026-04-15 08:00", "المشكلة": "بدء التشغيل اليومي", "الحالة": "تم الحل"},
        {"الوقت والتاريخ": "2026-04-15 10:30", "المشكلة": "تجاوز مصروفات فرع أ", "الحالة": "قيد المعالجة"}
    ]

# --- 5. واجهة المستخدم الرئيسية ---
st.markdown("<h1 style='text-align: center;'>⚠️ غرفة العمليات - إدارة المشكلات</h1>", unsafe_allow_html=True)

# إضافة مشكلة جديدة
with st.expander("➕ إضافة مشكلة جديدة للنظام"):
    with st.form("add_form", clear_on_submit=True):
        new_issue_desc = st.text_input("وصف المشكلة")
        submit = st.form_submit_button("تسجيل المشكلة")
        if submit and new_issue_desc:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.issues_data.append({
                "الوقت والتاريخ": now,
                "المشكلة": new_issue_desc,
                "الحالة": "قيد المعالجة"
            })
            st.rerun()

st.divider()

# عرض المشكلات في جدول تفاعلي
st.subheader("📋 سجل البلاغات الحالي")

# إنشاء أعمدة لعرض البيانات بشكل احترافي
cols = st.columns([2, 3, 1.5, 1])
cols[0].write("**الوقت والتاريخ**")
cols[1].write("**المشكلة**")
cols[2].write("**الحالة**")
cols[3].write("**الإجراء**")

for i, item in enumerate(st.session_state.issues_data):
    c1, c2, c3, c4 = st.columns([2, 3, 1.5, 1])
    c1.write(item["الوقت والتاريخ"])
    c2.write(item["المشكلة"])
    
    # تلوين الحالة
    status_color = "#34C759" if item["الحالة"] == "تم الحل" else "#FF3B30"
    c3.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{item["الحالة"]}</span>", unsafe_allow_html=True)
    
    # زر الحل
    if item["الحالة"] != "تم الحل":
        if c4.button("حل ✅", key=f"btn_{i}"):
            st.session_state.issues_data[i]["الحالة"] = "تم الحل"
            st.rerun()
    else:
        c4.write("✔️")

# --- 6. تصدير البيانات ---
st.sidebar.markdown("---")
df = pd.DataFrame(st.session_state.issues_data)
csv = df.to_csv(index=False).encode('utf-8-sig')
st.sidebar.download_button("📥 تحميل التقرير للمدير", data=csv, file_name="issues_report.csv", mime="text/csv")

if st.sidebar.button("تسجيل الخروج"):
    st.session_state.authenticated = False
    st.rerun()
