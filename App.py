import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Page Configuration
st.set_page_config(
    page_title="CoachBot A - AI Fitness Assistant",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2ecc71;
        margin-top: 1rem;
    }
    .info-box {
        background-color: #f0f8ff;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

# Get API key from Streamlit secrets (automatic)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Try to use gemini-1.5-pro-latest first, fallback to gemini-pro
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
    except:
        try:
            model = genai.GenerativeModel('gemini-pro')
        except:
            model = genai.GenerativeModel('gemini-1.0-pro')
    
    st.session_state.model = model
    st.session_state.api_key_configured = True
    st.session_state.temperature = 0.7  # Fixed temperature
    st.session_state.model_name = model.model_name
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.info("💡 Make sure you have a valid Gemini API key added to Streamlit secrets.")
    st.session_state.api_key_configured = False

# Sidebar - Configuration
with st.sidebar:
    st.title("🔧 CoachBot A")
    st.success("✅ API Key configured from secrets")
    
    st.divider()
    
    # Fixed temperature display (read-only)
    st.info("⚙️ Model Settings")
    st.write(f"**Temperature:** {st.session_state.temperature} (Fixed)")
    st.write("*Consistent, balanced recommendations*")
    
    if 'model_name' in st.session_state:
        st.divider()
        st.write(f"**Model:** {st.session_state.model_name}")

# Main App
if not st.session_state.api_key_configured:
    st.warning("⚠️ Please add GEMINI_API_KEY to Streamlit secrets to continue.")
else:
    st.markdown('<div class="main-header">💪 CoachBot A - Your AI Personal Fitness Coach</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.1rem;">Empowering young athletes with personalized, AI-powered coaching</p>', unsafe_allow_html=True)
    
    # Tabs for different features
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
        "🏋️ Workout Plan", "🏥 Recovery", "🎯 Tactical Tips", "🥗 Nutrition Guide", 
        "🔥 Warm-up/Cool-down", "🧠 Mental Training", "💧 Hydration", "👁️ Visualization",
        "📍 Position Drills", "🧘 Mobility", "📊 Dashboard"
    ])
    
    # ============================================
    # TAB 1: Full-Body Workout Plan Generator
    # ============================================
    with tab1:
        st.markdown('<div class="sub-header">🏋️ Full-Body Workout Plan Generator</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            sport = st.selectbox("Select Sport", [
                "Football", "Cricket", "Basketball", "Tennis", 
                "Athletics", "Swimming", "Volleyball", "Hockey", "Rugby", "Other"
            ], key="tab1_sport")
            position = st.selectbox("Player Position", [
                "Striker/Forward", "Midfielder", "Defender", "Goalkeeper",
                "Bowler", "Batsman", "Wicket Keeper", "All-rounder",
                "Point Guard", "Shooting Guard", "Center", "Power Forward", "Small Forward",
                "Sprinter", "Distance Runner", "Jumper", "Thrower",
                "General Athlete"
            ], key="tab1_position")
        
        with col2:
            fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"], key="tab1_fitness")
            training_days = st.slider("Training Days per Week", min_value=3, max_value=7, value=4, key="tab1_days")
            session_duration = st.slider("Session Duration (minutes)", min_value=30, max_value=120, value=60, key="tab1_duration")
        
        injuries = st.text_area("Current Injuries or Problem Areas (leave blank if none)", 
                               placeholder="e.g., ankle sprain, shoulder strain, knee pain...",
                               key="tab1_injuries")
        
        if st.button("Generate Workout Plan", key="tab1_generate"):
            with st.spinner("Creating your personalized workout plan..."):
                prompt = f"""
                Act as an expert sports coach and create a comprehensive full-body workout plan for a {position} in {sport}.
                
                Athlete Profile:
                - Fitness Level: {fitness_level}
                - Training Days: {training_days} days/week
                - Session Duration: {session_duration} minutes
                - Injuries/Concerns: {injuries if injuries else 'None - fully healthy'}
                
                Requirements:
                1. Create a structured weekly plan with specific exercises for each training day
                2. Include sets, reps, and rest periods
                3. Focus on position-specific skills and conditioning
                4. Modify exercises to accommodate any injuries
                5. Include progressive overload principles
                6. Provide clear instructions for each exercise
                7. Add intensity scales (RPE) for each session
                8. Response should be around 250-300 words
                9.Table is must in the workout plan
                
                
                Format the output in a clear, organized structure with weekly overview and daily breakdowns.
                Include safety warnings where applicable.
                """
                
                try:
                    generation_config = genai.types.GenerationConfig(
                        temperature=st.session_state.temperature,
                        top_p=0.9,
                        top_k=40,
                    )
                    
                    response = st.session_state.model.generate_content(
                        prompt, 
                        generation_config=generation_config
                    )
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("### 📋 Your Personalized Workout Plan")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating workout plan: {e}")
    
    # ============================================
    # TAB 2: Recovery Training Schedule
    # ============================================
    with tab2:
        st.markdown('<div class="sub-header">🏥 Safe Recovery Training Schedule</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            injury_type = st.selectbox("Type of Injury", [
                "None - General Recovery", "Knee Injury", "Ankle Sprain", "Shoulder Injury",
                "Hamstring Strain", "Lower Back Pain", "Wrist/Elbow Injury", "Concussion Recovery",
                "Muscle Strain", "Joint Pain", "Post-Surgery Recovery"
            ], key="tab2_injury")
            recovery_phase = st.selectbox("Recovery Phase", [
                "Acute Phase (0-72 hours)", "Sub-Acute Phase (3-14 days)", 
                "Remodeling Phase (2-6 weeks)", "Return to Sport Phase"
            ], key="tab2_phase")
        
        with col2:
            sport_focus = st.selectbox("Sport Focus", [
                "Football", "Cricket", "Basketball", "Tennis", "Athletics", "Swimming", "Other"
            ], key="tab2_sport")
            recovery_goal = st.selectbox("Primary Goal", [
                "Maintain Fitness", "Regain Mobility", "Strengthen Weak Areas",
                "Return to Play Prep", "Prevent Re-injury"
            ], key="tab2_goal")
        
        activity_level = st.text_area("Current Activity Level", 
                                     placeholder="e.g., can walk 20 mins, light jogging possible...",
                                     key="tab2_activity")
        
        if st.button("Generate Recovery Plan", key="tab2_generate"):
            with st.spinner("Designing your safe recovery program..."):
                prompt = f"""
                Act as a sports physical therapist and create a safe, progressive recovery training schedule.
                
                Athlete Profile:
                - Injury: {injury_type}
                - Recovery Phase: {recovery_phase}
                - Sport: {sport_focus}
                - Recovery Goal: {recovery_goal}
                - Current Activity: {activity_level if activity_level else 'Standard for this phase'}
                
                Requirements:
                1. Create a phased recovery plan with clear progression criteria
                2. Include mobility, strengthening, and conditioning exercises
                3. Specify exercises to AVOID at this stage
                4. Provide RPE (Rate of Perceived Exertion) guidelines
                5. Include daily pain monitoring recommendations
                6. Add signs to watch for that require medical attention
                7. Suggest cross-training activities that are safe
                8. Include timeline for progression to next phase
                
                Prioritize safety and gradual progression. Include specific exercises with modifications.
                """
                
                try:
                    generation_config = genai.types.GenerationConfig(
                        temperature=0.5,  # Slightly lower for safety
                        top_p=0.9,
                        top_k=40,
                    )
                    
                    response = st.session_state.model.generate_content(
                        prompt, 
                        generation_config=generation_config
                    )
                    
                    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                    st.markdown("### 🩺 Your Recovery Training Schedule")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating recovery plan: {e}")
    
    # ============================================
    # TAB 3: Tactical Coaching Tips
    # ============================================
    with tab3:
        st.markdown('<div class="sub-header">🎯 Tactical Coaching Tips</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            sport_tactical = st.selectbox("Sport for Tactical Advice", [
                "Football", "Cricket", "Basketball", "Tennis", "Volleyball", "Hockey"
            ], key="tab3_sport")
            position_tactical = st.selectbox("Position", [
                "Striker/Forward", "Midfielder", "Defender", "Goalkeeper",
                "Bowler", "Batsman", "Wicket Keeper", "All-rounder",
                "Point Guard", "Shooting Guard", "Center", "Power Forward", "Small Forward",
                "General Player"
            ], key="tab3_position")
        
        with col2:
            skill_focus = st.selectbox("Skill to Improve", [
                "Decision Making", "Positioning", "Game Awareness", "Communication",
                "Defensive Tactics", "Attacking Strategy", "Team Play", "Set Pieces",
                "Mental Game", "Pressure Situations"
            ], key="tab3_skill")
            experience_level = st.selectbox("Experience Level", ["Youth (Under 14)", "Junior (14-18)", "College", "Semi-Pro"], key="tab3_experience")
        
        match_situation = st.text_area("Specific Match Situations", 
                                      placeholder="e.g., defending a lead, playing against stronger opponents...",
                                      key="tab3_situation")
        
        if st.button("Generate Tactical Tips", key="tab3_generate"):
            with st.spinner("Analyzing tactical strategies..."):
                prompt = f"""
                Act as an expert tactical coach and provide advanced tactical coaching tips.
                
                Athlete Profile:
                - Sport: {sport_tactical}
                - Position: {position_tactical}
                - Skill Focus: {skill_focus}
                - Experience Level: {experience_level}
                - Specific Situations: {match_situation if match_situation else 'General gameplay'}
                
                Requirements:
                1. Provide 5-7 specific tactical tips for the chosen skill
                2. Include game scenarios where these apply
                3. Suggest drills to practice each tactical element
                4. Explain the 'why' behind each tactic (tactical reasoning)
                5. Include communication cues for teammates
                6. Add common mistakes to avoid
                7. Provide progression from practice to match application
                
                Make the tips practical, actionable, and appropriate for the experience level.
                Use coaching language that motivates and educates.
                """
                
                try:
                    generation_config = genai.types.GenerationConfig(
                        temperature=st.session_state.temperature,
                        top_p=0.9,
                        top_k=40,
                    )
                    
                    response = st.session_state.model.generate_content(
                        prompt, 
                        generation_config=generation_config
                    )
                    
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.markdown("### 🧠 Your Tactical Coaching Tips")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating tactical tips: {e}")
    
    # ============================================
    # TAB 4: Nutrition Guide Generator
    # ============================================
    with tab4:
        st.markdown('<div class="sub-header">🥗 Personalized Nutrition Guide</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age", min_value=10, max_value=25, value=15, key="tab4_age")
            gender = st.selectbox("Gender", ["Male", "Female"], key="tab4_gender")
            weight = st.number_input("Weight (kg)", min_value=30, max_value=120, value=60, key="tab4_weight")
        
        with col2:
            height = st.number_input("Height (cm)", min_value=120, max_value=210, value=170, key="tab4_height")
            diet_type = st.selectbox("Diet Type", ["Non-Vegetarian", "Vegetarian", "Vegan", "Eggetarian"], key="tab4_diet")
            activity_level_nutrition = st.selectbox("Daily Activity Level", [
                "Light (1-2 training sessions)", "Moderate (3-4 sessions)", 
                "Heavy (5-6 sessions)", "Very Heavy (Daily + Competition)"
            ], key="tab4_activity")
        
        with col3:
            calorie_goal = st.selectbox("Calorie Goal", [
                "Maintain Weight", "Build Muscle", "Lose Fat", "Performance Optimization"
            ], key="tab4_calorie")
            allergies = st.text_area("Food Allergies/Restrictions", 
                                   placeholder="e.g., lactose intolerance, nut allergy...",
                                   key="tab4_allergies")
            sport_nutrition = st.selectbox("Primary Sport", [
                "Football", "Cricket", "Basketball", "Athletics", "Swimming", "Tennis", "Other"
            ], key="tab4_sport")
        
        if st.button("Generate Nutrition Plan", key="tab4_generate"):
            with st.spinner("Creating your personalized nutrition guide..."):
                prompt = f"""
                Act as a sports nutritionist and create a comprehensive week-long nutrition guide.
                
                Athlete Profile:
                - Age: {age}, Gender: {gender}
                - Weight: {weight}kg, Height: {height}cm
                - Diet Type: {diet_type}
                - Activity Level: {activity_level_nutrition}
                - Calorie Goal: {calorie_goal}
                - Primary Sport: {sport_nutrition}
                - Allergies/Restrictions: {allergies if allergies else 'None'}
                
                Requirements:
                1. Calculate and display daily calorie and macronutrient needs
                2. Create a detailed 7-day meal plan (breakfast, lunch, dinner, snacks)
                3. Include pre-training and post-training nutrition recommendations
                4. Suggest meal timing strategies around training sessions
                5. Provide hydration guidelines
                6. Include recovery nutrition tips
                7. Suggest healthy snack options
                8. Add supplement recommendations (if appropriate for age)
                9. Include portion sizes and preparation tips
                
                All recommendations must be age-appropriate and safe for youth athletes.
                Focus on whole foods and balanced nutrition.
                """
                
                try:
                    generation_config = genai.types.GenerationConfig(
                        temperature=st.session_state.temperature,
                        top_p=0.9,
                        top_k=40,
                    )
                    
                    response = st.session_state.model.generate_content(
                        prompt, 
                        generation_config=generation_config
                    )
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("### 🍽️ Your Personalized Nutrition Guide")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating nutrition plan: {e}")
    
    # ============================================
    # TAB 5: Warm-up and Cool-down Routines
    # ============================================
    with tab5:
        st.markdown('<div class="sub-header">🔥 Warm-up & Cool-down Routines</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            sport_warmup = st.selectbox("Sport", [
                "Football", "Cricket", "Basketball", "Tennis", "Athletics", "Swimming", "Volleyball"
            ], key="tab5_sport")
            routine_type = st.selectbox("Routine Type", [
                "Pre-Training Warm-up", "Pre-Match Warm-up", "Post-Training Cool-down", 
                "Post-Match Cool-down", "Rest Day Active Recovery"
            ], key="tab5_routine")
        
        with col2:
            position_warmup = st.selectbox("Position", [
                "Striker/Forward", "Midfielder", "Defender", "Goalkeeper",
                "Bowler", "Batsman", "All-rounder", "General Player"
            ], key="tab5_position")
            available_time = st.slider("Available Time (minutes)", min_value=5, max_value=30, value=10, key="tab5_time")
        
        focus_areas = st.multiselect("Focus Areas", [
            "Dynamic Stretching", "Mobility", "Injury Prevention", 
            "Activation", "Flexibility", "Relaxation", "Breathing"
        ], key="tab5_focus")
        
        if st.button("Generate Routines", key="tab5_generate"):
            with st.spinner("Creating your warm-up/cool-down routine..."):
                prompt = f"""
                Act as a sports performance coach and create personalized warm-up/cool-down routines.
                
                Session Details:
                - Sport: {sport_warmup}
                - Position: {position_warmup}
                - Routine Type: {routine_type}
                - Available Time: {available_time} minutes
                - Focus Areas: {', '.join(focus_areas) if focus_areas else 'Comprehensive'}
                
                Requirements:
                1. Create a structured routine fitting within the time limit
                2. Include specific exercises with clear instructions
                3. Specify duration for each exercise
                4. Include variations for different fitness levels
                5. Explain the purpose of each exercise
                6. Add safety cues and common mistakes to avoid
                7. Include breathing techniques where applicable
                8. Provide modifications for any sensitive areas
                
                Make the routine practical and easy to follow. Use bullet points and clear numbering.
                """
                
                try:
                    generation_config = genai.types.GenerationConfig(
                        temperature=0.6,
                        top_p=0.9,
                        top_k=40,
                    )
                    
                    response = st.session_state.model.generate_content(
                        prompt, 
                        generation_config=generation_config
                    )
                    
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.markdown("### 🏃 Your Warm-up/Cool-down Routine")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating routine: {e}")
    
    # ============================================
    # TAB 6: Mental Focus & Training Routines
    # ============================================
    with tab6:
        st.markdown('<div class="sub-header">🧠 Mental Training & Focus Routines</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            mental_goal = st.selectbox("Mental Training Goal", [
                "Tournament Preparation", "Match Day Focus", "Overcoming Anxiety",
                "Building Confidence", "Handling Pressure", "Staying Motivated",
                "Recovery from Poor Performance", "Concentration Improvement"
            ], key="tab6_goal")
            sport_mental = st.selectbox("Sport", [
                "Football", "Cricket", "Basketball", "Tennis", "Athletics", "Swimming"
            ], key="tab6_sport")
        
        with col2:
            upcoming_event = st.selectbox("Upcoming Event Type", [
                "Tournament", "Important Match", "Championship", 
                "Regular Season Game", "Training Camp", "No Specific Event"
            ], key="tab6_event")
            time_to_event = st.selectbox("Time to Event", [
                "Today (Game Day)", "1-3 Days", "1 Week", "2-4 Weeks", "Off-Season"
            ], key="tab6_time")
        
        current_challenges = st.text_area("Current Mental Challenges", 
                                         placeholder="e.g., nervousness before games, losing focus during matches...",
                                         key="tab6_challenges")
        
        if st.button("Generate Mental Training Program", key="tab6_generate"):
            with st.spinner("Designing your mental training program..."):
                prompt = f"""
                Act as a sports psychologist and create a comprehensive mental training program.
                
                Athlete Profile:
                - Mental Goal: {mental_goal}
                - Sport: {sport_mental}
                - Upcoming Event: {upcoming_event}
                - Time to Event: {time_to_event}
                - Current Challenges: {current_challenges if current_challenges else 'None specified'}
                
                Requirements:
                1. Provide daily mental training exercises
                2. Include visualization techniques specific to the sport
                3. Suggest breathing and relaxation methods
                4. Create pre-performance routines
                5. Provide positive self-talk affirmations
                6. Include goal-setting strategies
                7. Add techniques for managing pressure and anxiety
                8. Provide recovery mental practices
                9. Include progress tracking methods
                
                Make the program practical and age-appropriate for young athletes.
                Include specific examples and scenarios.
                """
                
                try:
                    generation_config = genai.types.GenerationConfig(
                        temperature=st.session_state.temperature,
                        top_p=0.9,
                        top_k=40,
                    )
                    
                    response = st.session_state.model.generate_content(
                        prompt, 
                        generation_config=generation_config
                    )
                    
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.markdown("### 🧘 Your Mental Training Program")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating mental training: {e}")
    
    # ============================================
    # TAB 7: Hydration & Electrolyte Strategies
    # ============================================
    with tab7:
        st.markdown('<div class="sub-header">💧 Hydration & Electrolyte Strategy</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            sport_hydration = st.selectbox("Primary Sport", [
                "Football", "Cricket", "Basketball", "Tennis", "Athletics", "Swimming"
            ], key="tab7_sport")
            training_duration = st.slider("Typical Training Duration (minutes)", 
                                       min_value=30, max_value=180, value=90, key="tab7_duration")
        
        with col2:
            climate = st.selectbox("Training Climate", [
                "Cool (Under 15°C)", "Moderate (15-25°C)", 
                "Warm (25-30°C)", "Hot (30°C+)", "Humid"
            ], key="tab7_climate")
            sweat_rate = st.selectbox("Sweat Rate", ["Low", "Moderate", "High", "Very High"], key="tab7_sweat")
        
        if st.button("Generate Hydration Plan", key="tab7_generate"):
            with st.spinner("Creating your hydration strategy..."):
                prompt = f"""
                Act as a sports nutritionist specializing in hydration and electrolyte management.
                
                Athlete Profile:
                - Sport: {sport_hydration}
                - Training Duration: {training_duration} minutes
                - Climate: {climate}
                - Sweat Rate: {sweat_rate}
                
                Requirements:
                1. Calculate daily hydration needs (in liters)
                2. Create a pre-training hydration protocol
                3. Design during-training hydration schedule
                4. Provide post-training rehydration guidelines
                5. Explain electrolyte replacement needs
                6. Suggest natural electrolyte sources
                7. Include signs of dehydration to watch for
                8. Provide hydration for different weather conditions
                9. Create a daily hydration timeline
                10. Add tips for carrying and consuming fluids during matches
                
                Make recommendations practical for young athletes. Include timing and quantities.
                """
                
                try:
                    generation_config = genai.types.GenerationConfig(
                        temperature=0.6,
                        top_p=0.9,
                        top_k=40,
                    )
                    
                    response = st.session_state.model.generate_content(
                        prompt, 
                        generation_config=generation_config
                    )
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("### 💧 Your Hydration Strategy")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating hydration plan: {e}")
    
    # ============================================
    # TAB 8: Pre-Match Visualization
    # ============================================
    with tab8:
        st.markdown('<div class="sub-header">👁️ Pre-Match Visualization Techniques</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            sport_viz = st.selectbox("Sport", [
                "Football", "Cricket", "Basketball", "Tennis", "Athletics", "Swimming"
            ], key="tab8_sport")
            position_viz = st.selectbox("Position", [
                "Striker/Forward", "Midfielder", "Defender", "Goalkeeper",
                "Bowler", "Batsman", "Wicket Keeper", "All-rounder",
                "General Player"
            ], key="tab8_position")
        
        with col2:
            match_importance = st.selectbox("Match Importance", [
                "Regular Season", "Tournament Game", "Championship Final", 
                "Qualifying Match", "Friendly"
            ], key="tab8_importance")
            viz_preference = st.selectbox("Visualization Focus", [
                "Performance Skills", "Confidence Building", "Handling Pressure",
                "Specific Scenarios", "Complete Match Day Experience"
            ], key="tab8_preference")
        
        specific_scenarios = st.text_area("Specific Scenarios to Visualize", 
                                          placeholder="e.g., taking penalty kick, facing fast bowling, last minute defense...",
                                          key="tab8_scenarios")
        
        if st.button("Generate Visualization Guide", key="tab8_generate"):
            with st.spinner("Creating your visualization program..."):
                prompt = f"""
                Act as a sports psychology expert specializing in visualization and imagery.
                
                Athlete Profile:
                - Sport: {sport_viz}
                - Position: {position_viz}
                - Match Importance: {match_importance}
                - Visualization Focus: {viz_preference}
                - Specific Scenarios: {specific_scenarios if specific_scenarios else 'General match situations'}
                
                Requirements:
                1. Create a 10-15 minute pre-match visualization script
                2. Include guided imagery for key game moments
                3. Incorporate all senses (sight, sound, touch, feeling)
                4. Provide visualization for success scenarios
                5. Include techniques for managing unexpected situations
                6. Add breathing and relaxation components
                7. Create a match-day visualization timeline
                8. Include quick 2-3 minute visualization options
                9. Provide tips for effective visualization practice
                10. Add confidence-building visualization exercises
                
                Write the visualization script in first person, guiding the athlete through each step.
                Make it engaging and emotionally positive.
                """
                
                try:
                    generation_config = genai.types.GenerationConfig(
                        temperature=st.session_state.temperature,
                        top_p=0.9,
                        top_k=40,
                    )
                    
                    response = st.session_state.model.generate_content(
                        prompt, 
                        generation_config=generation_config
                    )
                    
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.markdown("### 🎯 Your Visualization Guide")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating visualization guide: {e}")
    
    # ============================================
    # TAB 9: Position-Specific Decision Drills
    # ============================================
    with tab9:
        st.markdown('<div class="sub-header">📍 Position-Specific Decision Drills</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            sport_drill = st.selectbox("Sport", [
                "Football", "Cricket", "Basketball", "Tennis", "Volleyball", "Hockey"
            ], key="tab9_sport")
            position_drill = st.selectbox("Position", [
                "Striker/Forward", "Midfielder", "Defender", "Goalkeeper",
                "Bowler", "Batsman", "Wicket Keeper", "All-rounder",
                "Point Guard", "Shooting Guard", "Center", "Power Forward", "Small Forward"
            ], key="tab9_position")
        
        with col2:
            decision_area = st.selectbox("Decision Area", [
                "Game Situations", "Positioning", "Timing", "Communication",
                "Under Pressure", "Transitional Play", "Set Pieces", "Team Tactics"
            ], key="tab9_area")
            skill_level_drill = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"], key="tab9_level")
        
        if st.button("Generate Decision Drills", key="tab9_generate"):
            with st.spinner("Creating position-specific drills..."):
                prompt = f"""
                Act as an expert tactical coach and design position-specific decision-making drills.
                
                Athlete Profile:
                - Sport: {sport_drill}
                - Position: {position_drill}
                - Decision Area: {decision_area}
                - Skill Level: {skill_level_drill}
                
                Requirements:
                1. Create 5-7 progressive decision-making drills
                2. Each drill should include:
                   - Clear setup and equipment needed
                   - Specific objectives
                   - Step-by-step instructions
                   - Decision points to focus on
                   - Progressions and variations
                   - Coaching cues and feedback points
                3. Include individual and team drill options
                4. Add time requirements and space needs
                5. Include scoring or measurement methods
                6. Provide common mistakes and corrections
                7. Add competitive elements where appropriate
                
                Focus on developing quick, smart decisions in game-like situations.
                Make drills engaging and challenging for the skill level.
                """
                
                try:
                    generation_config = genai.types.GenerationConfig(
                        temperature=st.session_state.temperature,
                        top_p=0.9,
                        top_k=40,
                    )
                    
                    response = st.session_state.model.generate_content(
                        prompt, 
                        generation_config=generation_config
                    )
                    
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.markdown("### 🏟️ Your Position-Specific Drills")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating drills: {e}")
    
    # ============================================
    # TAB 10: Mobility & Post-Injury Workouts
    # ============================================
    with tab10:
        st.markdown('<div class="sub-header">🧘 Mobility & Recovery Workouts</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            mobility_focus = st.selectbox("Mobility Focus", [
                "Full Body", "Lower Body", "Upper Body", "Spine & Core",
                "Hip Mobility", "Shoulder Mobility", "Ankle & Foot", "Post-Injury Recovery"
            ], key="tab10_focus")
            mobility_goal = st.selectbox("Primary Goal", [
                "Improve Flexibility", "Reduce Muscle Tension", "Enhance Range of Motion",
                "Injury Prevention", "Recovery After Training", "Joint Health"
            ], key="tab10_goal")
        
        with col2:
            time_available = st.slider("Time Available (minutes)", min_value=10, max_value=60, value=20, key="tab10_time")
            equipment = st.multiselect("Available Equipment", [
                "None (Bodyweight only)", "Resistance Bands", "Foam Roller",
                "Yoga Mat", "Medicine Ball", "Pilates Ball"
            ], key="tab10_equipment")
        
        injury_history_mobility = st.text_area("Relevant Injury History", 
                                              placeholder="e.g., past ankle injury, tight hamstrings, shoulder issues...",
                                              key="tab10_injury")
        
        if st.button("Generate Mobility Program", key="tab10_generate"):
            with st.spinner("Creating your mobility program..."):
                prompt = f"""
                Act as a sports physiotherapist and create a comprehensive mobility and recovery workout.
                
                Session Details:
                - Focus Area: {mobility_focus}
                - Primary Goal: {mobility_goal}
                - Time Available: {time_available} minutes
                - Equipment: {', '.join(equipment) if equipment else 'Bodyweight only'}
                - Injury History: {injury_history_mobility if injury_history_mobility else 'None'}
                
                Requirements:
                1. Create a structured mobility session fitting the time limit
                2. Include dynamic and static mobility exercises
                3. Specify duration and repetitions for each exercise
                4. Provide clear instructions and technique cues
                5. Include breathing techniques for each movement
                6. Add progression and regression options
                7. Include foam rolling or myofascial release if equipment allows
                8. Provide modifications for any injury history
                9. Add stretches for tight muscle groups
                10. Include functional mobility movements relevant to sports
                
                Prioritize safe, effective movements. Explain the 'why' behind each exercise.
                """
                
                try:
                    generation_config = genai.types.GenerationConfig(
                        temperature=0.5,
                        top_p=0.9,
                        top_k=40,
                    )
                    
                    response = st.session_state.model.generate_content(
                        prompt, 
                        generation_config=generation_config
                    )
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("### 🧘 Your Mobility Program")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating mobility program: {e}")
    
    # ============================================
    # TAB 11: Dashboard
    # ============================================
    with tab11:
        st.markdown('<div class="sub-header">📊 CoachBot Dashboard</div>', unsafe_allow_html=True)
        
        # Session Statistics
        st.subheader("📈 Session Overview")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Features", "10+ Coaching Modules")
        with col2:
            st.metric("Sports Supported", "10+ Sports")
        with col3:
            st.metric("User Age Range", "10-25 Years")
        
        st.divider()
        
        # Feature Summary
        st.subheader("🎯 Available Features")
        
        features_data = {
            "Feature": [
                "Full-Body Workout Plans",
                "Recovery Training Schedules",
                "Tactical Coaching Tips",
                "Personalized Nutrition Guides",
                "Warm-up/Cool-down Routines",
                "Mental Training Programs",
                "Hydration Strategies",
                "Pre-Match Visualization",
                "Position-Specific Drills",
                "Mobility & Recovery Workouts"
            ],
            "Best For": [
                "Strength & Conditioning",
                "Injury Rehabilitation",
                "Game Intelligence",
                "Performance Nutrition",
                "Injury Prevention",
                "Mental Toughness",
                "Optimal Hydration",
                "Confidence Building",
                "Decision Making",
                "Flexibility & Recovery"
            ],
            "Temperature": [
                "0.7 (Fixed)",
                "0.5 (Safety)",
                "0.7 (Fixed)",
                "0.7 (Fixed)",
                "0.6 (Balanced)",
                "0.7 (Fixed)",
                "0.6 (Scientific)",
                "0.7 (Fixed)",
                "0.7 (Fixed)",
                "0.5 (Safety)"
            ]
        }
        
        df_features = pd.DataFrame(features_data)
        st.dataframe(df_features, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Tips Section
        st.subheader("💡 Pro Tips for Best Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **🎯 For Workout Plans:**
            - Always include injury history for safe recommendations
            - Start with lower fitness level if unsure
            - Follow progressive overload principles
            
            **🏥 For Recovery:**
            - Be honest about current pain levels
            - Follow medical advice first
            - Progress gradually through phases
            """)
        
        with col2:
            st.info("""
            **🧠 For Mental Training:**
            - Practice visualization daily for best results
            - Start with shorter sessions and build up
            - Combine with physical practice
            
            **🥗 For Nutrition:**
            - Be specific about allergies and restrictions
            - Consult with parents/guardians for dietary changes
            - Focus on whole foods over supplements
            """)
        
        st.divider()
        
        # Sports Covered
        st.subheader("🏅 Supported Sports")
        
        sports_list = [
            "Football (Soccer)", "Cricket", "Basketball", "Tennis", "Athletics",
            "Swimming", "Volleyball", "Hockey", "Rugby", "Baseball", "Softball",
            "Badminton", "Table Tennis", "Gymnastics", "Martial Arts", "Wrestling",
            "Boxing", "Cross Country", "Track & Field", "Water Polo"
        ]
        
        cols = st.columns(5)
        for idx, sport in enumerate(sports_list):
            cols[idx % 5].markdown(f"• {sport}")
        
        st.divider()
        
        # About the App
        st.subheader("ℹ️ About CoachBot A")
        
        st.markdown("""
        **CoachBot A** is an AI-powered personal fitness coaching assistant designed specifically for young athletes (ages 10-25).
        
        ### Key Objectives:
        - ✅ Empower youth with AI-based personal training
        - ✅ Generate adaptive fitness routines based on physical condition
        - ✅ Encourage safety, motivation, and nutrition awareness
        - ✅ Provide accessibility for low-resource areas
        
        ### Technology Stack:
        - **AI Model**: Google gemini-2.5-flash
        - **Framework**: Streamlit
        - **Language**: Python
        
        ### Safety Features:
        - Injury-aware exercise modifications
        - Age-appropriate recommendations
        - Progressive training principles
        - Medical disclaimer for all content
        
        ### Developed For:
        - Young athletes seeking personalized coaching
        - Youth sports programs
        - Schools and sports academies
        - Under-resourced communities with limited coaching access
        """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💪 <strong>CoachBot A</strong> - AI-Powered Fitness Assistant | Powered by Gemini 1.5</p>
    <p>⚠️ <em>Disclaimer: Always consult with qualified coaches, trainers, or medical professionals before starting any new exercise program.</em></p>
</div>
""", unsafe_allow_html=True)
