import streamlit as st
import random
from enum import Enum

##############################################################################
# 1) PAGE CONFIG -- no 'theme' param to avoid older Streamlit TypeError
##############################################################################
st.set_page_config(page_title="Grammar Genius App", layout="wide")

##############################################################################
# 2) ENUM FOR GRAMMAR CATEGORIES
##############################################################################
class GrammarCategory(Enum):
    TENSES = "Tenses"
    CONDITIONALS = "Conditionals"

##############################################################################
# 3) SESSION STATE
##############################################################################
if "selected_category" not in st.session_state:
    st.session_state.selected_category = GrammarCategory.TENSES
if "selected_item_key" not in st.session_state:
    st.session_state.selected_item_key = None
if "answers" not in st.session_state:
    st.session_state.answers = []
if "submitted_questions" not in st.session_state:
    st.session_state.submitted_questions = set()
if "review_mode" not in st.session_state:
    st.session_state.review_mode = False
if "randomized_messages" not in st.session_state:
    motivational_sentences = [
        "You're on fire! 🔥",
        "Keep smashing it! 💥",
        "Fantastic answer! Your words are shining brighter now! 🌟",
        "You're a grammar wizard! Conjugations bend to your will! 🧙‍♂️",
        "Way to go, champ! That sentence just leapt off the page! 🏆",
        "Bravo! That's the spirit! Your linguistic muscles are flexing! 👏",
        "Grammar genius at work! Your sentences sparkle like diamonds! 🧠",
        "Outstanding! The grammar gods are smiling upon you now! 🥳",
        "You're unstoppable! The universe is taking notes from your syntax! 🚀",
        "Wonderful! Each answer you give writes poetry in the sky! 🎩✨",
        "You're dazzling! These sentences are lining up to be in your presence! ✨🌈",
        "Impressive! Your answers radiate confidence and linguistic flair! 💎💃",
        "Marvelous! The grammar galaxy bows before your might! 🌌🏅",
        "Astonishing! Every verb you conjure becomes a masterpiece! 🎉📚",
        "Magnificent! Even dictionaries blush at your command of words! 🦄📖",
        "Incredible! Grammarians form fan clubs in your honor! 🎶💫",
        "Stupendous! Your verb forms could charm the toughest critics! 🍀💬",
        "Glorious! Your tense usage now inspires entire textbooks! 🦋🔥",
        "Remarkable! Each reply is like a linguistic symphony in action! 🎼🌍",
        "Spectacular! Your English prowess bursts forth like cosmic fireworks! 💥🚀🎉"
    ]
    random.shuffle(motivational_sentences)
    st.session_state.randomized_messages = motivational_sentences

##############################################################################
# 4) THEMES & CSS TEMPLATE
##############################################################################
THEMES = {
    "Dark": {
        "main_bg": "#000000",
        "main_color": "#ffffff",
        "sidebar_bg": "#013369",
        "sidebar_color": "#ffffff",
        "heading_color": "#ff5722",
        "font_size": "20px"
    },
    "Light": {
        "main_bg": "#ffffff",
        "main_color": "#000000",
        "sidebar_bg": "#f0f0f0",
        "sidebar_color": "#000000",
        "heading_color": "#ff5722",
        "font_size": "20px"
    }
}

CSS_TEMPLATE = """
<style>
:root, html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBody"],
[data-testid="stMarkdownContainer"],
.stMarkdown, [class^="css-"],
[data-testid="stHeader"],
[data-testid="stSidebar"],
.css-1oe6wy4, .block-container,
.stRadio, .stSelectbox, .stTextInput, .stCheckbox,
.stRadio > div, .stSelectbox > div, .stTextInput > div, .stCheckbox > div {
    background-color: {main_bg} !important;
    color: {main_color} !important;
    font-size: {font_size} !important;
    border: none !important;
}

h1, h2, h3 {
    color: {heading_color} !important;
    font-family: "Trebuchet MS", sans-serif;
    font-size: calc({font_size} * 1.25) !important;
}

[data-testid="stSidebar"] {
    background-color: {sidebar_bg} !important;
    color: {sidebar_color} !important;
    font-size: {font_size} !important;
}
[data-testid="stSidebar"] * {
    color: {sidebar_color} !important;
    font-size: {font_size} !important;
    background: transparent !important;
}

main > div {
    padding-top: 20px;
}
</style>
"""

