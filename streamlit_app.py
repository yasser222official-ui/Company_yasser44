import streamlit as st
import pandas as pd
import datetime

# --- 1. إعدادات المتصفح الأساسية ---
st.set_page_config(
    page_title="نظام النخاع العصبي | الدخول الآمن",
    page_icon="🍏",
    layout="wide"
)

# --- 2. واجهة Apple الحديثة (CSS) ---
# تم استخدام unsafe_allow_html=True لتجنب أي تعليق في النظام
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label {
        font-family: 'Rubik', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    /* تصميم صندوق الدخول */
    .login-container {
        background-color: #F2F2F7;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        text-align: center;
    }

    /* أزرار Apple الحديثة */
    .stButton>button {
        border-radius: 15px;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
        background-color: #34C759;
        color: white;
        border: none;
        transition: 0.4s;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #28a745;
        transform: scale(1.02);
    }

    /* كروت البيانات */
    .metric-card {
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
    }
    .green-card { background-color: #34C759; box-shadow: 0 4px 15px rgba(52, 199, 89, 0.2); }
    .red-card { background-color: #FF3B30; box-shadow: 0 4px 15px rgba(255, 59, 48, 0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. منطق نظام الباسورد (Security Logic) ---
def check_password():
    """يرجع True إذا كانت كلمة المرور صحيحة."""
    
    def password_entered():
        # هنا يمكنك تغيير الباسورد (مثلاً: Yasser2026)
        if st.session_state["pwd_input"] == "1234": 
            st.session_state["password_correct"] = True
            del st.session_state["pwd_input"] # مسح الباسورد من الذاكرة المؤقتة للأمان
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # شاشة الدخول الأولى
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1.5,1])
        with col2:
            st.markdown("""
                <div class='login-container'>
                    <h1 style='font-size: 50px;'>🍏</h1>
                    <h2>نظام النخاع العصبي</h2>
                    <p style='color: #8E8E93;'>أدخل كلمة مرور الإدارة للمتابعة</p>
                </div>
            """, unsafe_allow_html=True)
            st.text_input("كلمة المرور", type="password", on_change=password_entered, key="pwd_input")
            st.button("فتح النظام")
        return False
        
    elif not st.session_state["password_correct"]:
        # في حالة الخطأ
        col1, col2, col3 = st.columns([1,1.5,1])
        with col2:
            st.error("❌ كلمة المرور غير صحيحة. يرجى المحاولة مرة أخرى.")
            st.text_input("كلمة المرور", type="password", on_change=password_entered, key="pwd_input")
            st.button("إعادة المحاولة")
        return False
    else:
        return True

# --- 4. محتوى التطبيق بعد الدخول ---
if check_password():
    
    # القائمة الجانبية
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'></h1>", unsafe_allow_html=True)
        st.title("مركز التحكم")
        st.divider()
        menu = st.radio("القائمة الرئيسية", ["لوحة المؤشرات 📊", "غرفة العمليات ⚠️"])
        st.divider()
        if st.button("تسجيل الخروج"):
            st.session_state.password_correct = False
            del st.session_state["password_correct"]
            st.rerun()

    if menu == "لوحة المؤشرات 📊":
        st.header("نظرة عامة على أداء الشركة")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="metric-card green-card"><h3>المبيعات</h3><h1>150,000 ج.م</h1><p>الحالة: ممتازة ✅</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-card red-card"><h3>المصاريف</h3><h1>45,000 ج.م</h1><p>الحالة: تجاوز الحد ⚠️</p></div>', unsafe_allow_html=True)
            
    elif menu == "غرفة العمليات ⚠️":
        st.header("⚠️ سجل المشكلات والحلول")
        issues = pd.DataFrame([
            {"الوقت": "09:00", "المشكلة": "انقطاع GPS سيارة 1", "الحل المقترح": "تنبيه السائق"},
            {"الوقت": "11:30", "المشكلة": "تجاوز ميزانية فرع أ", "الحل المقترح": "مراجعة المدير"}
        ])
        st.table(issues)
