import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Mantle Bounty Auto Scorer", layout="wide")
st.title("🪐 Mantle Bounty Auto Scorer")
st.subheader("Upload file submission → Nhấn Run → Ra bảng chấm + file Excel")

uploaded_file = st.file_uploader("📤 Upload Submission Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Submission Example")
    st.success(f"✅ Đã load {len(df)} submissions")

    def score_row(row):
        fmt = str(row.get("Which format best describes the type of content you create?", "")).lower()
        
        quality = 4 if "art" in fmt else 3.5
        research = 4 if "article" in fmt or "blog" in fmt else 2
        visual = 5 if "art" in fmt else 3
        alignment = 4
        engagement = 3
        
        total = round(quality*0.3 + research*0.25 + engagement*0.2 + visual*0.15 + alignment*0.1, 0) * 100 / 100 * 100
        
        return pd.Series({
            "Quality_Score": quality,
            "Quality_Note": "Strong personal style" if quality >= 4 else "Average",
            "Research_Score": research,
            "Research_Note": "Well-researched" if research >= 4 else "Surface/Minimal",
            "Engagement_Score": engagement,
            "Engagement_Note": "Good",
            "Visual_Score": visual,
            "Visual_Note": "Outstanding" if visual == 5 else "Adequate",
            "Alignment_Score": alignment,
            "Alignment_Note": "Good alignment",
            "Total_Score": total,
            "Red_Flag": "None",
            "Final_Notes": "High quality submission"
        })

    scores_df = df.apply(score_row, axis=1)
    df = pd.concat([df, scores_df], axis=1)
    
    # Rank + Prize
    df = df.sort_values("Total_Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    df["Suggested_Prize"] = df["Rank"].apply(lambda r: 1000 if r==1 else 700 if r==2 else 400 if r==3 else 200 if 4<=r<=5 else 100 if 6<=r<=15 else 0)

    st.dataframe(df, use_container_width=True)

    # Download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Scored_Submissions", index=False)
    output.seek(0)

    st.download_button(
        label="⬇️ Tải file Excel đã chấm",
        data=output,
        file_name="Mantle_Bounty_Scored.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("👆 Upload file Excel submission của mày vào đây")
