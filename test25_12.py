import streamlit as st
import random
from enum import Enum

# =================================================================================
# 1. Initialization & Constants
# =================================================================================
class GrammarCategory(Enum):
    TENSES = "Tenses"
    CONDITIONALS = "Conditionals"

MOTIVATIONAL_MESSAGES = [
    "You're on fire! 🔥", "Keep smashing it! 💥", 
    "Fantastic answer! 🌟", "Grammar wizard! 🧙♂️",
    "Way to go, champ! 🏆", "Bravo! 👏", "Remarkable! 🎩✨"
]

THEMES = {
    "Dark": {
        "main_bg": "#000000", "main_color": "#FFFFFF",
        "sidebar_bg": "#013369", "heading_color": "#FF5722",
        "font_size": "18px", "border_color": "#555555"
    },
    "Light": {
        "main_bg": "#FFFFFF", "main_color": "#000000",
        "sidebar_bg": "#F0F0F0", "heading_color": "#FF5722",
        "font_size": "18px", "border_color": "#CCCCCC"
    }
}

CSS_TEMPLATE = """
<style>
:root {{
    --main-bg: {main_bg};
    --main-color: {main_color};
    --sidebar-bg: {sidebar_bg};
    --heading-color: {heading_color};
    --font-size: {font_size};
    --border-color: {border_color};
}}

[data-testid="stAppViewContainer"] {{
    background-color: var(--main-bg) !important;
    color: var(--main-color) !important;
    font-size: var(--font-size);
}}

[data-testid="stSidebar"] {{
    background-color: var(--sidebar-bg) !important;
}}

h1, h2, h3 {{
    color: var(--heading-color) !important;
    font-family: 'Trebuchet MS', sans-serif;
    border-bottom: 2px solid var(--heading-color);
    padding-bottom: 0.3em;
}}

.stSelectbox, .stRadio, .stButton {{
    margin: 1rem 0;
}}

.stProgress > div > div {{
    background-color: var(--heading-color) !important;
}}
</style>
"""

# =================================================================================
# 2. Session State Initialization
# =================================================================================
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "selected_category": GrammarCategory.TENSES,
        "selected_item_key": None,
        "answers": [],
        "submitted_questions": set(),
        "review_mode": False,
        "randomized_messages": random.sample(MOTIVATIONAL_MESSAGES, len(MOTIVATIONAL_MESSAGES))
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# =================================================================================
# 3. Data Structures (Simplified for Demo)
# =================================================================================
TENSES_DATA = {
    "1": {
        "name": "Present Simple",
        "formation": {
            "Positive": "Subject + base form",
            "Negative": "Subject + do not/does not + base form",
            "Question": "Do/Does + subject + base form?"
        },
        "usage_cases": [
            {
                "question": "He ________ English every week.",
                "choices": ["study", "studies", "studys"],
                "correct": "studies"
            }
        ]
    }
}

CONDITIONALS_DATA = {
    "0": {
        "name": "Zero Conditional",
        "formation": {
            "Positive": "If + present simple, present simple",
            "Negative": "If + present simple, present simple (negative)"
        },
        "usage_cases": [
            {
                "question": "If you don't water plants, they ________.",
                "choices": ["die", "dies", "dying"],
                "correct": "die"
            }
        ]
    }
}

# =================================================================================
# 4. Core Components
# =================================================================================
def render_sidebar():
    """Sidebar with navigation and theme controls"""
    with st.sidebar:
        st.title("Grammar Master")
        
        # Category selection
        category = st.radio(
            "Category:",
            options=[c.value for c in GrammarCategory],
            index=0
        )
        st.session_state.selected_category = GrammarCategory(category)
        
        # Item selection
        render_item_selector()
        
        # Theme selection
        theme = st.radio("Theme:", options=list(THEMES.keys()))
        apply_theme(theme)

