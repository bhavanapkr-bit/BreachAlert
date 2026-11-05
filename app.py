import streamlit as st
import pandas as pd
from pathlib import Path
st.set_page_config(page_title="BreachAlert | Exposure Monitor",page_icon="🛡️",layout="wide")
DATA=Path(__file__).parent/"data"/"breaches.csv"
@st.cache_data
def load(): return pd.read_csv(DATA,parse_dates=["breach_date"])
df=load()
st.sidebar.title("🛡️ BreachAlert")
st.sidebar.caption("Exposure monitoring • Demo")
page=st.sidebar.radio("Navigation",["Overview","Exposure Explorer","About"])
st.sidebar.divider(); st.sidebar.caption("DEMO MODE • Fictional records")
if page=="Overview":
 st.title("BreachAlert — Exposure Monitor")
 st.caption("A clear dashboard for reviewing illustrative exposure incidents.")
 a,b,c,d=st.columns(4); a.metric("Records",len(df)); b.metric("Critical",int((df.severity=="Critical").sum())); c.metric("High severity",int((df.severity=="High").sum())); d.metric("Unresolved",int((df.status=="Unresolved").sum()))
 x,y=st.columns(2)
 with x: st.subheader("Severity"); st.bar_chart(df.severity.value_counts())
 with y: st.subheader("Exposure types"); st.bar_chart(df.exposure_type.value_counts())
 st.subheader("Recent demo incidents"); st.dataframe(df.sort_values("breach_date",ascending=False),use_container_width=True,hide_index=True)
elif page=="Exposure Explorer":
 st.title("Exposure Explorer")
 x,y,z=st.columns(3); sev=x.multiselect("Severity",sorted(df.severity.unique()),default=sorted(df.severity.unique())); status=y.multiselect("Status",sorted(df.status.unique()),default=sorted(df.status.unique())); q=z.text_input("Search")
 view=df[df.severity.isin(sev)&df.status.isin(status)]
 if q: view=view[view.astype(str).apply(lambda r:r.str.contains(q,case=False).any(),axis=1)]
 st.write(f"Showing **{len(view)}** records"); st.dataframe(view,use_container_width=True,hide_index=True)
 st.download_button("⬇ Export current view (CSV)",view.to_csv(index=False).encode(),"breachalert_export.csv","text/csv")
 st.info("Fictional records only; no real breach lookup is performed.")
else:
 st.title("About BreachAlert")
 st.markdown("**BreachAlert** is a student dashboard prototype for organizing fictional exposure records.\n\n- Metrics and charts\n- Severity/status filters\n- Keyword search\n- CSV export\n\n**Ethics:** No external breach database, real-person lookup, or actual compromise verification.")