##############################################################################
# 5) TENSES AND CONDITIONALS DATA
#    REPLACE WITH YOUR OWN 20 USAGE CASES PER TENSE/CONDITIONAL IF NEEDED
##############################################################################
tenses_data = {
    "1": {
        "name": "Present Simple",
        "illustration_url": "https://example.com/present_simple_illus.png",
        "formation": {
            "Positive": "Subject + base form (e.g., 'I eat')",
            "Negative": "Subject + do not/does not + base form (e.g., 'I do not eat')",
            "Question": "Do/Does + subject + base form? (e.g., 'Do you eat?')",
            "Short answer": "'Yes, I do.' / 'No, I don't.'"
        },
        "usage_explanation": [
            "General or always true facts.",
            "Situations that are more or less permanent.",
            "Habits or routines."
        ],
        "usage_cases": [
            {
                "title": "Habits (1)",
                "context": "Think of a daily activity.",
                "question_type": "multiple_choice",
                "question": "He ________ English every week.",
                "choices": ["study", "studies", "studys"],
                "correct_choice": "studies",
                "explanation": "For he/she/it in Present Simple, we add 's' to the base form."
            },
            {
                "title": "Facts (2)",
                "context": "A scientific or general truth.",
                "question_type": "multiple_choice",
                "question": "Water ________ at 100 degrees Celsius.",
                "choices": ["boil", "boils", "boiles"],
                "correct_choice": "boils",
                "explanation": "In Present Simple, 'water' is singular, so we add 's': water boils."
            },
            {
                "title": "Routines (3)",
                "context": "A daily morning routine scenario.",
                "question_type": "multiple_choice",
                "question": "I ________ breakfast at 7 AM every day.",
                "choices": ["have", "haves", "am having"],
                "correct_choice": "have",
                "explanation": "For 'I' in Present Simple, we use the base form: have."
            }
            # ... up to 20 ...
        ],
        "extra_examples": [
            "I always wake up at 7 AM.",
            "He never drinks coffee.",
            "They usually watch TV in the evening."
        ]
    },
    # ... 6 more tenses ...
}

conditionals_data = {
    "0": {
        "name": "Zero Conditional",
        "illustration_url": "https://example.com/zero_cond_illus.png",
        "formation": {
            "Positive": "If + present simple, present simple",
            "Negative": "If + present simple, present simple (negative)",
            "Question": "Do/Does + subject + base form in each clause",
            "Short answer": "N/A"
        },
        "usage_explanation": [
            "Facts always true under certain conditions.",
            "General truths or cause-and-effect relationships."
        ],
        "usage_cases": [
            {
                "title": "General truths (1)",
                "context": "Everyday cause-and-effect scenario.",
                "question_type": "multiple_choice",
                "question": "If you don't water plants, they ________.",
                "choices": ["die", "dies", "dying"],
                "correct_choice": "die",
                "explanation": "Zero conditional uses present simple in both clauses: If you don't water plants, they die."
            },
            {
                "title": "Scientific facts (2)",
                "context": "A typical scientific scenario.",
                "question_type": "multiple_choice",
                "question": "If you heat ice, it ________.",
                "choices": ["melt", "melts", "melted"],
                "correct_choice": "melts",
                "explanation": "For zero conditional: If you heat ice, it melts."
            }
            # ... up to 20 ...
        ],
        "extra_examples": [
            "If you freeze water, it becomes ice.",
            "If you press Ctrl+S, most programs save your work."
        ]
    },
    # ... 4 more conditionals ...
}

