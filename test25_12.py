import streamlit as st
import random
from enum import Enum

##############################################################################
# 1) PAGE CONFIG -- No 'theme' parameter to avoid TypeError on older versions
##############################################################################
st.set_page_config(
    page_title="Grammar Genius App",
    layout="wide"
)

##############################################################################
# 2) ENUM FOR GRAMMAR CATEGORIES
##############################################################################
class GrammarCategory(Enum):
    TENSES = "Tenses"
    CONDITIONALS = "Conditionals"

##############################################################################
# 3) SESSION STATE INITIALIZATION
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
        "font_size": "20px"  # default; will be replaced dynamically
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
# 5) SAMPLE TENSES AND CONDITIONALS DATA
#    (For full deployment, replace these with 20 usage cases each)
##############################################################################
def sample_tenses_data():
    return {
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
                "Used for general or always true facts.",
                "Describes habitual actions and routines."
            ],
            "usage_cases": [
                {
                    "title": "Habit Exercise (1)",
                    "context": "Imagine your weekly routine.",
                    "question_type": "multiple_choice",
                    "question": "He ________ English every week.",
                    "choices": ["study", "studies", "studys"],
                    "correct_choice": "studies",
                    "explanation": "For third-person singular, add 's' to the base form."
                },
                {
                    "title": "Fact Exercise (2)",
                    "context": "Think about a scientific fact.",
                    "question_type": "multiple_choice",
                    "question": "Water ________ at 100°C.",
                    "choices": ["boil", "boils", "boiled"],
                    "correct_choice": "boils",
                    "explanation": "Since water is singular, use 'boils' in Present Simple."
                },
                {
                    "title": "Negative Sentence (3)",
                    "context": "Form a negative statement about routine.",
                    "question_type": "multiple_choice",
                    "question": "She ________ coffee in the morning.",
                    "choices": ["don't drink", "doesn't drink", "not drink"],
                    "correct_choice": "doesn't drink",
                    "explanation": "For third-person singular negatives, use 'doesn't' + base form."
                }
                # ... (extend up to 20 usage cases) ...
            ],
            "extra_examples": [
                "I always wake up at 7 AM.",
                "He never drinks coffee.",
                "They usually go for a walk in the evening."
            ]
        },
        # ... Define 6 more tenses similarly ...
    }

def sample_conditionals_data():
    return {
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
                "Expresses facts that are always true under certain conditions.",
                "Shows cause and effect in general situations."
            ],
            "usage_cases": [
                {
                    "title": "General Truth (1)",
                    "context": "Everyday cause and effect.",
                    "question_type": "multiple_choice",
                    "question": "If you don't water plants, they ________.",
                    "choices": ["die", "dies", "died"],
                    "correct_choice": "die",
                    "explanation": "Both clauses use the present simple in Zero Conditional."
                },
                {
                    "title": "Scientific Fact (2)",
                    "context": "A typical scientific scenario.",
                    "question_type": "multiple_choice",
                    "question": "If you heat ice, it ________.",
                    "choices": ["melt", "melts", "melted"],
                    "correct_choice": "melts",
                    "explanation": "Zero Conditional: use present simple in both clauses."
                },
                {
                    "title": "Negative Example (3)",
                    "context": "Express a negative result.",
                    "question_type": "multiple_choice",
                    "question": "If you don't exercise, you ________ healthy.",
                    "choices": ["are not", "aren't", "isn't"],
                    "correct_choice": "aren't",
                    "explanation": "For 'you' in present simple, the negative contraction is 'aren't.'"
                }
                # ... (extend up to 20 usage cases) ...
            ],
            "extra_examples": [
                "If you freeze water, it becomes ice.",
                "If you press Ctrl+S, your work is saved."
            ]
        },
        # ... Define 4 more conditionals similarly ...
    }

# For demonstration, we use sample data:
tenses_data = sample_tenses_data()
conditionals_data = sample_conditionals_data()

##############################################################################
# 6) HELPER FUNCTIONS
##############################################################################
def reset_questions():
    """Clear answers, submitted questions, reset review mode, and reshuffle messages."""
    st.session_state.answers = []
    st.session_state.submitted_questions = set()
    st.session_state.review_mode = False
    random.shuffle(st.session_state.randomized_messages)

