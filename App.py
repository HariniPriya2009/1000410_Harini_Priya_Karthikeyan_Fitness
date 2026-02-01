try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Use gemini-pro (most commonly available)
    model = genai.GenerativeModel('gemini-pro')
    
    st.session_state.model = model
    st.session_state.api_key_configured = True
    st.session_state.temperature = 0.7
    st.session_state.model_name = model.model_name
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.info("💡 Make sure you have a valid Gemini API key added to Streamlit secrets.")
    st.session_state.api_key_configured = False

