import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="SHL Recommender", layout="centered")

st.title("SHL Assessment Recommendation System")
st.write("Enter a job description or natural language query below to find the best matching SHL assessments.")

# Text input area
query = st.text_area("Job Description / Query:", height=150, placeholder="e.g., I am hiring for Java developers who can also collaborate effectively...")

# Submission button
if st.button("Get Recommendations", type="primary"):
    if query.strip():
        with st.spinner("Searching the SHL Catalog..."):
            try:
                # Call your local FastAPI server
                response = requests.post(
                    "http://127.0.0.1:8000/recommend",
                    json={"query": query},
                    timeout=10
                )
                
                if response.status_code == 200:
                    results = response.json().get("recommended_assessments", [])
                    
                    if results:
                        st.success(f"Found {len(results)} relevant assessments!")
                        
                        # Display the results beautifully
                        for idx, item in enumerate(results):
                            with st.expander(f"{idx + 1}. {item['name']}", expanded=(idx==0)):
                                st.markdown(f"**Description:** {item['description']}")
                                st.markdown(f"**Test Type:** {', '.join(item['test_type'])}")
                                
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Duration", f"{item['duration']} mins")
                                col2.metric("Remote Support", item['remote_support'])
                                col3.metric("Adaptive", item['adaptive_support'])
                                
                                st.markdown(f"[🔗 View Assessment on SHL]({item['url']})")
                    else:
                        st.warning("No recommendations found.")
                else:
                    st.error(f"Backend API Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the API. Make sure `python app.py` is running in another terminal!")
    else:
        st.warning("Please enter a query to get recommendations.")