def get_current_data():
    """Return the correct data dictionary and item key based on the selected category."""
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
# 7) SIDEBAR RENDERING
##############################################################################
def render_grammar_item_selector():
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
    """Render the sidebar with improved category, theme, and font size controls."""
    with st.sidebar:
        st.title("Grammar Navigator")
        
        # 1. Category Selection
        cat_value = st.radio(
            "Grammar Category:",
            options=[c.value for c in GrammarCategory],
            index=0,
            key="category_selector"
        )
        st.session_state.selected_category = GrammarCategory(cat_value)
        
        # 2. Grammar Item Selector
        render_grammar_item_selector()
        
        # 3. Theme Selection
        theme = st.radio("Color Theme:", options=list(THEMES.keys()), index=0)
        
        # 4. Font Size Selection
        font_size = st.radio("Font Size:", ["Small", "Medium", "Large"], index=1)
        font_map = {"Small": "16px", "Medium": "20px", "Large": "24px"}
        THEMES[theme]["font_size"] = font_map.get(font_size, "20px")
        
        # Inject dynamic CSS
        st.markdown(CSS_TEMPLATE.format(**THEMES[theme]), unsafe_allow_html=True)

##############################################################################
# 8) SCREENS
##############################################################################
def show_welcome():
    st.title("Welcome to the Grammar Genius Game! 🎉✨🎮")
    st.write("""
    Get ready to boost your English grammar skills in a fun and interactive way!
    
    1. Use the sidebar to choose either Tenses or Conditionals.
    2. Select which Tense/Conditional you want to practice.
    3. Each item contains multiple exercises (20 recommended per item).
    4. Answer the exercises and receive immediate feedback with explanations.
    5. Earn a special badge upon completion!
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
    st.write("Great job! Feel free to choose another grammar item from the sidebar.")

def show_explanation_and_questions():
    data_dict, item_key = get_current_data()
    if not data_dict or not item_key:
        return

    info = data_dict[item_key]

    # Show illustration if available
    if "illustration_url" in info and info["illustration_url"]:
        st.image(info["illustration_url"], width=220)

    st.header(info["name"])
    st.subheader("How is it formed?")
    for form_type, form_rule in info["formation"].items():
        st.markdown(f"**{form_type}:** {form_rule}")

    st.subheader("When do we use it?")
    for usage in info["usage_explanation"]:
        st.write("- " + usage)

    if "extra_examples" in info and info["extra_examples"]:
        with st.expander("More Examples"):
            for ex in info["extra_examples"]:
                st.write("- " + ex)

    usage_cases = info["usage_cases"]
    total_questions = len(usage_cases)
    answered_count = len(st.session_state.answers)

    if st.session_state.review_mode:
        show_review(data_dict, item_key)
        return

    st.write("### Practice Exercises")
    colA, colB = st.columns(2)
    colA.metric("Exercises Answered", f"{answered_count}")
    colB.metric("Total Exercises", f"{total_questions}")

    progress_val = int((answered_count / total_questions) * 100)
    st.progress(progress_val)

    if answered_count == total_questions:
        st.success(f"You've completed all {total_questions} exercises for {info['name']}!")
        st.markdown(f"**Badge Unlocked:** *{info['name']} Expert!* 🏆")
        if st.button("Review Your Answers"):
            st.session_state.review_mode = True
        return

    # Display each exercise
    for i, case in enumerate(usage_cases):
        answer_key = f"answer_{item_key}_{i}"
        submit_key = f"submit_{item_key}_{i}"
        question_type = case.get("question_type", "open_ended")
        
        if submit_key in st.session_state.submitted_questions:
            st.write(f"**{case['title']}**")
            if "context" in case:
                st.write(f"Context: {case['context']}")
            st.write(case["question"])
            user_answer = st.session_state.get(answer_key, "")
            st.write(f"Your answer: {user_answer}")
            continue

        st.write(f"**{case['title']}**")
        if "context" in case:
            st.write(f"Context: {case['context']}")
        st.write(case["question"])

        if question_type == "multiple_choice":
            choices = case.get("choices", [])
            correct_choice = case.get("correct_choice", None)
            explanation = case.get("explanation", "")
            st.session_state.setdefault(answer_key, "")
            user_answer = st.selectbox("Select your answer:", ["-- Select --"] + choices, key=answer_key)
        else:
            user_answer = st.text_input("Your answer:", key=answer_key)

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
            elif question_type == "multiple_choice":
                if correct_choice and user_answer == correct_choice:
                    st.success("Correct! " + msg)
                    if explanation:
                        st.info(f"Explanation: {explanation}")
                else:
                    st.warning("Incorrect. Try again?")
                    st.session_state.answers.pop()
                    st.session_state.submitted_questions.remove(submit_key)
                    st.stop()
            else:
                if msg and msg[0].isupper():
                    new_msg = f"{msg[0].lower() + msg[1:]}"
                else:
                    new_msg = msg
                st.success(new_msg)

            st.write(f"Your answer: {user_answer}")

##############################################################################
# 9) MAIN FUNCTION
##############################################################################
def main():
    render_sidebar()
    if st.session_state.selected_item_key is None:
        show_welcome()
    else:
        show_explanation_and_questions()

if __name__ == "__main__":
    main()

