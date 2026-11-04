import streamlit as st
import pandas as pd
import numpy as np

# 1. Cấu hình trang giao diện rộng (Wide layout)
st.set_page_config(
    page_title="Phòng Pha Chế Nước Hoa Bốn Mùa - STEM Lab AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS Tùy biến Cao cấp (Tương thích Light/Dark Mode, Thẻ Card Bo Góc, Hiệu ứng Mềm mại)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Global Cursor Fix: Ép toàn bộ thẻ bấm/chọn dạng bàn tay */
    .stSelectbox, .stRadio, button, [role="button"], [role="option"] {
        cursor: pointer !important;
    }
    input {
        caret-color: auto;
    }

    /* Hero Banner Header */
    .hero-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 18px;
        padding: 26px 30px;
        color: #ffffff;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
        border: 1px solid #334155;
    }
    .hero-title {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(90deg, #f8fafc 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-top: 6px;
    }

    /* Metric Cards */
    .metric-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
    }
    .metric-val {
        font-size: 26px;
        font-weight: 700;
        line-height: 1.2;
    }
    .metric-lbl {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Thẻ An Toàn High-Contrast Fix */
    .safety-card {
        background-color: #fef3c7 !important;
        border: 1px solid #f59e0b !important;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
    .safety-card-title {
        color: #92400e !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        margin-bottom: 6px !important;
    }
    .safety-card-body {
        color: #78350f !important;
        font-size: 13.5px !important;
        line-height: 1.5 !important;
    }

    /* Container hồ sơ hương */
    .profile-card {
        background-color: #f8fafc;
        border: 1px dashed #cbd5e1;
        border-radius: 12px;
        padding: 14px 18px;
        margin: 14px 0;
        color: #334155;
    }

    /* Chat bubble styling */
    .chat-bubble-ai {
        background-color: #f1f5f9;
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# 3. Cơ sở dữ liệu 4 Mùa hoàn chỉnh bám sát Kế hoạch & Bảng tham khảo
seasons_data = {
    "Xuân": {
        "label": "Mùa Xuân — Sớm Mai (Tươi Mới & Sắc Hoa)",
        "slug": "xuan",
        "icon": "🌸",
        "theme_color": "#d53f8c",
        "desc_profile": "Hương đầu tươi sáng của Bergamot FCF & Cam ngọt hòa quyện cùng nét thanh dịu của Oải hương, Phong lữ và nền gỗ Tuyết tùng phảng phất Vanilla.",
        "rules": {
            "Bergamot FCF": {"limit": 4.0, "default": 3.8, "tier": "Hương đầu (Top)", "type": "top"},
            "Sweet orange": {"limit": 3.0, "default": 2.0, "tier": "Hương đầu (Top)", "type": "top"},
            "Lavender":     {"limit": 4.0, "default": 3.5, "tier": "Hương giữa (Heart)", "type": "middle"},
            "Geranium":     {"limit": 3.0, "default": 2.5, "tier": "Hương giữa (Heart)", "type": "middle"},
            "Cedarwood":    {"limit": 2.0, "default": 1.3, "tier": "Hương cuối (Base)", "type": "base"},
            "Vanilla accord":{"limit": 1.0, "default": 0.6, "tier": "Hương cuối (Base)", "type": "base"},
        }
    },
    "Hạ": {
        "label": "Mùa Hạ — Solar Jasmine / Vườn Nhiệt Đới (Năng Động)",
        "slug": "ha",
        "icon": "🌊",
        "theme_color": "#0284c7",
        "desc_profile": "Mát lạnh năng động bùng nổ hương Cam Bưởi, Hoa Mộc Tê hòa quyện nét nồng nàn của Hoa Nhài Nhiệt Đới và nền Dừa Dịu mát.",
        "rules": {
            "Cam/Bưởi/Mộc tê": {"limit": 4.0, "default": 3.5, "tier": "Hương đầu (Top)", "type": "top"},
            "Hoa Nhài (Jasmine)": {"limit": 4.0, "default": 3.0, "tier": "Hương giữa (Heart)", "type": "middle"},
            "Bạc hà / Thảo mộc": {"limit": 1.5, "default": 0.8, "tier": "Hương giữa (Heart)", "type": "middle"},
            "Hương Dừa (Coconut)": {"limit": 2.0, "default": 1.2, "tier": "Hương cuối (Base)", "type": "base"},
            "Cedarwood":         {"limit": 2.0, "default": 1.0, "tier": "Hương cuối (Base)", "type": "base"},
            "Vanilla accord":    {"limit": 1.0, "default": 0.3, "tier": "Hương cuối (Base)", "type": "base"},
        }
    },
    "Thu": {
        "label": "Mùa Thu — Dịu Êm & Sâu Lắng",
        "slug": "thu",
        "icon": "🍁",
        "theme_color": "#d97706",
        "desc_profile": "Cảm giác chuyển mùa ấm áp đằm thắm với Cam ngọt, Oải hương dịu nốt và hợp hương Gỗ Tuyết Tùng đượm vị ngọt Vanilla.",
        "rules": {
            "Sweet orange": {"limit": 3.0, "default": 2.5, "tier": "Hương đầu (Top)", "type": "top"},
            "Bergamot FCF": {"limit": 3.0, "default": 1.8, "tier": "Hương đầu (Top)", "type": "top"},
            "Lavender":     {"limit": 4.0, "default": 3.0, "tier": "Hương giữa (Heart)", "type": "middle"},
            "Geranium":     {"limit": 3.0, "default": 2.5, "tier": "Hương giữa (Heart)", "type": "middle"},
            "Cedarwood":    {"limit": 3.0, "default": 2.2, "tier": "Hương cuối (Base)", "type": "base"},
            "Vanilla accord":{"limit": 1.5, "default": 0.9, "tier": "Hương cuối (Base)", "type": "base"},
        }
    },
    "Đông": {
        "label": "Mùa Đông — Ấm Áp & Sang Trọng",
        "slug": "dong",
        "icon": "❄️",
        "theme_color": "#7c3aed",
        "desc_profile": "Hương cuối đậm sâu sang trọng, lưu hương lâu dài với Tuyết Tùng đượm vị kết hợp Vanilla nồng nàn quyến rũ.",
        "rules": {
            "Bergamot FCF": {"limit": 3.0, "default": 1.8, "tier": "Hương đầu (Top)", "type": "top"},
            "Sweet orange": {"limit": 2.5, "default": 1.5, "tier": "Hương đầu (Top)", "type": "top"},
            "Lavender":     {"limit": 3.5, "default": 2.5, "tier": "Hương giữa (Heart)", "type": "middle"},
            "Geranium":     {"limit": 3.0, "default": 2.0, "tier": "Hương giữa (Heart)", "type": "middle"},
            "Cedarwood":    {"limit": 3.0, "default": 2.5, "tier": "Hương cuối (Base)", "type": "base"},
            "Vanilla accord":{"limit": 2.0, "default": 1.2, "tier": "Hương cuối (Base)", "type": "base"},
        }
    }
}

# 4. THANH BÊN BẢNG ĐIỀU KHIỂN (SIDEBAR)
with st.sidebar:
    st.markdown("### 🎛️ Cấu Hình Mẻ Pha Chế")
    st.markdown("---")
    
    # Chọn Mùa
    selected_season_key = st.radio(
        "🌿 Chọn chủ đề mùa / concept:",
        list(seasons_data.keys()),
        format_func=lambda k: f"{seasons_data[k]['icon']} {k} - {seasons_data[k]['label'].split('—')[1].strip()}"
    )
    season_info = seasons_data[selected_season_key]

    st.markdown("---")
    st.markdown("🧪 **Thể tích mẻ nước hoa (mL)**")
    
    # Preset Thể tích nhanh
    v_col1, v_col2, v_col3, v_col4 = st.columns(4)
    if "vol_state" not in st.session_state:
        st.session_state["vol_state"] = 10.0
        
    with v_col1:
        if st.button("5ml"): st.session_state["vol_state"] = 5.0
    with v_col2:
        if st.button("10ml"): st.session_state["vol_state"] = 10.0
    with v_col3:
        if st.button("15ml"): st.session_state["vol_state"] = 15.0
    with v_col4:
        if st.button("20ml"): st.session_state["vol_state"] = 20.0

    volume = st.number_input(
        "Tùy chỉnh thể tích mẻ (mL):",
        min_value=1.0,
        max_value=20.0,
        value=float(st.session_state["vol_state"]),
        step=0.5,
        help="Giới hạn an toàn mẻ học tập phòng thí nghiệm: 1.0 – 20.0 mL"
    )
    
    st.markdown("---")
    st.markdown("#### 📋 Tiêu Chuẩn An Toàn STEM")
    st.markdown("""
    - **Nồng độ tinh dầu:** ≤ 30.0% Max
    - **Dung môi Ethanol:** Tự động cân bằng
    - **Độ chính xác mL:** 3 chữ số (`0.001 mL`)
    - **Quy chuẩn:** IFRA & Phê duyệt Giáo viên
    """)

# 5. KHU VỰC HERO BANNER CHÍNH
st.markdown(f"""
<div class="hero-container">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <div>
            <h1 class="hero-title">{season_info['icon']} {season_info['label']}</h1>
            <p class="hero-subtitle">Dự án STEM Hóa Học 12 — Thiết Kế Công Thức Hương Thơm Tích Hợp Dữ Liệu & Trí Tuệ Nhân Tạo (AI)</p>
        </div>
        <span style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: #ffffff; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 13px;">
            Mẻ thực hành: {volume:.1f} mL
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. KHỜI TẠO TABS CHỨC NĂNG CHỦ ĐẠO
tab_mix, tab_charts, tab_ai, tab_safety = st.tabs([
    "🧪 1. Pha Chế & Quy Đổi", 
    "📊 2. Biểu Đồ & Dữ Liệu", 
    "🤖 3. Trợ Lý AI Chuyên Sâu", 
    "⚠️ 4. Quy Tắc An Toàn"
])

# ---------------------------------------------------------
# TAB 1: PHÒNG PHA CHẾ & QUY ĐỔI THỜI GIAN THỰC
# ---------------------------------------------------------
with tab_mix:
    col_left, col_right = st.columns([1.15, 1], gap="large")

    rows = []
    errors = []

    with col_left:
        st.subheader("🎚️ Điều chỉnh tỷ lệ phần trăm (%) từng chất")
        st.caption("Kéo thanh trượt để tinh chỉnh. Trần an toàn (Max %) đã được khóa cố định theo phê duyệt của Giáo viên.")

        tier_groups = {
            "Hương đầu (Top Notes) 🍋": [k for k, v in season_info["rules"].items() if v["type"] == "top"],
            "Hương giữa (Heart Notes) 🌸": [k for k, v in season_info["rules"].items() if v["type"] == "middle"],
            "Hương cuối (Base Notes) 🪵": [k for k, v in season_info["rules"].items() if v["type"] == "base"],
        }

        for group_title, items in tier_groups.items():
            with st.expander(f"**{group_title}**", expanded=True):
                for name in items:
                    rule = season_info["rules"][name]
                    limit = rule["limit"]
                    default_val = rule["default"]
                    tier = rule["tier"]

                    c_label, c_slider = st.columns([1, 2])
                    with c_label:
                        st.markdown(f"<div style='padding-top: 8px; font-weight: 600; font-size: 13.5px;'>{name}</div>", unsafe_allow_html=True)
                        st.caption(f"Trần an toàn: {limit:.1f}%")
                    with c_slider:
                        pct = st.slider(
                            f"Tỷ lệ {name}",
                            min_value=0.0,
                            max_value=limit,
                            value=default_val,
                            step=0.1,
                            label_visibility="collapsed"
                        )

                    if pct > limit:
                        errors.append(f"{name} vượt quá trần an toàn ({limit}%)")

                    rows.append({
                        "Thành phần": name,
                        "Tầng hương": tier,
                        "%": pct,
                        "Giới hạn GV (%)": limit,
                        "mL": round(volume * pct / 100, 3)
                    })

    # Tính toán dung môi và tổng tinh dầu
    fragrance_total = sum(r["%"] for r in rows)
    solvent_pct = round(100.0 - fragrance_total, 2)
    solvent_ml = round(volume * solvent_pct / 100, 3)

    if solvent_pct < 0:
        errors.append("Tổng nhóm hương vượt quá 100% (Dung môi Ethanol bị âm)")
    if fragrance_total > 30.0:
        errors.append("Tổng nồng độ tinh dầu vượt quá 30% ngưỡng an toàn mẻ học tập")

    rows.append({
        "Thành phần": "Dung môi (Ethanol thực phẩm)",
        "Tầng hương": "Dung môi",
        "%": solvent_pct,
        "Giới hạn GV (%)": 100.0,
        "mL": solvent_ml
    })

    df = pd.DataFrame(rows)

    with col_right:
        st.subheader("📊 Thống kê mẻ & Bảng quy đổi")
        
        # 3 Thẻ Metric
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: {'#ef4444' if fragrance_total > 30 else '#0d9488'};">{fragrance_total:.1f}%</div>
                <div class="metric-lbl">Tinh dầu</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: {'#ef4444' if solvent_pct < 0 else '#2563eb'};">{solvent_pct:.1f}%</div>
                <div class="metric-lbl">Dung môi</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            status_text = "Hợp lệ" if not errors else "Lỗi"
            status_color = "#16a34a" if not errors else "#dc2626"
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: {status_color}; font-size: 20px; line-height: 38px;">{status_text}</div>
                <div class="metric-lbl">Trạng thái</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        pct_progress = min(max(fragrance_total / 30.0, 0.0), 1.0)
        st.progress(pct_progress, text=f"Nồng độ tinh dầu mẻ: {fragrance_total:.1f}% / 30.0% Max")

        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        
        # Bảng hiển thị
        df_display = df.copy()
        df_display["%"] = df_display["%"].map(lambda x: f"{x:.2f}%")
        df_display["Giới hạn GV (%)"] = df_display["Giới hạn GV (%)"].map(lambda x: f"{x:.1f}%")
        df_display["mL"] = df_display["mL"].map(lambda x: f"{x:.3f} mL")
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Cảnh báo an toàn cố định bắt buộc
        st.caption("⚠️ **Chú ý:** Hợp lệ toán học không đồng nghĩa an toàn. Cần giáo viên duyệt trước khi pha.")

        # Thẻ Hồ sơ Mùi Hương
        st.markdown(f"""
        <div class="profile-card">
            <span style="font-weight: 700;">🌿 Hồ sơ cảm quan:</span> {season_info['desc_profile']}
        </div>
        """, unsafe_allow_html=True)

        # Xuất file CSV
        if not errors:
            st.success(f"✨ **ĐỦ ĐIỀU KIỆN GỬI GIÁO VIÊN DUYỆT:** Mẻ {volume:.1f} mL hợp lệ toán học và giới hạn an toàn.")
            
            export_func = getattr(df, "to_csv")
            csv_bytes = export_func(index=False).encode("utf-8-sig")
            
            dl_button = getattr(st, "download_button")
            dl_button(
                label="📥 Tải Bảng Công Thức Kiểm Duyệt (CSV)",
                data=csv_bytes,
                file_name=f"cong_thuc_{season_info['slug']}_{int(volume)}ml.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            for err in errors:
                st.error(f"⚠️ {err}")

# ---------------------------------------------------------
# TAB 2: BIỂU ĐỒ VÀ TRỰC QUAN HÓA DỮ LIỆU STEM
# ---------------------------------------------------------
with tab_charts:
    st.subheader("📊 Trực Quan Hóa Tỷ Lệ & Thể Tích Thực Tế (mL)")
    st.caption("Biểu đồ tự động cập nhật thời gian thực theo từng thao tác tinh chỉnh của học sinh.")

    c1, c2 = st.columns(2)
    
    df_chart = df[df["Tầng hương"] != "Dung môi"].copy()
    
    with c1:
        st.markdown("##### 💧 Phân bổ Thể tích thực tế (mL) từng chất")
        st.bar_chart(df_chart.set_index("Thành phần")["mL"])
        
    with c2:
        st.markdown("##### 📈 So sánh Tỷ lệ (%) vs Trần An toàn (%)")
        df_comp = df_chart.set_index("Thành phần")[["%", "Giới hạn GV (%)"]]
        st.bar_chart(df_comp)

    st.markdown("---")
    st.markdown("##### 🧩 Tỷ lệ đóng góp của các Nhóm Tầng Hương")
    top_sum = df[df["Tầng hương"] == "Hương đầu (Top)"]["%"].sum()
    mid_sum = df[df["Tầng hương"] == "Hương giữa (Heart)"]["%"].sum()
    base_sum = df[df["Tầng hương"] == "Hương cuối (Base)"]["%"].sum()
    
    df_tiers = pd.DataFrame({
        "Tầng hương": ["Hương đầu (Top)", "Hương giữa (Heart)", "Hương cuối (Base)", "Dung môi Ethanol"],
        "Tỷ lệ (%)": [top_sum, mid_sum, base_sum, solvent_pct]
    })
    st.dataframe(df_tiers, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 3: TRỢ LÝ AI CHUYÊN SÂU (AI PERFUMER & PROMPT GENERATOR)
# ---------------------------------------------------------
with tab_ai:
    st.subheader("🤖 Trợ Lý Trí Tuệ Nhân Tạo (AI STEM Perfumer)")
    st.caption("Tích hợp công cụ phân tích tự động công thức mẻ hiện tại và khung tư vấn AI thời gian thực.")

    ai_sub1, ai_sub2 = st.columns([1, 1.1], gap="large")

    with ai_sub1:
        st.markdown("#### ⚡ 1. Phân Tích Công Thức Mẻ Hiện Tại bằng AI")
        st.markdown("Bấm nút bên dưới để AI đánh giá độ cân bằng 3 tầng hương và gợi ý hướng cải tiến.")
        
        if st.button("🔮 Phân Tích Công Thức Bằng AI", use_container_width=True):
            st.markdown("---")
            st.markdown("##### 📝 Kết Quả Phân Tích AI:")
            
            # Tính toán logic đánh giá
            harmony_score = int(85 + (top_sum * 1.2 if top_sum <= 8 else 5) + (mid_sum * 1.5 if mid_sum <= 8 else 5))
            harmony_score = min(harmony_score, 98)
            
            st.metric("Điểm Cân Bằng Cảm Quan Dự Kiến", f"{harmony_score} / 100")
            
            st.markdown(f"""
            - **Đánh giá Hương đầu ({top_sum:.1f}%):** {'Tươi mát rực rỡ, ấn tượng ban đầu tốt.' if top_sum >= 4 else 'Hơi dịu nhẹ, có thể tăng nhẹ Bergamot/Cam.'}
            - **Đánh giá Hương giữa ({mid_sum:.1f}%):** {'Hoa cỏ thảo mộc tỏa nét tròn đặn.' if mid_sum >= 4 else 'Tầng giữa hơi mỏng, nên giữ vững nốt Oải hương.'}
            - **Đánh giá Hương cuối ({base_sum:.1f}%):** {'Lưu hương đằm sâu với Tuyết Tùng và Vanilla.' if base_sum >= 1.5 else 'Hương nền vừa đủ, đảm bảo tính thanh thoát.'}
            - **Khuyến nghị AI:** Công thức mẻ **{season_info['label'].split('—')[0]}** đạt tỷ lệ hài hòa. Đã sẵn sàng cho thực hành pha mẻ thử nghiệm!
            """)

        st.markdown("---")
        st.markdown("#### 📋 2. Trình Tạo Prompt AI Cho File Audit `07_Nhat_ky_prompt_AI.pdf`")
        st.caption("Sao chép đoạn lệnh đã được tối ưu hóa dữ liệu bên dưới để gửi cho AI (ChatGPT/Claude) phục vụ báo cáo:")
        
        prompt_text = f"""Bạn là chuyên gia Hóa học & Nước hoa STEM. Hãy phân tích công thức nước hoa {season_info['label']} mẻ {volume} mL với các tỷ lệ sau:
{chr(10).join([f"- {r['Thành phần']}: {r['%']}% (Thành thể tích: {r['mL']} mL)" for r in rows if r['Tầng hương'] != 'Dung môi'])}
- Dung môi Ethanol bù: {solvent_pct}% ({solvent_ml} mL)
- Tổng nồng độ tinh dầu: {fragrance_total:.1f}%

Yêu cầu:
1. Đánh giá sự hài hòa giữa 3 tầng hương (Top, Heart, Base).
2. Kiểm tra các ràng buộc an toàn (Không vượt trần % quy định, không dùng trên da).
3. Đề xuất 2 phương án tối ưu v2 (chỉ chỉnh ±0.5% mỗi chất, giữ tổng 100%).
4. Trả lời ngắn gọn, khoa học để nhóm lưu vào Nhật ký Prompt AI."""

        st.code(prompt_text, language="markdown")

    with ai_sub2:
        st.markdown("#### 💬 3. Khung Hỏi Đáp Trực Tiếp Với Trợ Lý AI STEM")
        st.caption("Nhập câu hỏi để được AI giải đáp về kỹ thuật pha chế, quy chuẩn IFRA, và cách đánh giá cảm quan.")

        if "chat_messages" not in st.session_state:
            st.session_state["chat_messages"] = [
                {"role": "assistant", "content": f"Xin chào! Tôi là Trợ lý AI Chuyên sâu dự án STEM Nước Hoa. Bạn cần tư vấn gì về công thức mẻ **{selected_season_key}** hay các quy định an toàn phòng thí nghiệm không?"}
            ]

        for msg in st.session_state["chat_messages"]:
            if msg["role"] == "assistant":
                st.markdown(f"""
                <div class="chat-bubble-ai">
                    <b>🤖 Trợ Lý AI:</b><br>{msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"**👤 Bạn:** {msg['content']}")

        user_input = st.text_input("Nhập câu hỏi cho AI (ví dụ: Làm sao để lưu hương lâu hơn?):", key="ai_chat_input")
        if st.button("Gửi câu hỏi AI", use_container_width=True) and user_input:
            st.session_state["chat_messages"].append({"role": "user", "content": user_input})
            
            # Trả lời thông minh theo ngữ cảnh
            query = user_input.lower()
            if "lưu hương" in query or "lâu" in query:
                reply = "Để tăng độ lưu hương tự nhiên trên giấy thử, bạn nên giữ tỷ lệ Hương cuối (Base notes như Cedarwood, Vanilla) ở mức hợp lý (1.5% - 3.0%), đồng thời đảm bảo mẻ pha được ủ tĩnh (mating) ít nhất 24-48 giờ trước khi thử nghiệm."
            elif "an toàn" in query or "ifra" in query or "da" in query:
                reply = "Quy định an toàn STEM §9 nhấn mạnh: Nước hoa học đường chỉ được thử nghiệm trên giấy thử (blotter), tuyệt đối không xịt trực tiếp lên da. Tổng nồng độ tinh dầu không vượt quá 30%."
            elif "dung môi" in query or "cồn" in query or "ethanol" in query:
                reply = f"Dung môi Ethanol thực phẩm đóng vai trò hòa tan tinh dầu và giúp hương thơm bay hơi theo 3 tầng. Trong mẻ hiện tại, Ethanol chiếm **{solvent_pct:.1f}%** ({solvent_ml} mL)."
            else:
                reply = f"Công thức mẻ **{season_info['label'].split('—')[0]}** của bạn đang có tổng nồng độ tinh dầu là **{fragrance_total:.1f}%**. Đây là tỷ lệ rất đẹp và chuẩn cho mẻ học tập!"

            st.session_state["chat_messages"].append({"role": "assistant", "content": reply})
            st.rerun()

# ---------------------------------------------------------
# TAB 4: QUY TẮC AN TOÀN CHUẨN KẾ HOẠCH §9
# ---------------------------------------------------------
with tab_safety:
    st.subheader("⚠️ 6 Quy Tắc An Toàn Bắt Buộc (Kế Hoạch STEM §9)")
    st.caption("Toàn bộ học sinh và thành viên nhóm phải tuân thủ nghiêm ngặt các quy định phòng thí nghiệm bên dưới.")

    safety_rules = [
        ("1. Địa điểm & Giám sát", "Chỉ thực hành pha chế tại phòng thí nghiệm Hóa học dưới sự giám sát trực tiếp của giáo viên hướng dẫn."),
        ("2. Kiểm duyệt Nguyên liệu & SDS", "Chỉ sử dụng các nguyên liệu có trong danh mục phê duyệt, có nhãn mác và phiếu an toàn hóa chất SDS."),
        ("3. Không tiếp xúc trực tiếp", "Đánh giá cảm quan hoàn toàn trên giấy thử (blotter). Tuyệt đối không xịt trực tiếp lên da hay niêm mạc."),
        ("4. An toàn Ethanol chống cháy", "Ethanol là chất dễ cháy. Yêu cầu tuyệt đối không có nguồn nhiệt, ngọn lửa hay thiết bị phát tia lửa gần khu vực pha."),
        ("5. Trang bị Bảo hộ PPE", "Đeo kính bảo hộ, găng tay y tế và khẩu trang trong suốt quá trình thao tác với tinh dầu và dung môi."),
        ("6. Giới hạn Mục đích Học tập", "Sản phẩm thử nghiệm chỉ phục vụ mục đích nghiên cứu học thuật STEM, không lưu hành hay kinh doanh thương mại.")
    ]

    for title, detail in safety_rules:
        st.markdown(f"""
        <div class="safety-card">
            <div class="safety-card-title">{title}</div>
            <div class="safety-card-body">{detail}</div>
        </div>
        """, unsafe_allow_html=True)
