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
        margin-bottom: 2rem;
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
        تم تصميم وتطوير هذا التطبيق التفاعلي خصيصاً كأداة بيداغوجية موجهة إلى <b>طلبة وأساتذة السنة الثانية علوم اقتصادية</b> بجامعة محمد البشير الإبراهيمي، بهدف ترسيخ المفاهيم النظرية وتطبيقها عملياً عبر الحاسوب.
    </p>
    <p style="margin-bottom: 0; color: #334155;">
        يتيح التطبيق دراسة التدفق الدائري للنشاط الاقتصادي وحساب الناتج الداخلي الخام (PIB) عبر <b>الطرق العلمية الثلاث المتطابقة (طريقة الإنتاج، طريقة الإنفاق، وطريقة الدخل)</b>، فضلاً عن تتبع التدرج المحاسبي الكامل حتى الوصول إلى الدخل المتاح وتكوين الادخار الوطني الكلي، مع توفير مؤشرات بيانية واختبارات للتوازن التلقائي.
    </p>
</div>
""", unsafe_allow_html=True)

# 3. الشريط الجانبي للمدخلات الاقتصادية (Sidebar)
with st.sidebar:
    st.header("⚙️ مدخلات التدفقات الاقتصادية")
    preset = st.radio("اختر وضع البيانات:", ["بيانات نموذجية متوازنة", "تعديل حر للمتغيرات"])

    # قيم افتراضية متناسقة حسابياً
    w_val, r_val, int_val, prop_val = 650.0, 120.0, 80.0, 150.0
    div_val, pnd_val, tapr_val = 200.0, 60.0, 70.0
    am_val, imp_i_val, sub_exp_val = 150.0, 110.0, 50.0

    st.subheader("1. أنشطة وعوائد طريقة الدخل")
    wages = st.number_input("أجور وتعويضات العمال (W)", value=w_val, step=20.0)
    rents = st.number_input("الريع وإيجارات العقارات (R)", value=r_val, step=10.0)
    interests = st.number_input("صافي الفوائد والأرباح المالية (Int)", value=int_val, step=10.0)
    prop_inc = st.number_input("دخول أصحاب المهن والمشروعات الفردية", value=prop_val, step=10.0)
    dividends = st.number_input("أرباح الأسهم الموزعة على الأفراد (Div)", value=div_val, step=10.0)
    pnd = st.number_input("الأرباح المحتجزة / غير الموزعة (PND)", value=pnd_val, step=10.0)
    ta_pr = st.number_input("الضرائب على أرباح الشركات (TA_pr)", value=tapr_val, step=10.0)

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

    st.subheader("4. الضرائب والتحويلات والاهتلاك")
    am = st.number_input("اهتلاك الأصول الرأسمالية (Am)", value=am_val, step=10.0)
    imp_i = st.number_input("الضرائب غير المباشرة (Imp I)", value=imp_i_val, step=10.0)
    sub_exp = st.number_input("إعانات الاستغلال (Sub d'Exp)", value=sub_exp_val, step=5.0)
    rnfe = st.number_input("صافي عوائد عناصر الإنتاج الخارجية (RNFE)", value=40.0, step=10.0)
    cs = st.number_input("الاشتراكات الاجتماعية (CS)", value=80.0, step=5.0)
    tr = st.number_input("التحويلات الحكومية الاجتماعية (TR)", value=90.0, step=10.0)
    ta_y = st.number_input("الضرائب المباشرة على دخل العائلات (TA_Y)", value=100.0, step=10.0)

# ==================== العمليات الحسابية الاقتصادية ====================
# أ. طريقة الإنفاق
net_exports = x - m
pib_exp = c + i + g + net_exports

# ب. طريقة الإنتاج
vab = vpt - ci
pib_prod = vab + tva + dd - sub_imp

# ج. طريقة الدخل (وفق ما ورد في وثائق المحاضرات)
total_corp_profits = dividends + pnd + ta_pr # إجمالي أرباح الشركات
pib_cf = wages + rents + interests + prop_inc + total_corp_profits # تكلفة عوامل الإنتاج
# الانتقال إلى سعر السوق: إضافة صافي الضرائب غير المباشرة + الاهتلاك
pib_income = pib_cf + (imp_i - sub_exp) + am

# المؤشرات المشتقة (السلسلة التراكمية)
pib_pm = pib_exp # اتخاذ ناتج الإنفاق كمعيار ارتكاز
pnb_pm = pib_pm + rnfe
pnn_pm = pnb_pm - am
rn = pnn_pm - imp_i + sub_exp
rp = rn - pnd - ta_pr - cs + tr
yd = rp - ta_y
sm = yd - c
se = pnd + am
total_tax = ta_y + ta_pr + imp_i + tva + dd
sap = total_tax - (g + tr)
st_total = sm + se + sap

# توازن الحقن والتسرب
leakages = sm + (total_tax - tr) + m
injections = i + g + x

# ==================== علامات التبويب الرئيسية ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "⚖️ طرق قياس الناتج الثلاث (المطابقة والتحليل)",
    "📈 لوحة المؤشرات الكلية (Dashboard)",
    "🔄 شجرة التدفق التراكمي للمؤشرات",
    "📖 الدليل العلمي والمفاهيمي المفصل"
])

# ----------------- التبويب 1: طرق قياس الناتج الثلاث -----------------
with tab1:
    st.subheader("مقارنة ومطابقة طرق قياس الناتج الداخلي الخام (PIB) الثلاث")
    st.markdown("""
    يقاس النشاط الاقتصادي من ثلاث زوايا تعبر جميعها عن وجهين لعملة واحدة: **ما يُنتج يُولد دخلاً، والدخل المتولد يُنفق بالكامل على شراء الإنتاج**.
    """)
    
    col_prod, col_exp, col_inc = st.columns(3)
    
    with col_prod:
        st.markdown("""
        <div class="kpi-card" style="border-top: 4px solid #3B82F6;">
            <h4 style="color: #3B82F6; margin-top:0;">1. طريقة الإنتاج (VAB)</h4>
            <p style="font-size: 0.85rem; color: #64748B;">تقيس الثروة المضافة الحقيقية وتتفادى الازدواج الحسابي.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"- قيمة الإنتاج الكلي (VPT): **{vpt:,.1f}**")
        st.write(f"- ناقص الاستهلاك الوسيط (-CI): **{ci:,.1f}**")
        st.write(f"- = القيمة المضافة (VAB): **{vab:,.1f}**")
        st.write(f"- زائد الرسوم (+TVA): **{tva:,.1f}**")
        st.write(f"- زائد الحقوق الجمركية (+DD): **{dd:,.1f}**")
        st.write(f"- ناقص إعانات الاستيراد (-Sub): **{sub_imp:,.1f}**")
        st.markdown("---")
        st.success(f"**الناتج بطريقة الإنتاج: {pib_prod:,.1f}**")
        
    with col_exp:
        st.markdown("""
        <div class="kpi-card" style="border-top: 4px solid #10B981;">
            <h4 style="color: #10B981; margin-top:0;">2. طريقة الإنفاق النهائي</h4>
            <p style="font-size: 0.85rem; color: #64748B;">تقيس مجموع الطلب الكلي النهائي على السلع والخدمات.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"- الاستهلاك العائلي (C): **{c:,.1f}**")
        st.write(f"- الاستثمار الإجمالي (I): **{i:,.1f}**")
        st.write(f"- الإنفاق الحكومي (G): **{g:,.1f}**")
        st.write(f"- الصادرات (X): **{x:,.1f}**")
        st.write(f"- ناقص الواردات (-M): **{m:,.1f}**")
        st.write(f"- صافي الصادرات (X - M): **{net_exports:,.1f}**")
        st.markdown("---")
        st.success(f"**الناتج بطريقة الإنفاق: {pib_exp:,.1f}**")
        
    with col_inc:
        st.markdown("""
        <div class="kpi-card" style="border-top: 4px solid #D97706;">
            <h4 style="color: #D97706; margin-top:0;">3. طريقة الدخل (عوائد العوامل)</h4>
            <p style="font-size: 0.85rem; color: #64748B;">تقيس مجموع العوائد المدفوعة لمالكي عناصر الإنتاج.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"- الأجور والمرتبات (W): **{wages:,.1f}**")
        st.write(f"- الريع والإيجارات (R): **{rents:,.1f}**")
        st.write(f"- صافي الفوائد (Int): **{interests:,.1f}**")
        st.write(f"- دخول المشروعات الفردية: **{prop_inc:,.1f}**")
        st.write(f"- أرباح الشركات الكلية: **{total_corp_profits:,.1f}**")
        st.caption("*(أرباح موزعة + محتجزة PND + ضرائب شركات)*")
        st.write(f"- الناتج بتكلفة العوامل: **{pib_cf:,.1f}**")
        st.write(f"- + الضرائب غير المباشرة الصافية: **{(imp_i - sub_exp):,.1f}**")
        st.write(f"- + اهتلاك الأصول الرأسمالية (+Am): **{am:,.1f}**")
        st.markdown("---")
        st.success(f"**الناتج بطريقة الدخل: {pib_income:,.1f}**")

    st.markdown("---")
    # رسم بياني تفاعلي لمقارنة الطرق الثلاث
    fig_comp = go.Figure(data=[
        go.Bar(
            name='طرق قياس PIB',
            x=['طريقة الإنتاج (VAB)', 'طريقة الإنفاق النهائي', 'طريقة الدخل وعوامل الإنتاج'],
            y=[pib_prod, pib_exp, pib_income],
            marker_color=['#3B82F6', '#10B981', '#D97706'],
            text=[f"{pib_prod:,.1f}", f"{pib_exp:,.1f}", f"{pib_income:,.1f}"],
            textposition='auto',
        )
    ])
    fig_comp.update_layout(
        title="تطابق النتائج عبر المناهج التحليلية الثلاث لقياس PIB",
        font=dict(family="Cairo"),
        yaxis_title="القيمة النقدية بملايين الوحدات",
        height=380
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# ----------------- التبويب 2: لوحة المؤشرات -----------------
with tab2:
    st.subheader("المؤشرات الاقتصادية السيادية الكبرى")
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
        <small style="color: #D97706;">بتكلفة عوامل الإنتاج</small>
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
        st.write("##### 📊 توزيع عوائد الدخل على عوامل الإنتاج")
        inc_dist = pd.DataFrame({
            "عنصر الإنتاج": ["الأجور والرواتب", "الريع والإيجارات", "صافي الفوائد", "دخول المهن الفردية", "أرباح الشركات الكلية"],
            "القيمة": [wages, rents, interests, prop_inc, total_corp_profits]
        })
        fig_inc = px.pie(inc_dist, values='القيمة', names='عنصر الإنتاج', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Bold)
        fig_inc.update_layout(font=dict(family="Cairo"), margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_inc, use_container_width=True)

    with c_g2:
        st.write("##### 🏦 مصادر تكوين الادخار الوطني الإجمالي (ST)")
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
        {"المرحلة / المؤشر": "6. الدخل الوطني (RN)", "المعادلة والبيان": "PNN_pm - Imp_I + Sub_Exp", "القيمة المحسوبة": f"{rn:,.1f}"},
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
    
    with st.expander("📌 طريقة الدخل وعوائد عناصر الإنتاج"):
        st.markdown("""
        - **طبيعة الطريقة:** تجمع دخول الأفراد والمؤسسات الناتجة عن تقديم خدمات عوامل الإنتاج المساهمة في العملية الإنتاجية خلال سنة.
        - **المكونات الأساسية:**
          1. **الأجور والمرتبات:** عوائد عنصر العمل وتشمل المكافآت والبدلات.
          2. **الريع والإيجارات:** عوائد الأراضي والمباني والموارد الطبيعية المؤجرة.
          3. **صافي الفوائد:** الفوائد التي تحصل عليها العائلات من قطاع الأعمال بعد استبعاد الفوائد المدفوعة.
          4. **دخول أصحاب المهن والمشروعات الفردية:** أرباح الأعمال غير المسجلة كشركات مساهمة.
          5. **أرباح الشركات المساهمة:** وتُقسم إلى: ضرائب أرباح الشركات ($TA_{p/r}$)، أرباح موزعة على المساهمين ($Dividends$)، وأرباح غير موزعة/محتجزة ($PND$).
        - **التحويل إلى سعر السوق:** ناتج تكلفة العوامل يعبر عما يدفعه المنتجون مباشرة، ولكي يتساوى مع سعر السوق في المتاجر، يضاف إليه صافي الضرائب غير المباشرة ($Imp\ I - Sub\ d'Exp$) واهتلاك الأصول الرأسمالية ($Am$).
        """)
        
    with st.expander("📌 طريقة القيمة المضافة (الإنتاج) وتفادي الازدواج"):
        st.markdown("""
        - تستبعد الاستهلاك الوسيط ($CI$) لضمان عدم احتساب قيمة السلع الوسيطة (مثل القمح، الدقيق في الخبز) أكثر من مرة.
        - الصيغة: $VAB = VPT - CI$.
        """)

    with st.expander("📌 طريقة الإنفاق النهائي ومكونات الطلب الكلي"):
        st.markdown("""
        - تقيس مشتريات القطاعات الأربعة: العائلات ($C$)، قطاع الأعمال والشركات ($I$)، الحكومة ($G$)، والعالم الخارجي ($X - M$).
        - الصيغة: $PIB = C + I + G + (X - M)$.
        """)

# تذييل الصفحة
st.markdown("---")
st.markdown(
    "<center><small style='color: #64748B;'>جامعة محمد البشير الإبراهيمي - برج بوعريريج | كلية العلوم الاقتصادية والتجارية وعلوم التسيير | إعداد: الأستاذ لعايب وليد</small></center>", 
    unsafe_allow_html=True
)