def render_item_selector():
    """Dynamic grammar item selector"""
    data = TENSES_DATA if st.session_state.selected_category == GrammarCategory.TENSES else CONDITIONALS_DATA
    items = [f"{k}. {v['name']}" for k, v in data.items()]
    
    selected = st.selectbox(
        f"Select {st.session_state.selected_category.value[:-1]}:",
        ["Choose..."] + items
    )
    
    if selected != "Choose...":
        key = selected.split(".", 1)[0].strip()
        if key != st.session_state.selected_item_key:
            st.session_state.selected_item_key = key
            reset_questions()

def apply_theme(theme: str):
    """Apply selected theme CSS"""
    css = CSS_TEMPLATE.format(**THEMES[theme])
    st.markdown(css, unsafe_allow_html=True)

# =================================================================================
# 5. Main Content
# =================================================================================
def render_main_content():
    """Main content area with grammar exercises"""
    if not st.session_state.selected_item_key:
        show_welcome()
        return
    
    data = get_current_data()
    if not data:
        st.error("Invalid selection")
        return
    
    item = data[st.session_state.selected_item_key]
    
    # Header section
    st.header(item["name"])
    render_formation_rules(item)
    
    # Progress tracking
    total = len(item["usage_cases"])
    answered = len(st.session_state.answers)
    st.progress(answered / total if total > 0 else 0)
    
    # Question handling
    if st.session_state.review_mode:
        render_review(item)
    elif answered >= total:
        show_completion(item)
    else:
        render_questions(item)

def render_formation_rules(item: dict):
    """Display formation rules"""
    with st.expander("Formation Rules"):
        for rule, desc in item["formation"].items():
            st.markdown(f"**{rule}:** {desc}")

def render_questions(item: dict):
    """Render interactive questions"""
    for i, case in enumerate(item["usage_cases"]):
        if i in st.session_state.submitted_questions:
            continue
            
        q_key = f"q_{st.session_state.selected_item_key}_{i}"
        
        st.markdown(f"**Question {i+1}**")
        answer = st.selectbox(
            case["question"],
            ["Select answer"] + case["choices"],
            key=q_key
        )
        
        if st.button("Submit", key=f"btn_{i}"):
            handle_answer(case, answer, i)

def handle_answer(case: dict, answer: str, index: int):
    """Process user answers"""
    if answer == "Select answer":
        st.warning("Please select an answer")
        return
    
    st.session_state.answers.append(answer)
    st.session_state.submitted_questions.add(index)
    
    if answer == case["correct"]:
        msg = random.choice(st.session_state.randomized_messages)
        st.success(f"Correct! {msg}")
    else:
        st.error(f"Incorrect. The right answer is: {case['correct']}")

# =================================================================================
# 6. Helper Functions
# =================================================================================
def reset_questions():
    """Reset progress while maintaining selection"""
    st.session_state.answers = []
    st.session_state.submitted_questions = set()
    st.session_state.review_mode = False

def get_current_data():
    """Get current grammar data based on selection"""
    if st.session_state.selected_category == GrammarCategory.TENSES:
        return TENSES_DATA
    return CONDITIONALS_DATA

def show_welcome():
    """Initial welcome screen"""
    st.title("Welcome to Grammar Genius!")
    st.markdown("""
    ## Getting Started
    1. Select a grammar category from the sidebar
    2. Choose specific tense/conditional to practice
    3. Answer interactive questions
    4. Earn progress badges!
    """)

def show_completion(item: dict):
    """Completion screen"""
    st.success(f"🎉 Perfect! You've completed all {len(item['usage_cases'])} questions!")
    if st.button("Review Answers"):
        st.session_state.review_mode = True

def render_review(item: dict):
    """Review screen with answers"""
    st.header("Review Mode")
    for i, case in enumerate(item["usage_cases"]):
        user_answer = st.session_state.answers[i]
        correct = user_answer == case["correct"]
        status = "✅" if correct else "❌"
        
        st.markdown(f"""
        **Question {i+1}**: {case['question']}  
        Your answer: {user_answer} {status}  
        Correct answer: {case['correct']}
        """)

# =================================================================================
# 7. Main Execution
# =================================================================================
if __name__ == "__main__":
    init_session_state()
    st.set_page_config(page_title="Grammar Genius", layout="wide")
    render_sidebar()
    render_main_content()
