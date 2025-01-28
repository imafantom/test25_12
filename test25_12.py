import streamlit as st
import random
from PIL import Image

# Sample data structure (you'll need to expand this)
tenses_data = {
    "Present Simple": {
        "name": "Present Simple",
        "illustration_url": "https://example.com/present-simple.png",
        "formation": {
            "Positive": "Subject + base verb",
            "Negative": "Subject + do/does + not + base verb",
            "Question": "Do/Does + subject + base verb?"
        },
        "usage_explanation": ["Habits", "Facts", "Scheduled events"],
        "usage_cases": [
            {
                "title": "Daily Routine",
                "context": "Describe your morning routine",
                "question_type": "open_ended",
                "question": "Complete this sentence: I ______ (wake up) at 7 AM every day."
            }
        ],
        "extra_examples": ["The sun rises in the east.", "She works at a hospital."]
    }
}

conditionals_data = {
    "Zero Conditional": {
        "name": "Zero Conditional",
        "illustration_url": "https://example.com/zero-conditional.png",
        "formation": {
            "Positive": "If + present simple, present simple"
        },
        "usage_explanation": ["General truths", "Scientific facts"],
        "usage_cases": [
            {
                "title": "Scientific Fact",
                "question_type": "multiple_choice",
                "question": "Complete: If you heat water to 100°C, it ______.",
                "choices": ["boils", "boiled", "will boil"],
                "correct_choice": "boils"
            }
        ],
        "extra_examples": ["If you mix red and blue, you get purple."]
    }
}

# Initialize session state
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Sidebar controls
st.sidebar.title("Grammar Genius Game")
category = st.sidebar.radio("Category", ["Tenses", "Conditionals"])
selected_item = st.sidebar.selectbox(
    "Select Item",
    list(tenses_data.keys() if category == "Tenses" else conditionals_data.keys())
)

theme = st.sidebar.radio("Theme", ["Light", "Dark"])
font_size = st.sidebar.radio("Font Size", ["Small", "Medium", "Large"])

# Dynamic CSS styling
font_sizes = {"Small": "16px", "Medium": "20px", "Large": "24px"}
theme_styles = {
    "Light": {"bg": "#ffffff", "text": "#000000", "sidebar": "#f0f2f6"},
    "Dark": {"bg": "#000000", "text": "#ffffff", "sidebar": "#001158"}
}

st.markdown(f"""
    <style>
    html {{
        font-size: {font_sizes[font_size]}!important;
    }}
    .main {{
        background-color: {theme_styles[theme]['bg']};
        color: {theme_styles[theme]['text']};
    }}
    .sidebar .sidebar-content {{
        background-color: {theme_styles[theme]['sidebar']}!important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Main content
st.title("📚 Grammar Genius Game")
data = tenses_data if category == "Tenses" else conditionals_data
item_data = data[selected_item]

# Display grammar item info
st.header(item_data['name'])
if item_data['illustration_url']:
    st.image(item_data['illustration_url'], width=200)

with st.expander("Formation Rules"):
    for key, value in item_data['formation'].items():
        st.write(f"**{key}**: {value}")

with st.expander("Usage Explanations"):
    for explanation in item_data['usage_explanation']:
        st.write(f"- {explanation}")

# Progress tracking
total_questions = len(item_data['usage_cases'])
progress = st.session_state.current_question / total_questions
st.progress(progress)
col1, col2 = st.columns(2)
col1.metric("Questions Answered", f"{st.session_state.current_question}/{total_questions}")
col2.metric("Progress", f"{int(progress*100)}%")

# Questions handling
if st.session_state.current_question < total_questions:
    question_data = item_data['usage_cases'][st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1}")
    
    if 'context' in question_data:
        st.write(f"**Scenario**: {question_data['context']}")
    
    if question_data['question_type'] == 'multiple_choice':
        user_answer = st.selectbox(
            question_data['question'],
            question_data['choices']
        )
        if st.button("Submit Answer"):
            if user_answer == question_data['correct_choice']:
                st.success("Correct! 🎉")
                st.session_state.current_question += 1
            else:
                st.error("Try again! 💪")
    else:
        user_answer = st.text_input(question_data['question'])
        if user_answer:
            st.success("Great attempt! Keep going! 🌟")
            st.session_state.current_question += 1

    # Motivational messages
    motivations = ["Awesome! 🚀", "You're crushing it! 💥", "Grammar master! 📖"]
    st.write(random.choice(motivations))

# Completion state
else:
    st.balloons()
    st.success(f"Badge Unlocked: {selected_item} Expert! 🏆")
    
    if st.button("Review Your Answers"):
        for idx, question in enumerate(item_data['usage_cases']):
            st.write(f"**Question {idx+1}**: {question['question']}")
            st.write(f"**Your Answer**: {st.session_state.answers.get(idx, 'N/A')}")
            if question['question_type'] == 'multiple_choice':
                st.write(f"**Correct Answer**: {question['correct_choice']}")
            st.write("---")

# Add to requirements.txt:
# streamlit
# Pillow
