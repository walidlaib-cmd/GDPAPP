import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# إعداد الصفحة وتفضيلات العرض
st.set_page_config(
    page_title="منصة قياس النشاط الاقتصادي | جامعة برج بوعريريج",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص واجهة المستخدم لدعم اللغة العربية وتنسيق RTL
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .academic-header {
        background: linear-gradient(135deg, #1B365D 0%, #0F2342 100%);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(27, 54, 93, 0.15);
        margin-bottom: 1.5rem;
        border-right: 6px solid #D97706;
    }
    
    .intro-card {
        background-color: #F1F5F9;
        border-radius: 12px;
        padding: 1.3rem 1.8rem;
        border: 1px solid #CBD5E1;
        margin-bottom: 1.8rem;
        line-height: 1.8;
    }

    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1B365D;
    }
    
    .metric-title {
        font-size: 0.95rem;
        color: #64748B;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 1. الترويسة الأكاديمية الرسمية
st.markdown("""
<div class="academic-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h3 style="margin: 0; font-weight: 800; color: #FCD34D;">جامعة محمد البشير الإبراهيمي - برج بوعريريج</h3>
            <h4 style="margin: 4px 0; font-weight: 600; color: #E2E8F0;">كلية العلوم الاقتصادية والتجارية وعلوم التسيير</h4>
            <div style="margin-top: 10px; display: flex; gap: 15px; flex-wrap: wrap;">
                <span style="background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">📚 السنة الثانية: اقتصاد كلي</span>
                <span style="background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">👨‍🏫 الأستاذ: لعايب وليد</span>
                <span style="background: #D97706; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">🗓️ السنة الجامعية: 2026/2027</span>
            </div>
        </div>
        <div style="text-align: left; margin-top: 10px;">
            <span style="font-size: 2.5rem;">📊</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. بطاقة المقدمة الترحيبية الشاملة
st.markdown("""
<div class="intro-card">
    <h4 style="color: #1B365D; margin-top: 0; font-weight: 700;">🌟 مرحباً بكم في منصة المحاكاة والتحليل الكلي لقياس النشاط الاقتصادي</h4>
    <p style="margin-bottom: 0.5rem; color: #334155;">
        تم تطوير هذه الأداة البيداغوجية التفاعلية لخدمة <b>طلبة وأساتذة السنة الثانية علوم اقتصادية</b>، لتجسيد متطابقات المحاسبة القومية ومراقبة مؤشرات النشاط الاقتصادي عملياً.
    </p>
    <p style="margin-bottom: 0; color: #334155;">
        تتيح المنصة التحقق الآلي من <b>التطابق النظري والمحاسبي لطرق قياس الناتج الثلاث (الإنتاج، الإنفاق، والدخل)</b>، سواء عند سعر السوق أو بسعر تكلفة عوامل الإنتاج، مع استعراض مسار التحول التدريجي من الإنتاج الكلي وصولاً إلى الدخل المتاح وتكوين الادخار الإجمالي.
    </p>
</div>
""", unsafe_allow_html=True)

# 3. الشريط الجانبي للمدخلات الاقتصادية (Sidebar)
with st.sidebar:
    st.header("⚙️ مدخلات التدفقات الاقتصادية")
    
    # قيم افتراضية متطابقة حسابياً 100% عبر الطرق الثلاث
    st.subheader("1. أنشطة وعوائد طريقة الدخل (عوامل الإنتاج)")
    wages = st.number_input("أجور وتعويضات العمال (W)", value=650.0, step=20.0)
    rents = st.number_input("الريع وإيجارات العقارات (R)", value=150.0, step=10.0)
    interests = st.number_input("صافي الفوائد النقدية (Int)", value=110.0, step=10.0)
    prop_inc = st.number_input("دخول المشروعات الفردية والمهن", value=220.0, step=10.0)
    dividends = st.number_input("أرباح الأسهم الموزعة (Div)", value=200.0, step=10.0)
    pnd = st.number_input("الأرباح غير الموزعة / المحتجزة (PND)", value=60.0, step=10.0)
    ta_pr = st.number_input("الضرائب على أرباح الشركات (TA_pr)", value=70.0, step=10.0)

    st.subheader("2. بنود طريقة الإنفاق النهائي")
    c = st.number_input("الاستهلاك العائلي النهائي (C)", value=1100.0, step=50.0)
    i = st.number_input("الاستثمار الإجمالي (I)", value=400.0, step=20.0)
    g = st.number_input("الإنفاق الحكومي العام (G)", value=320.0, step=20.0)
    x = st.number_input("الصادرات (X)", value=250.0, step=20.0)
    m = st.number_input("الواردات (M)", value=400.0, step=20.0)

    st.subheader("3. طريقة الإنتاج والقيمة المضافة")
    vpt = st.number_input("قيمة الإنتاج الكلي (VPT)", value=2500.0, step=50.0)
    ci = st.number_input("الاستهلاك الوسيط (CI)", value=1000.0, step=50.0)
    tva = st.number_input("الرسوم على القيمة المضافة (TVA)", value=120.0, step=10.0)
    dd = st.number_input("الحقوق والرسوم الجمركية (DD)", value=80.0, step=10.0)
    sub_imp = st.number_input("إعانات الاستيراد (Sub d'Imp)", value=30.0, step=5.0)

    st.subheader("4. بنود التسوية المحاسبية والتحويلات")
    am = st.number_input("اهتلاك الأصول الرأسمالية (Am)", value=150.0, step=10.0)
    imp_i = st.number_input("الضرائب غير المباشرة (Imp I)", value=110.0, step=10.0)
    sub_exp = st.number_input("إعانات الاستغلال (Sub d'Exp)", value=50.0, step=5.0)
    rnfe = st.number_input("صافي عوائد عوامل الإنتاج الخارجية (RNFE)", value=40.0, step=10.0)
    cs = st.number_input("الاشتراكات الاجتماعية (CS)", value=80.0, step=5.0)
    tr = st.number_input("التحويلات الحكومية الاجتماعية (TR)", value=90.0, step=10.0)
    ta_y = st.number_input("الضرائب المباشرة على دخل العائلات (TA_Y)", value=100.0, step=10.0)

# ==================== الحسابات الاقتصادية ====================
# صافي الضرائب غير المباشرة = الضرائب غير المباشرة - إعانات الاستغلال
net_indirect_taxes = imp_i - sub_exp

# 1. طريقة الإنفاق
net_exports = x - m
pib_exp_pm = c + i + g + net_exports
# الصافي بتكلفة العوامل بطريقة الإنفاق
pin_cf_exp = pib_exp_pm - am - net_indirect_taxes

# 2. طريقة الإنتاج
vab = vpt - ci
pib_prod_pm = vab + tva + dd - sub_imp
# الصافي بتكلفة العوامل بطريقة الإنتاج
pin_cf_prod = pib_prod_pm - am - net_indirect_taxes

# 3. طريقة الدخل
total_corp_profits = dividends + pnd + ta_pr  # إجمالي أرباح الشركات
# مجموع عوائد عناصر الإنتاج يمثل مباشرة الناتج الداخلي الصافي بتكلفة عوامل الإنتاج
pin_cf_income = wages + rents + interests + prop_inc + total_corp_profits
# الانتقال إلى سعر السوق بطريقة الدخل
pib_income_pm = pin_cf_income + am + net_indirect_taxes

# المؤشرات المشتقة المتبقية
pib_pm = pib_exp_pm
pnb_pm = pib_pm + rnfe
pnn_pm = pnb_pm - am
rn = pnn_pm - imp_i + sub_exp  # الدخل الوطني = الناتج القومي الصافي بتكلفة العوامل
rp = rn - pnd - ta_pr - cs + tr
yd = rp - ta_y
sm = yd - c
se = pnd + am
total_tax = ta_y + ta_pr + imp_i + tva + dd
sap = total_tax - (g + tr)
st_total = sm + se + sap

# ==================== علامات التبويب ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "⚖️ طرق قياس الناتج ومطابقة التكلفة الصافية",
    "📈 لوحة المؤشرات الكلية (Dashboard)",
    "🔄 شجرة التدفق التراكمي للمؤشرات",
    "📖 الدليل العلمي والمفاهيمي المفصل"
])

# ----------------- التبويب 1: مقارنة الطرق الثلاث -----------------
with tab1:
    st.subheader("1. مطابقة الناتج المحلي الإجمالي بسعر السوق (PIB pm)")
    col_prod, col_exp, col_inc = st.columns(3)
    
    with col_prod:
        st.markdown("""
        <div class="kpi-card" style="border-top: 4px solid #3B82F6;">
            <h4 style="color: #3B82F6; margin-top:0;">طريقة الإنتاج (VAB)</h4>
            <small style="color: #64748B;">الثروة المضافة المستخرجة</small>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"- قيمة الإنتاج الكلي (VPT): **{vpt:,.1f}**")
        st.write(f"- ناقص الاستهلاك الوسيط (-CI): **{ci:,.1f}**")
        st.write(f"- = القيمة المضافة الإجمالية (VAB): **{vab:,.1f}**")
        st.write(f"- + صافي الرسوم (TVA+DD-Sub): **{(tva + dd - sub_imp):,.1f}**")
        st.markdown("---")
        st.success(f"**PIB بسعر السوق: {pib_prod_pm:,.1f}**")

    with col_exp:
        st.markdown("""
        <div class="kpi-card" style="border-top: 4px solid #10B981;">
            <h4 style="color: #10B981; margin-top:0;">طريقة الإنفاق النهائي</h4>
            <small style="color: #64748B;">مجموع الطلب الكلي</small>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"- الاستهلاك العائلي (C): **{c:,.1f}**")
        st.write(f"- الاستثمار الإجمالي (I): **{i:,.1f}**")
        st.write(f"- الإنفاق العام الحكومي (G): **{g:,.1f}**")
        st.write(f"- صافي الصادرات (X - M): **{net_exports:,.1f}**")
        st.markdown("---")
        st.success(f"**PIB بسعر السوق: {pib_exp_pm:,.1f}**")

    with col_inc:
        st.markdown("""
        <div class="kpi-card" style="border-top: 4px solid #D97706;">
            <h4 style="color: #D97706; margin-top:0;">طريقة الدخل (العوامل)</h4>
            <small style="color: #64748B;">عوائد عناصر الإنتاج</small>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"- مجموع عوائد العوامل (PIN cf): **{pin_cf_income:,.1f}**")
        st.write(f"- + اهتلاك الأصول الرأسمالية (+Am): **{am:,.1f}**")
        st.write(f"- + صافي الضرائب غير المباشرة: **{net_indirect_taxes:,.1f}**")
        st.caption("*(الضرائب غير المباشرة Imp I - إعانات الاستغلال Sub Exp)*")
        st.markdown("---")
        st.success(f"**PIB بسعر السوق: {pib_income_pm:,.1f}**")

    st.markdown("---")
    
    # التحقق الحاسم والمحاسبي الذي أشرت إليه: التساوي بسعر التكلفة الصافي
    st.subheader("2. التطابق النظري والمحاسبي للناتج الصافي بسعر التكلفة (PIN cf)")
    st.markdown("""
    تقتضي النظرية الاقتصادية أن يتساوى **الناتج الداخلي الصافي بسعر تكلفة عوامل الإنتاج ($PIN_{cf}$)** بدقة تامة بين الطرق الثلاث:
    $$\\text{PIN}_{cf} = \\text{PIB}_{pm} - Am - (Imp\\ I - Sub\\ Exp) = \\sum \\text{عوائد عوامل الإنتاج}$$
    """)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("طريقة الإنتاج (PIN cf)", f"{pin_cf_prod:,.1f}")
    m2.metric("طريقة الإنفاق (PIN cf)", f"{pin_cf_exp:,.1f}")
    m3.metric("طريقة الدخل (PIN cf)", f"{pin_cf_income:,.1f}")
    
    # فحص التطابق التلقائي
    diff = max(abs(pin_cf_prod - pin_cf_income), abs(pin_cf_exp - pin_cf_income))
    if diff < 0.001:
        st.success("🎯 **تحقق التطابق الكامل (100%):** الناتج الصافي بسعر التكلفة متساوٍ تماماً عبر الطرق الثلاث دون أي فارق إحصائي!")
    else:
        st.warning(f"⚠️ **تنبيه وجود فارق إحصائي ({diff:,.1f}):** يرجع هذا الفارق في الممارسة العملية إلى اختلاف مصادر جمع البيانات الإحصائية بين الضرائب ومسوح الإنفاق والمصانع.")

    st.markdown("---")
    # رسم بياني لمطابقة الطرق الثلاث
    fig_comp = go.Figure(data=[
        go.Bar(
            name='الناتج بسعر السوق (PIB pm)',
            x=['طريقة الإنتاج', 'طريقة الإنفاق', 'طريقة الدخل'],
            y=[pib_prod_pm, pib_exp_pm, pib_income_pm],
            marker_color='#1E3A8A',
            text=[f"{pib_prod_pm:,.1f}", f"{pib_exp_pm:,.1f}", f"{pib_income_pm:,.1f}"],
            textposition='auto'
        ),
        go.Bar(
            name='الناتج الصافي بسعر التكلفة (PIN cf)',
            x=['طريقة الإنتاج', 'طريقة الإنفاق', 'طريقة الدخل'],
            y=[pin_cf_prod, pin_cf_exp, pin_cf_income],
            marker_color='#D97706',
            text=[f"{pin_cf_prod:,.1f}", f"{pin_cf_exp:,.1f}", f"{pin_cf_income:,.1f}"],
            textposition='auto'
        )
    ])
    fig_comp.update_layout(
        barmode='group',
        title="مقارنة متوازية: الناتج بسعر السوق مقابل الناتج الصافي بسعر التكلفة عبر الطرق الثلاث",
        font=dict(family="Cairo"),
        height=390
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# ----------------- التبويب 2: لوحة المؤشرات الكبرى -----------------
with tab2:
    st.subheader("المؤشرات الاقتصادية الكلية الكبرى")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.markdown(f"""
    <div class="kpi-card">
        <div class="metric-title">الناتج الداخلي بسعر السوق (PIB)</div>
        <div class="metric-value">{pib_pm:,.1f}</div>
        <small style="color: #059669;">سعر السوق المعياري</small>
    </div>
    """, unsafe_allow_html=True)
    
    col2.markdown(f"""
    <div class="kpi-card">
        <div class="metric-title">الناتج القومي الخام (PNB)</div>
        <div class="metric-value">{pnb_pm:,.1f}</div>
        <small style="color: #2563EB;">PIB + RNFE ({rnfe:+,.0f})</small>
    </div>
    """, unsafe_allow_html=True)
    
    col3.markdown(f"""
    <div class="kpi-card">
        <div class="metric-title">الدخل الوطني الصافي (RN)</div>
        <div class="metric-value">{rn:,.1f}</div>
        <small style="color: #D97706;">PNN بتكلفة عوامل الإنتاج</small>
    </div>
    """, unsafe_allow_html=True)
    
    col4.markdown(f"""
    <div class="kpi-card">
        <div class="metric-title">الدخل التصرفي المتاح (Yd)</div>
        <div class="metric-value">{yd:,.1f}</div>
        <small style="color: #7C3AED;">الدخل القابل للتصرف العائلي</small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    c_g1, c_g2 = st.columns(2)
    with c_g1:
        st.write("##### 📊 توزيع عوائد الدخل الصافي على عوامل الإنتاج")
        inc_dist = pd.DataFrame({
            "عنصر الإنتاج": ["الأجور والرواتب", "الريع والإيجارات", "صافي الفوائد", "دخول المهن الفردية", "أرباح الشركات الكلية"],
            "القيمة": [wages, rents, interests, prop_inc, total_corp_profits]
        })
        fig_inc = px.pie(inc_dist, values='القيمة', names='عنصر الإنتاج', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Bold)
        fig_inc.update_layout(font=dict(family="Cairo"), margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_inc, use_container_width=True)

    with c_g2:
        st.write("##### 🏦 مصادر الادخار الوطني الكلي (ST)")
        sav_df = pd.DataFrame({
            "القطاع المدخر": ["القطاع العائلي (SM)", "قطاع المؤسسات (SE)", "القطاع الحكومي (SAP)"],
            "القيمة": [sm, se, sap]
        })
        fig_sav = px.bar(sav_df, x='القطاع المدخر', y='القيمة', color='القطاع المدخر',
                         text_auto='.1f', color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B'])
        fig_sav.update_layout(font=dict(family="Cairo"), showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_sav, use_container_width=True)

# ----------------- التبويب 3: شجرة التدفق التراكمي -----------------
with tab3:
    st.subheader("التسلسل الانتقالي التراكمي للمؤشرات (من الإنتاج إلى الادخار الكلي)")
    st.caption("وفقاً للمخطط المحاسبي الدقيق الوارد في ملخص مقياس الاقتصاد الكلي.")
    
    flow_df = pd.DataFrame([
        {"المرحلة / المؤشر": "1. قيمة الإنتاج الكلي (VPT)", "المعادلة والبيان": "VPT", "القيمة المحسوبة": f"{vpt:,.1f}"},
        {"المرحلة / المؤشر": "2. القيمة المضافة الإجمالية (VAB)", "المعادلة والبيان": "VPT - CI", "القيمة المحسوبة": f"{vab:,.1f}"},
        {"المرحلة / المؤشر": "3. الناتج الداخلي الخام بسعر السوق (PIB_pm)", "المعادلة والبيان": "VAB + TVA + DD - Sub_Imp", "القيمة المحسوبة": f"{pib_pm:,.1f}"},
        {"المرحلة / المؤشر": "4. الناتج الوطني الخام بسعر السوق (PNB_pm)", "المعادلة والبيان": "PIB + RNFE", "القيمة المحسوبة": f"{pnb_pm:,.1f}"},
        {"المرحلة / المؤشر": "5. الناتج الوطني الصافي بسعر السوق (PNN_pm)", "المعادلة والبيان": "PNB - Am", "القيمة المحسوبة": f"{pnn_pm:,.1f}"},
        {"المرحلة / المؤشر": "6. الدخل الوطني (RN = PNN_pp)", "المعادلة والبيان": "PNN_pm - Imp_I + Sub_Exp", "القيمة المحسوبة": f"{rn:,.1f}"},
        {"المرحلة / المؤشر": "7. الدخل الشخصي (RP)", "المعادلة والبيان": "RN - PND - TA_pr - CS + TR", "القيمة المحسوبة": f"{rp:,.1f}"},
        {"المرحلة / المؤشر": "8. الدخل التصرفي المتاح (Yd)", "المعادلة والبيان": "RP - TA_Y", "القيمة المحسوبة": f"{yd:,.1f}"},
        {"المرحلة / المؤشر": "9. الادخار العائلي (SM)", "المعادلة والبيان": "Yd - C", "القيمة المحسوبة": f"{sm:,.1f}"},
        {"المرحلة / المؤشر": "10. ادخار المؤسسات (SE)", "المعادلة والبيان": "PND + Am", "القيمة المحسوبة": f"{se:,.1f}"},
        {"المرحلة / المؤشر": "11. الادخار الحكومي (SAP)", "المعادلة والبيان": "TA - (G + TR)", "القيمة المحسوبة": f"{sap:,.1f}"},
        {"المرحلة / المؤشر": "12. الادخار الكلي الوطني (ST)", "المعادلة والبيان": "SM + SE + SAP", "القيمة المحسوبة": f"{st_total:,.1f}"}
    ])
    st.table(flow_df)

# ----------------- التبويب 4: الدليل العلمي والمفاهيمي -----------------
with tab4:
    st.subheader("المعجم الاقتصادي التفاعلي لمؤشرات النشاط الكلي")
    
    with st.expander("📌 لماذا يتطابق الناتج الصافي بسعر التكلفة عبر الطرق الثلاث؟"):
        st.markdown("""
        - **طريقة الدخل:** تبدأ مباشرة من عوائد عوامل الإنتاج (أجور، أرباح، ريوع، فوائد)، وبالتالي نتيجتها المباشرة هي **الناتج الداخلي الصافي بسعر التكلفة ($PIN_{cf}$)**.
        - **طريقتا الإنتاج والإنفاق:** تقومان بحساب الناتج بسعر السوق في المتاجر ($PIB_{pm}$)، وللوصول إلى التكلفة الصافية نقوم بـ:
          1. طرح اهتلاك رأس المال ($Am$) للوصول إلى الصافي ($PIN$).
          2. طرح الضرائب غير المباشرة الصافية ($Imp\\ I - Sub\\ Exp$) لأنها تذهب لخزينة الدولة ولا تدخل في تكلفة العوامل المدفوعة للمنتجين.
        - **النتيجة:** تتطابق الطرق الثلاث في تقدير الثروة الصافية الحقيقية التي ولدها الاقتصاد خلال الفترة.
        """)
        
    with st.expander("📌 الفرق بين سعر السوق (Prix du Marché) وسعر التكلفة (Coût des Facteurs)"):
        st.markdown("""
        - **سعر السوق ($pm$):** هو السعر الفعلي الذي يدفعه المستهلك عند الشراء، متضمناً الضرائب غير المباشرة (مثل الرسم على القيمة المضافة $TVA$) ومستبعداً منه إعانات الدولة للأسعار.
        - **سعر التكلفة ($cf$ أو $pp$):** هو ما يستلمه المنتج وأصحاب عوامل الإنتاج نظير خدماتهم الإنتاجية دون احتساب الجباية غير المباشرة.
        """)

# تذييل الصفحة
st.markdown("---")
st.markdown(
    "<center><small style='color: #64748B;'>جامعة محمد البشير الإبراهيمي - برج بوعريريج | كلية العلوم الاقتصادية والتجارية وعلوم التسيير | إعداد: الأستاذ لعايب وليد</small></center>", 
    unsafe_allow_html=True
)
