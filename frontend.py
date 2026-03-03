import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="SHL Recommender", page_icon="🎯", layout="centered")

st.title("🎯 SHL Assessment Recommendation System")
st.write("Enter a job description or natural language query below to find the best matching SHL assessments.")

# Text input area
query = st.text_area("Job Description / Query:", height=150, placeholder="e.g., I am hiring for Java developers who can also collaborate effectively...")

# Submission button
if st.button("Get Recommendations", type="primary"):
    if query.strip():
        with st.spinner("Searching the SHL Catalog..."):
            try:
                # 🛑 CRITICAL FIX: Added /recommend to the end of your Render URL
                api_url = "https://shl-assessment-recommender-mg1w.onrender.com/recommend"
                
                response = requests.post(
                    api_url,
                    json={"query": query},
                    timeout=30  # Increased timeout for slow cold starts on Render
                )
                
                if response.status_code == 200:
                    results = response.json().get("recommended_assessments", [])
                    
                    if results:
                        st.success(f"Found {len(results)} relevant assessments!")
                        
                        # Display the results beautifully
                        for idx, item in enumerate(results):
                            with st.expander(f"{idx + 1}. {item['name']}", expanded=(idx==0)):
                                st.markdown(f"**Description:** {item.get('description', 'No description available.')}")
                                
                                # Handling test_type list
                                t_type = item.get('test_type', [])
                                st.markdown(f"**Test Type:** {', '.join(t_type) if isinstance(t_type, list) else t_type}")
                                
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Duration", f"{item.get('duration', 'N/A')} mins")
                                col2.metric("Remote Support", item.get('remote_support', 'Yes'))
                                col3.metric("Adaptive", item.get('adaptive_support', 'No'))
                                
                                st.markdown(f"[🔗 View Assessment on SHL]({item['url']})")
                    else:
                        st.warning("No recommendations found. The catalog might still be loading.")
                else:
                    st.error(f"Backend API Error: {response.status_code}. Make sure the Render service is 'Live'.")
                    
            except requests.exceptions.Timeout:
                st.error("The request timed out. Render's free tier can be slow to wake up. Please wait 1 minute and try again.")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the API. Check your Render URL and ensure the service is active.")
    else:
        st.warning("Please enter a query to get recommendations.")