##############################################################################
# 6) RESET FUNCTION - ensures no NameError
##############################################################################
def reset_questions():
    """Clear answers, reset usage case submission states, shuffle messages."""
    st.session_state.answers = []
    st.session_state.submitted_questions = set()
    st.session_state.review_mode = False
    if "randomized_messages" in st.session_state:
        random.shuffle(st.session_state.randomized_messages)

##############################################################################
# 7) SIDEBAR RENDERING
##############################################################################
def render_grammar_item_selector():
    """Show a sub-selector for Tenses or Conditionals depending on chosen category."""
    if st.session_state.selected_category == GrammarCategory.TENSES:
        st.subheader("Select a Tense")
        all_tenses = ["Select a tense..."] + [f"{k}. {tenses_data[k]['name']}" for k in tenses_data]
        chosen_tense = st.selectbox("Which tense?", all_tenses)
        if chosen_tense != "Select a tense...":
            key_str = chosen_tense.split('.')[0].strip()
            if key_str != st.session_state.selected_item_key:
                st.session_state.selected_item_key = key_str
                reset_questions()
        else:
            st.session_state.selected_item_key = None
            reset_questions()
    else:
        st.subheader("Select a Conditional")
        all_conds = ["Select a conditional..."] + [f"{k}. {conditionals_data[k]['name']}" for k in conditionals_data]
        chosen_cond = st.selectbox("Which conditional?", all_conds)
        if chosen_cond != "Select a conditional...":
            key_str = chosen_cond.split('.')[0].strip()
            if key_str != st.session_state.selected_item_key:
                st.session_state.selected_item_key = key_str
                reset_questions()
        else:
            st.session_state.selected_item_key = None
            reset_questions()

def render_sidebar():
    """Render the sidebar with improved category & theme controls."""
    with st.sidebar:
        st.title("Grammar Navigator")
        
        # Category selection
        cat_value = st.radio(
            "Grammar Category:",
            options=[c.value for c in GrammarCategory],  # ["Tenses", "Conditionals"]
            index=0,
            key="category_selector"
        )
        st.session_state.selected_category = GrammarCategory(cat_value)
        
        # Grammar item selector
        render_grammar_item_selector()
        
        # Theme selection
        theme = st.radio("Color Theme:", options=list(THEMES.keys()), index=0)
        # Font size
        font_size = st.radio("Font Size:", ["Small", "Medium", "Large"], index=1)
        
        # Fill in the CSS template
        css = CSS_TEMPLATE.format(**THEMES[theme])
        # Adjust font size
        font_map = {"Small":"16px","Medium":"20px","Large":"24px"}
        chosen_size = font_map.get(font_size,"20px")
        final_css = css.replace("{font_size}", chosen_size)
        st.markdown(final_css, unsafe_allow_html=True)

##############################################################################
# 8) SCREENS
##############################################################################
def show_welcome():
    st.title("Welcome to the Grammar Genius Game! 🎉✨🎮")
    st.write("""
    Get ready to boost your English grammar skills in a fun and interactive way!
    
    1. Use the sidebar to choose either Tenses or Conditionals.
    2. Select which Tense/Conditional you want to practice.
    3. Each tense/conditional has multiple exercises (20 recommended).
    4. After answering all exercises, you'll earn a special badge!
    """)

def show_review(data_dict, item_key):
    st.header("Review Your Answers")
    usage_cases = data_dict[item_key]["usage_cases"]
    for i, case in enumerate(usage_cases):
        st.write(f"**{case['title']}**")
        if "question" in case:
            st.write(f"Question: {case['question']}")
        user_answer = st.session_state.get(f"answer_{item_key}_{i}", "")
        st.write(f"Your answer: {user_answer} 🏆")
    st.write("Feel free to pick another grammar item from the sidebar if you want.")

