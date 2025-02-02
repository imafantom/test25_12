import streamlit as st
import random
from enum import Enum

##############################################################################
# 1) PAGE CONFIG
##############################################################################
st.set_page_config(
    page_title="Grammar Genius App",
    layout="wide"
)

##############################################################################
# 2) ENUM FOR GRAMMAR CATEGORIES (If you need them)
##############################################################################
class GrammarCategory(Enum):
    TENSES = "Tenses"
    CONDITIONALS = "Conditionals"

##############################################################################
# 3) SESSION STATE INITIALIZATION
##############################################################################
if "selected_category" not in st.session_state:
    st.session_state.selected_category = GrammarCategory.TENSES  # or just "Tenses"

if "selected_item_key" not in st.session_state:
    st.session_state.selected_item_key = None

if "answers" not in st.session_state:
    st.session_state.answers = []

if "submitted_questions" not in st.session_state:
    st.session_state.submitted_questions = set()

if "review_mode" not in st.session_state:
    st.session_state.review_mode = False

# IMPORTANT: Ensure "randomized_messages" is defined BEFORE we call random.shuffle(...)
if "randomized_messages" not in st.session_state:
    # Provide your motivational messages
    st.session_state["randomized_messages"] = [
        "You're on fire! 🔥",
        "Keep smashing it! 💥",
        "Fantastic answer! Your words are shining brighter now! 🌟",
        "You're a grammar wizard! 🧙‍♂️",
        "Way to go, champ! 🏆",
        # ... etc. ...
    ]

# Now it's safe to shuffle
random.shuffle(st.session_state.randomized_messages)

##############################################################################
# 4) CUSTOM CSS
##############################################################################
st.markdown("""
<style>
/* Main page background black, default text white */
body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBody"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Dark blue sidebar, white text */
[data-testid="stSidebar"] {
    background-color: #013369 !important;
    color: #ffffff !important;
}

/* Headings remain orange (#ff5722) */
h1, h2, h3 {
    color: #ff5722 !important;
    font-family: "Trebuchet MS", sans-serif;
}

/* Tweak the main container spacing if needed */
main > div {
    padding-top: 20px;
}
</style>
""", unsafe_allow_html=True)

##############################################################################
# 5) TENSES AND CONDITIONALS DATA (paste your actual data below)
##############################################################################
# (No changes needed, just ensure you have your usage_cases etc.)

tenses_data = {
    # ...
}
conditionals_data = {
    # ...
}

##############################################################################
# 6) HELPER FUNCTIONS
##############################################################################
def reset_questions():
    """Reset answers, submitted questions, and review mode. Then shuffle messages again if needed."""
    st.session_state.answers = []
    st.session_state.submitted_questions = set()
    st.session_state.review_mode = False
    # Safe to shuffle again
    random.shuffle(st.session_state["randomized_messages"])

def get_current_data():
    if st.session_state.selected_category == GrammarCategory.TENSES:
        if st.session_state.selected_item_key:
            return tenses_data, st.session_state.selected_item_key
        else:
            return None, None
    else:
        if st.session_state.selected_item_key:
            return conditionals_data, st.session_state.selected_item_key
        else:
            return None, None

##############################################################################
# 7) SIDEBAR
##############################################################################
# ... your sidebar code ...

##############################################################################
# 8) SCREENS
##############################################################################
def show_welcome():
    # ...
    st.title("Welcome to the Grammar Genius Game! 🎉✨🎮")
    # ...

def show_review(data_dict, item_key):
    # ...
    # Implementation here

def show_explanation_and_questions():
    # ...
    # Implementation for your multiple-choice logic

##############################################################################
# 9) MAIN
##############################################################################
def main():
    # 1) Possibly render your sidebar here
    # 2) If no item selected, show_welcome(), else show_explanation_and_questions()

if __name__ == "__main__":
    main()
