import streamlit as st
import random
from dataclasses import dataclass
from enum import Enum
from typing import Literal, Dict, Any
from functools import lru_cache

# =================================================================================
# 1. DATA STRUCTURES AND ENUMS
# =================================================================================
class GrammarCategory(Enum):
    TENSES = "Tenses"
    CONDITIONALS = "Conditionals"

@dataclass
class GrammarItem:
    name: str
    formation: Dict[str, str]
    usage_explanation: list[str]
    usage_cases: list[Dict[str, str]]
    extra_examples: list[str]

@dataclass
class AppState:
    selected_category: GrammarCategory
    selected_item_key: str | None
    answers: list[str]
    submitted_questions: set[str]
    review_mode: bool
    randomized_messages: list[str]
    current_progress: int = 0

# =================================================================================
# 2. DATA LOADING (Separate JSON files recommended for production)
# =================================================================================
@lru_cache(maxsize=2)
def load_grammar_data(category: Literal["tenses", "conditionals"]) -> Dict[str, Any]:
    """Mock data loader - replace with actual JSON loading in production"""
    # Sample data structure - keep similar to original but more type-safe
    return {
        "1": GrammarItem(
            name="Present Simple",
            formation={
                "Positive": "Subject + base form",
                "Negative": "Subject + do not/does not + base form",
                "Question": "Do/Does + subject + base form?",
                "Short answer": "'Yes, I do.' / 'No, I don't.'"
            },
            usage_explanation=["General truths", "Habits"],
            usage_cases=[{"title": "Facts", "question": "Does water boil at 100°C?"}],
            extra_examples=["I eat breakfast daily."]
        )
    }

# =================================================================================
# 3. THEME MANAGEMENT
# =================================================================================
CSS_TEMPLATE = """
<style>
:root {{
    --primary-color: {primary};
    --secondary-color: {secondary};
    --text-color: {text};
    --background-color: {background};
    --border-color: {border};
}}

[data-testid="stAppViewContainer"] {{
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
}}

[data-testid="stSidebar"] {{
    background-color: var(--secondary-color) !important;
}}

h1, h2, h3 {{
    color: var(--primary-color) !important;
    font-family: 'Trebuchet MS', sans-serif;
}}

.stTextInput>div>div>input {{
    color: var(--text-color) !important;
    background-color: var(--background-color) !important;
    border-color: var(--border-color) !important;
}}
</style>
"""

THEMES = {
    "Dark": {
        "primary": "#ff5722",
        "secondary": "#013369",
        "text": "#ffffff",
        "background": "#000000",
        "border": "#555555"
    },
    "Light": {
        "primary": "#ff5722",
        "secondary": "#f0f0f0",
        "text": "#000000",
        "background": "#ffffff",
        "border": "#cccccc"
    }
}

# =================================================================================
# 4. STATE MANAGEMENT
# =================================================================================
def initialize_session_state():
    """Initialize all required session state variables"""
    defaults = AppState(
        selected_category=GrammarCategory.TENSES,
        selected_item_key=None,
        answers=[],
        submitted_questions=set(),
        review_mode=False,
        randomized_messages=[],
    )
    
    for field in defaults.__dataclass_fields__:
        if field not in st.session_state:
            setattr(st.session_state, field, getattr(defaults, field))
    
    if not st.session_state.randomized_messages:
        reset_motivational_messages()

def reset_motivational_messages():
    """Shuffle motivational messages ensuring unique order"""
    messages = [
        "You're on fire! 🔥", 
        "Keep smashing it! 💥",
        # ... (keep your original messages list)
    ]
    random.shuffle(messages)
    st.session_state.randomized_messages = messages

def reset_questions():
    """Reset progress while maintaining category selection"""
    st.session_state.answers = []
    st.session_state.submitted_questions = set()
    st.session_state.review_mode = False
    if len(st.session_state.answers) >= len(st.session_state.randomized_messages):
        reset_motivational_messages()

# =================================================================================
# 5. UI COMPONENTS
# =================================================================================
def render_sidebar():
    """Render the sidebar with category and theme controls"""
    with st.sidebar:
        st.title("Grammar Navigator")
        
        # Category selection
        category = st.radio(
            "Grammar Category:",
            options=[c.value for c in GrammarCategory],
            index=0,
            key="category_selector"
        )
        st.session_state.selected_category = GrammarCategory(category)
        
        # Item selection
        render_grammar_item_selector()
        
        # Theme selector
        theme = st.radio("Color Theme:", options=list(THEMES.keys()))
        st.markdown(CSS_TEMPLATE.format(**THEMES[theme]), unsafe_allow_html=True)

def render_grammar_item_selector():
    """Render appropriate selector based on current category"""
    data = load_grammar_data("tenses" if st.session_state.selected_category == GrammarCategory.TENSES else "conditionals")
    items = [f"{k}. {v.name}" for k, v in data.items()]
    
    selected = st.selectbox(
        f"Select {st.session_state.selected_category.value[:-1]}:",
        options=["Select..."] + items,
        key="item_selector"
    )
    
    if selected != "Select...":
        key = selected.split(".", 1)[0].strip()
        if key != st.session_state.selected_item_key:
            st.session_state.selected_item_key = key
            reset_questions()

# =================================================================================
# 6. MAIN CONTENT RENDERERS
# =================================================================================
def render_welcome():
    """Initial welcome screen"""
    st.title("Welcome to Grammar Genius! 🎓")
    st.markdown("""
    ## Quick Start Guide
    1. **Choose a category** from the sidebar
    2. **Select specific grammar item** to practice
    3. **Study** the formation rules and examples
    4. **Practice** with interactive questions
    5. **Earn badges** by completing sections!
    """)
    st.image("https://via.placeholder.com/600x200?text=Grammar+Mastery+Journey", use_column_width=True)

def render_grammar_section():
    """Main grammar practice interface"""
    data = load_grammar_data("tenses" if st.session_state.selected_category == GrammarCategory.TENSES else "conditionals")
    item = data.get(st.session_state.selected_item_key)
    
    if not item:
        st.error("Invalid selection - please choose a valid item from the sidebar")
        return
    
    # Header section
    st.header(item.name)
    cols = st.columns([3, 2])
    
    with cols[0]:
        render_formation_rules(item)
    with cols[1]:
        render_progress(item)
    
    render_practice_questions(item)

def render_formation_rules(item: GrammarItem):
    """Display formation rules with expandable examples"""
    st.subheader("Formation Rules")
    for rule, desc in item.formation.items():
        st.markdown(f"**{rule}:** {desc}")
    
    with st.expander("📚 Additional Examples"):
        for ex in item.extra_examples:
            st.markdown(f"- `{ex}`")

def render_progress(item: GrammarItem):
    """Show progress metrics and controls"""
    progress = len(st.session_state.answers) / len(item.usage_cases) if item.usage_cases else 0
    st.metric("Completed", f"{len(st.session_state.answers)}/{len(item.usage_cases)}")
    st.progress(min(progress, 1.0))
    
    if st.button("🔄 Reset Progress"):
        reset_questions()

# =================================================================================
# 7. CORE FUNCTIONALITY
# =================================================================================
def main():
    initialize_session_state()
    
    if not st.session_state.selected_item_key:
        render_welcome()
    else:
        render_grammar_section()

if __name__ == "__main__":
    main()
