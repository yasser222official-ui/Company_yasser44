import streamlit as st
import pandas as pd
import datetime

# --- 1. إعدادات المتصفح ---
st.set_page_config(
    page_title="متابعة شركة الكينج",
    page_icon="",
    layout="wide"
)

# --- 2. التصميم (CSS) ودعم خط Rubik ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label {
        font-family: 'Rubik', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .login-box {
        background-color: #F2F2F7;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #D1D1D6;
        text-align: center;
    }
    .stButton>button {
        border-radius: 12px;
        height: 3em;
        width: 100%;
        background-color: #34C759;
        color: white;
        font-weight: bold;
        border: none;
    }
    .metric-card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 10px;
    }
    .green-bg { background-color: #34C759; }
    .red-bg { background-color: #FF3B30; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام الأمان (Login Logic) - نسخة محسنة لمنع KeyError ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    # شاشة الدخول
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown('<div class="login-box"><h1>🍏</h1><h3>نظام الدخول الآمن</h3></div>', unsafe_allow_html=True)
        # استخدام البرنامج بدون callback لمنع KeyError
        password_input = st.text_input("أدخل كلمة المرور", type="password")
        if st.button("تسجيل الدخول"):
            if password_input == "1234": # كلمة السر
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ كلمة المرور غير صحيحة")
    return False

# --- 4. محتوى التطبيق بعد النجاح ---
if check_password():
    # القائمة الجانبية
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'></h1>", unsafe_allow_html=True)
        st.title("لوحة القيادة")
        menu = st.radio("نتقل إلى:", ["الرئيسية", "غرفة العمليات ⚠️", "تصدير 📥"])
        st.divider()
        if st.button("خروج"):
            st.session_state.authenticated = False
            st.rerun()

    # قسم الرئيسية
    if menu == "الرئيسية 🏠":
        st.header("إحصائيات الشركة")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="metric-card green-bg"><h3>المبيعات</h3><h2>150,000 ج.م</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-card red-bg"><h3>المصاريف</h3><h2>45,000 ج.م</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="metric-card green-bg"><h3>الكفاءة</h3><h2>98%</h2></div>', unsafe_allow_html=True)
            
        st.divider()
        st.subheader("حالة النظم")
        st.table(pd.DataFrame({"النظام": ["ERP", "GPS", "AI"], "الحالة": ["✅", "✅", "⚠️"]}))

    # قسم غرفة العمليات
    elif menu == "غرفة العمليات ⚠️":
        st.header("⚠️ سجل المشكلات اللحظي")
        if 'logs' not in st.session_state:
            st.session_state.logs = [{"الوقت": "08:00", "المشكلة": "بدء التشغيل", "الحالة": "مستقر"}]
        
        st.table(pd.DataFrame(st.session_state.logs))
        
        with st.form("add_log"):
            txt = st.text_input("إضافة بلاغ جديد")
            if st.form_submit_button("إرسال"):
                st.session_state.logs.append({"الوقت": datetime.datetime.now().strftime("%H:%M"), "المشكلة": txt, "الحالة": "قيد المعالجة"})
                st.rerun()

    # قسم التصدير
    elif menu == "تصدير 📥":
        st.header("تصدير التقارير")
        df = pd.DataFrame(st.session_state.get('logs', []))
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل التقرير (CSV)", data=csv, file_name="report.csv")
