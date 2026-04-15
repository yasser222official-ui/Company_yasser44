import streamlit as st
import pandas as pd
import datetime

# --- 1. إعدادات المتصفح ---
st.set_page_config(
    page_title="نظام النخاع العصبي | إدارة الشركة",
    page_icon="🍏",
    layout="wide"
)

# --- 2. التصميم الاحترافي (Apple Style) ودعم خط Rubik ---
# ملاحظة: تم تصحيح الخطأ هنا باستخدام unsafe_allow_html
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap" rel="stylesheet">
    <style>
    /* تطبيق الخط العربي والاتجاه */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label {
        font-family: 'Rubik', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    /* أزرار Apple الحديثة */
    .stButton>button {
        border-radius: 12px;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
        background-color: #34C759;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #28a745;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* كروت البيانات (أخضر وأحمر) */
    .metric-card {
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
    }
    .green-card { background-color: #34C759; box-shadow: 0 4px 15px rgba(52, 199, 89, 0.2); }
    .red-card { background-color: #FF3B30; box-shadow: 0 4px 15px rgba(255, 59, 48, 0.2); }
    
    /* تحسين شكل القائمة الجانبية */
    .css-1d391kg { background-color: #F2F2F7; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام الأمان (Login System) ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center;'>🍏 دخول النظام الآمن</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            password = st.text_input("كلمة المرور", type="password")
            if st.button("تسجيل الدخول"):
                if password == "Admin2026": # يمكنك تعديل كلمة السر هنا
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ كلمة المرور خاطئة")
        return False
    return True

# --- 4. تشغيل واجهة التطبيق الرئيسية ---
if check_password():
    
    # القائمة الجانبية (Sidebar)
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'></h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>لوحة القيادة</h3>", unsafe_allow_html=True)
        st.divider()
        choice = st.radio("القائمة", ["الرئيسية 🏠", "غرفة العمليات ⚠️", "تصدير البيانات 📥"])
        st.divider()
        if st.button("خروج"):
            st.session_state.authenticated = False
            st.rerun()

    # قسم الرئيسية
    if choice == "الرئيسية 🏠":
        st.header("نظرة عامة على الشركة")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card green-card"><h3>المبيعات</h3><h1>150,000 ج.م</h1><p>أداء مستقر</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card red-card"><h3>المصاريف</h3><h1>45,000 ج.م</h1><p>⚠️ تجاوز حد الأمان</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card green-card"><h3>كفاءة الـ GPS</h3><h1>98%</h1><p>تغطية كاملة</p></div>', unsafe_allow_html=True)

        st.divider()
        st.subheader("حالة الأنظمة الحية")
        status_data = pd.DataFrame({
            "النظام": ["ERP", "تتبع السيارات", "المراقبة", "الرقم الموحد"],
            "الحالة": ["✅ فعال", "✅ فعال", "❌ عطل", "✅ فعال"]
        })
        st.table(status_data)

    # قسم غرفة العمليات
    elif choice == "غرفة العمليات ⚠️":
        st.header("⚠️ مركز إدارة الأزمات")
        st.warning("يتم رصد المشاكل بناءً على الحساسات الذكية (Thresholds)")
        
        if 'issues' not in st.session_state:
            st.session_state.issues = [
                {"الوقت": "10:00 AM", "النوع": "مالي", "المشكلة": "تجاوز مصروفات المكتب", "الحل": "مراجعة المدير"},
                {"الوقت": "11:30 AM", "النوع": "تقني", "المشكلة": "انقطاع كاميرا المنطقة 2", "الحل": "إعادة تشغيل"}
            ]
        
        st.table(pd.DataFrame(st.session_state.issues))
        
        with st.form("add_issue"):
            st.write("إضافة بلاغ يدوي")
            desc = st.text_input("وصف المشكلة")
            if st.form_submit_button("إرسال"):
                st.session_state.issues.append({"الوقت": "الآن", "النوع": "يدوي", "المشكلة": desc, "الحل": "جاري التحقق"})
                st.rerun()

    # قسم التصدير
    elif choice == "تصدير البيانات 📥":
        st.header("إخراج التقارير")
        df = pd.DataFrame(st.session_state.get('issues', []))
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل سجل الأخطاء للمدير (Excel)", data=csv, file_name="report.csv", mime="text/csv")
