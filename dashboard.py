import streamlit as st
import cds.main as cds
import ctwp.main as ctwp
import scr.main as scr

st.set_page_config(page_title="Global Solution")
tab1, tab2, tab3 = st.tabs(["CTWP", "CDS", "SCR"])

with tab1:
    ctwp.dashboard()

with tab2:
    cds.dashboard()

with tab3:
    scr.dashboard()
