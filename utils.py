import streamlit as st
import io
import matplotlib.pyplot as plt

def download_csv(df):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="scraped_data.csv",
        mime="text/csv"
    )

def download_chart_as_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    st.download_button(
        label="Download Chart as PNG",
        data=buf,
        file_name="chart.png",
        mime="image/png"
    )