def show_explanation_and_questions():
    """Practice screen for the chosen Tense or Conditional."""
    if st.session_state.selected_category == GrammarCategory.TENSES:
        data_dict = tenses_data
    else:
        data_dict = conditionals_data

    item_key = st.session_state.selected_item_key
    if not item_key:
        return

    info = data_dict[item_key]
    # Thematic illustration
    if "illustration_url" in info and info["illustration_url"]:
        st.image(info["illustration_url"], width=220)

    st.header(info["name"])
    st.subheader("How is it formed?")
    for form_type, form_rule in info["formation"].items():
        st.markdown(f"**{form_type}:** {form_rule}")

    st.subheader("When do we use it?")
    for usage in info["usage_explanation"]:
        st.write("- " + usage)

    if "extra_examples" in info:
        with st.expander("More Examples"):
            for ex in info["extra_examples"]:
                st.write("- " + ex)

    usage_cases = info["usage_cases"]
    total_questions = len(usage_cases)
    answered_count = len(st.session_state.answers)

    if st.session_state.review_mode:
        show_review(data_dict, item_key)
        return

    st.write("### Practice Exercises (Multiple-Choice)")
    colA, colB = st.columns(2)
    colA.metric("Questions Answered", f"{answered_count}")
    colB.metric("Total Questions", f"{total_questions}")

    progress_val = int((answered_count / total_questions) * 100)
    st.progress(progress_val)

    if answered_count == total_questions:
        st.success(f"You've answered all {total_questions} questions for {info['name']}!")
        st.markdown(f"**Badge Unlocked:** *{info['name']} Expert!* 🏆")

        if st.button("Review Your Answers"):
            st.session_state.review_mode = True
        return

    # Exercises
    for i, case in enumerate(usage_cases):
        answer_key = f"answer_{item_key}_{i}"
        submit_key = f"submit_{item_key}_{i}"

        if submit_key in st.session_state.submitted_questions:
            st.write(f"**{case['title']}**")
            if "context" in case:
                st.write(f"Context: {case['context']}")
            st.write(case["question"])
            user_answer = st.session_state.get(answer_key, "")
            st.write(f"Your answer: {user_answer}")
            continue

        # Show question
        st.write(f"**{case['title']}**")
        if "context" in case:
            st.write(f"Context: {case['context']}")
        st.write(case["question"])

        choices = case.get("choices", [])
        correct_choice = case.get("correct_choice", None)
        explanation = case.get("explanation", "")

        # Build the multiple-choice selectbox
        st.session_state.setdefault(answer_key, "")
        user_answer = st.selectbox(
            "Select your answer:",
            ["-- Select --"] + choices,
            key=answer_key
        )

        if st.button("Submit", key=submit_key):
            st.session_state.answers.append(user_answer)
            st.session_state.submitted_questions.add(submit_key)

            msg_index = len(st.session_state.answers) - 1
            if msg_index < len(st.session_state.randomized_messages):
                msg = st.session_state.randomized_messages[msg_index]
            else:
                msg = st.session_state.randomized_messages[-1]

            if user_answer == "-- Select --":
                st.warning("You haven't selected an option yet.")
                st.session_state.answers.pop()
                st.session_state.submitted_questions.remove(submit_key)
                st.stop()
            elif user_answer == correct_choice:
                st.success("Correct! " + msg)
                if explanation:
                    st.info(f"Explanation: {explanation}")
            else:
                st.warning("Incorrect. Try again?")
                st.session_state.answers.pop()
                st.session_state.submitted_questions.remove(submit_key)
                st.stop()

            st.write(f"Your answer: {user_answer}")

##############################################################################
# 9) MAIN
##############################################################################
def main():
    # 1) Render the improved sidebar first
    render_sidebar()
    # 2) If no item is chosen, show welcome
    if st.session_state.selected_item_key is None:
        show_welcome()
    else:
        # 3) Show explanation + multiple choice exercises
        show_explanation_and_questions()

if __name__ == "__main__":
    main()
