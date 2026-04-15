import streamlit as st
import pandas as pd
import datetime

# --- 1. إعدادات الصفحة والتنسيق ---
st.set_page_config(page_title="النظام الذكي | ربط العمليات", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label {
        font-family: 'Rubik', sans-serif !important; direction: rtl; text-align: right;
    }
    .status-card { padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; text-align: center; }
    .green-card { background-color: #34C759; }
    .red-card { background-color: #FF3B30; }
    .suggestion-box { background-color: #F2F2F7; padding: 15px; border-radius: 12px; border-right: 5px solid #007AFF; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك اكتشاف الأخطاء والربط (The Logic Engine) ---
def analyze_business_health(sales, marketing_spend, target_reached):
    issues = []
    
    # ربط المبيعات بالتسويق (مثال استهداف ناس غلط)
    if marketing_spend > 5000 and sales < 1000:
        issues.append({
            "المشكلة": "انحراف حملة التسويق",
            "السبب": "ميزانية التسويق عالية والمبيعات منخفضة (استهداف جمهور غير مناسب)",
            "الحل المقترح": "إيقاف الإعلان الحالي فوراً وإعادة ضبط الفئة المستهدفة لتناسب المنتج."
        })
    
    # ربط المبيعات بالتشغيل
    if sales == 0:
        issues.append({
            "المشكلة": "توقف تدفق المبيعات",
            "السبب": "عطل في نظام الدفع أو بوابة الـ ERP",
            "الحل المقترح": "فحص اتصال API بين المتجر ونظام المحاسبة."
        })
        
    return issues

# --- 3. نظام الأمان ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🍏 دخول النظام الذكي")
        pwd = st.text_input("باسورد", type="password")
        if st.button("دخول"):
            if pwd == "1234": st.session_state.auth = True; st.rerun()
    st.stop()

# --- 4. واجهة التحكم والربط ---
st.sidebar.title(" إدارة الربط")
page = st.sidebar.radio("المنطقة", ["لوحة التحكم حياً", "سجل الأخطاء والحلول"])

# بيانات افتراضية للمحاكاة (كأنها قادمة من البرامج الأخرى)
if 'sales_val' not in st.session_state: st.session_state.sales_val = 500
if 'mkt_val' not in st.session_state: st.session_state.mkt_val = 6000

if page == "لوحة التحكم حياً":
    st.header("📊 الربط بين الأقسام (Live Sync)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.sales_val = st.number_input("قيمة المبيعات الحالية (من الـ ERP)", value=st.session_state.sales_val)
    with col2:
        st.session_state.mkt_val = st.number_input("صرف التسويق (من Facebook/Google Ads)", value=st.session_state.mkt_val)
    
    st.divider()
    
    # تشغيل المحرك الذكي
    found_issues = analyze_business_health(st.session_state.sales_val, st.session_state.mkt_val, True)
    
    if found_issues:
        st.subheader("🚨 تنبيهات النظام التلقائية")
        for issue in found_issues:
            st.error(f"**{issue['المشكلة']}**")
            st.markdown(f"""
                <div class="suggestion-box">
                    <strong>السبب المكتشف:</strong> {issue['السبب']}<br>
                    <span style='color: #34C759;'><strong>✅ الحل الذكي:</strong> {issue['الحل المقترح']}</span>
                </div><br>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ جميع الأنظمة مرتبطة وتعمل بكفاءة (لا توجد تناقضات في البيانات)")

elif page == "سجل الأخطاء والحلول":
    st.header("📋 أرشيف الأزمات المحلولة")
    # هنا يتم عرض الجداول السابقة التي صممناها
    st.info("هذا القسم يسجل كل "الحلول" التي تم تنفيذها بناءً على اقتراحات النظام.")
