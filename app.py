
import streamlit as st
import pandas as pd
from main_engine import run_pipeline

st.set_page_config(
    page_title="Compressor Performance Ranking",
    layout="wide"
)

st.title("⚙️ Compressor Performance Ranking System")

st.write(
"""
Upload a compressor performance Excel report.  
The system will analyze machine parameters and rank compressors
based on operational efficiency using a multi-criteria decision model.
"""
)

uploaded_file = st.file_uploader(
    "Upload Compressor Performance Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:
        with st.spinner("Processing compressor data..."):

            result = run_pipeline(uploaded_file)

        st.success("Analysis completed successfully")

        st.subheader("🏆 Compressor Ranking")

        st.dataframe(result, use_container_width=True, hide_index=False)

        # Best machine
        best_machine = result.iloc[0]["machine"]
        best_score = result.iloc[0]["performance_score"]

        st.success(
            f"Best Performing Compressor: **{best_machine}** "
            f"(Score: {best_score:.3f})"
        )
     
        # Performance chart
        st.subheader("📊 Performance Score Comparison")

        chart_data = result.set_index("machine")["performance_score"]

        st.bar_chart(chart_data)

        # Download results
        st.subheader("⬇️ Download Results")

        csv = result.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Ranking as CSV",
            data=csv,
            file_name="compressor_ranking.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error("An error occurred while processing the file.")
        st.exception(e)

else:
    st.info("Please upload an Excel file to start the analysis.")

