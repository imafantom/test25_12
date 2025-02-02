import streamlit as st
import random
from enum import Enum

##############################################################################
# PAGE CONFIG - set page title & layout
##############################################################################
st.set_page_config(page_title="Grammar Genius App", layout="wide")

##############################################################################
# ENUM FOR GRAMMAR CATEGORIES
##############################################################################
class GrammarCategory(Enum):
    TENSES = "Tenses"
    CONDITIONALS = "Conditionals"

##############################################################################
# SESSION STATE + RANDOM MESSAGES
##############################################################################
# Ensure reset_questions is declared before usage

def reset_questions():
    """
    Clears answers, clears which questions were submitted, resets review mode,
    and reshuffles motivational messages if they exist.
    """
    st.session_state.answers = []
    st.session_state.submitted_questions = set()
    st.session_state.review_mode = False
    if "randomized_messages" in st.session_state:
        random.shuffle(st.session_state["randomized_messages"])

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
    st.session_state["randomized_messages"] = [
        "You're on fire! 🔥",
        "Keep smashing it! 💥",
        "Fantastic answer! Your words are shining brighter now! 🌟",
        "You're a grammar wizard! 🧙‍♂️",
        "Way to go, champ! 🏆",
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

random.shuffle(st.session_state["randomized_messages"])

##############################################################################
# CUSTOM CSS - Black background, orange headings, dark-blue sidebar
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
# HELPER DATA BUILDERS: 20 Exercises for Tenses & Conditionals
##############################################################################
def build_20_exercises_for_tense(tense_name):
    usage_cases = []
    for i in range(1, 21):
        question_type = "multiple_choice"
        # We'll alternate Affirmative, Negative, Question patterns
        if i % 3 == 1:
            question = f"He ________ {tense_name} tasks each week (#{i})."
            choices = ["does", "do", "doesn't"]
            correct_choice = "does"
            explanation = f"For {tense_name}, 'He' often uses 'does' in present contexts."
        elif i % 3 == 2:
            question = f"They ________ any {tense_name} exercises (#{i})."
            choices = ["do not do", "didn't do", "haven't done"]
            correct_choice = "do not do"
            explanation = f"In {tense_name}, we might use 'do not do' for a simple negative."
        else:
            question = f"________ you apply {tense_name} daily (#{i})?"
            choices = ["Do", "Will", "Have"]
            correct_choice = "Do"
            explanation = f"In {tense_name}, forming questions with 'Do' + subject is standard."

        usage_cases.append({
            "title": f"Case #{i}",
            "context": f"Scenario for {tense_name}, example {i}.",
            "question_type": question_type,
            "question": question,
            "choices": choices,
            "correct_choice": correct_choice,
            "explanation": explanation
        })
    return usage_cases

def build_20_exercises_for_conditional(cond_name):
    usage_cases = []
    for i in range(1, 21):
        question_type = "multiple_choice"
        if i % 3 == 1:
            question = f"If you ________ the {cond_name}, you might succeed (#{i})."
            choices = ["follow", "follows", "following"]
            correct_choice = "follow"
            explanation = f"For {cond_name}, 'if' + present simple => main clause can have 'might'."
        elif i % 3 == 2:
            question = f"If they didn't hurry, they ________ it in {cond_name} (#{i})."
            choices = ["wouldn't get", "won't get", "haven't got"]
            correct_choice = "wouldn't get"
            explanation = f"{cond_name}: 'wouldn't' + base form for negative hypothetical outcomes."
        else:
            question = f"________ you handle {cond_name} conditions if needed (#{i})?"
            choices = ["Would", "Do", "Are"]
            correct_choice = "Would"
            explanation = f"In {cond_name}, 'Would you ...?' is typical for hypothetical questions."

        usage_cases.append({
            "title": f"Case #{i}",
            "context": f"Real-life scenario for {cond_name}, example {i}",
            "question_type": question_type,
            "question": question,
            "choices": choices,
            "correct_choice": correct_choice,
            "explanation": explanation
        })
    return usage_cases

##############################################################################
# TENSES DATA (7 Tenses) with 20 usage cases each
##############################################################################
tenses_data = {
    "1": {
        "name": "Present Simple",
        "formation": {
            "Positive": "Subject + base form",
            "Negative": "Subject + do/does + not + base form",
            "Question": "Do/Does + subject + base form?",
            "Short answer": "Yes, I do / No, I don't"
        },
        "usage_explanation": [
            "General truths, habits, and routines."
        ],
        "usage_cases": build_20_exercises_for_tense("Present Simple"),
        "extra_examples": [
            "I play tennis on Sundays.",
            "He doesn't eat seafood."
        ]
    },
    "2": {
        "name": "Past Simple",
        "formation": {
            "Positive": "Subject + past form",
            "Negative": "Subject + did not + base form",
            "Question": "Did + subject + base form?",
            "Short answer": "Yes, I did / No, I didn't"
        },
        "usage_explanation": [
            "Actions completed at a specific time in the past."
        ],
        "usage_cases": build_20_exercises_for_tense("Past Simple"),
        "extra_examples": [
            "I visited Rome last year.",
            "They didn't like the movie."
        ]
    },
    "3": {
        "name": "Present Continuous",
        "formation": {
            "Positive": "Subject + am/is/are + verb-ing",
            "Negative": "Subject + am/is/are + not + verb-ing",
            "Question": "Am/Is/Are + subject + verb-ing?",
            "Short answer": "Yes, I am / No, I'm not"
        },
        "usage_explanation": [
            "Actions happening right now, temporary situations."
        ],
        "usage_cases": build_20_exercises_for_tense("Present Continuous"),
        "extra_examples": [
            "I am learning Spanish at the moment.",
            "She isn't working this week."
        ]
    },
    "4": {
        "name": "Past Continuous",
        "formation": {
            "Positive": "Subject + was/were + verb-ing",
            "Negative": "Subject + was/were + not + verb-ing",
            "Question": "Was/Were + subject + verb-ing?",
            "Short answer": "Yes, I was / No, I wasn't"
        },
        "usage_explanation": [
            "Actions in progress at a moment in the past, or interrupted actions."
        ],
        "usage_cases": build_20_exercises_for_tense("Past Continuous"),
        "extra_examples": [
            "I was driving when you called.",
            "They weren't sleeping at midnight."
        ]
    },
    "5": {
        "name": "Present Perfect",
        "formation": {
            "Positive": "Subject + have/has + past participle",
            "Negative": "Subject + have/has + not + past participle",
            "Question": "Have/Has + subject + past participle?",
            "Short answer": "Yes, I have / No, I haven't"
        },
        "usage_explanation": [
            "Actions from the past that affect the present or have no specified time."
        ],
        "usage_cases": build_20_exercises_for_tense("Present Perfect"),
        "extra_examples": [
            "I have seen that film twice.",
            "She hasn't finished her project yet."
        ]
    },
    "6": {
        "name": "Future Simple",
        "formation": {
            "Positive": "Subject + will + base form",
            "Negative": "Subject + will + not + base form",
            "Question": "Will + subject + base form?",
            "Short answer": "Yes, I will / No, I won't"
        },
        "usage_explanation": [
            "Spontaneous decisions, predictions, offers, promises."
        ],
        "usage_cases": build_20_exercises_for_tense("Future Simple"),
        "extra_examples": [
            "We will travel next month.",
            "He won't agree to that idea."
        ]
    },
    "7": {
        "name": "Future Continuous",
        "formation": {
            "Positive": "Subject + will be + verb-ing",
            "Negative": "Subject + will + not + be + verb-ing",
            "Question": "Will + subject + be + verb-ing?",
            "Short answer": "Yes, I will / No, I won't"
        },
        "usage_explanation": [
            "Actions that will be ongoing at a certain time in the future."
        ],
        "usage_cases": build_20_exercises_for_tense("Future Continuous"),
        "extra_examples": [
            "I will be waiting for you at noon.",
            "They won't be working on Sunday."
        ]
    }
}

##############################################################################
# 5 CONDITIONALS: Zero, First, Second, Third, Mixed (each 20 usage cases)
##############################################################################
conditionals_data = {
    "0": {
        "name": "Zero Conditional",
        "formation": {
            "Positive": "If + present simple, present simple",
            "Negative": "If + present simple, present simple (negative)",
            "Question": "Do/Does + subject + base form?",
            "Short answer": "N/A"
        },
        "usage_explanation": [
            "Facts always true under certain conditions.",
            "General truths or cause-and-effect."
        ],
        "usage_cases": build_20_exercises_for_conditional("Zero Conditional"),
        "extra_examples": [
            "If you heat water, it boils.",
            "If you leave ice in the sun, it melts."
        ]
    },
    "1": {
        "name": "First Conditional",
        "formation": {
            "Positive": "If + present simple, will + base form",
            "Negative": "If + present simple, will + not + base form",
            "Question": "Will + subject + base form?",
            "Short answer": "Yes, I will / No, I won't"
        },
        "usage_explanation": [
            "Real or likely future situations.",
            "Cause-effect in the future."
        ],
        "usage_cases": build_20_exercises_for_conditional("First Conditional"),
        "extra_examples": [
            "If it rains, I'll take an umbrella.",
            "If we don't hurry, we'll miss the bus."
        ]
    },
    "2": {
        "name": "Second Conditional",
        "formation": {
            "Positive": "If + past simple, would + base form",
            "Negative": "If + past simple, would + not + base form",
            "Question": "Would + subject + base form?",
            "Short answer": "Yes, I would / No, I wouldn't"
        },
        "usage_explanation": [
            "Unreal/imaginary situations in the present/future.",
            "Hypothetical or unlikely scenarios."
        ],
        "usage_cases": build_20_exercises_for_conditional("Second Conditional"),
        "extra_examples": [
            "If I had a car, I would drive to the beach.",
            "She would help if she were here."
        ]
    },
    "3": {
        "name": "Third Conditional",
        "formation": {
            "Positive": "If + past perfect, would + have + past participle",
            "Negative": "If + past perfect, would + not + have + past participle",
            "Question": "Would + subject + have + past participle?",
            "Short answer": "Yes, I would've / No, I wouldn't have"
        },
        "usage_explanation": [
            "Past situations that didn't happen, imagining different outcomes."
        ],
        "usage_cases": build_20_exercises_for_conditional("Third Conditional"),
        "extra_examples": [
            "If I had known, I would've arrived earlier.",
            "We wouldn't have missed the show if we had left on time."
        ]
    },
    "4": {
        "name": "Mixed Conditional",
        "formation": {
            "Positive": "If + past perfect, would + base form",
            "Negative": "If + past perfect, would + not + base form",
            "Question": "Would + subject + base form? (if-clause in past perfect)",
            "Short answer": "Yes, I would / No, I wouldn't"
        },
        "usage_explanation": [
            "Combines a past hypothetical with a present/future result."
        ],
        "usage_cases": build_20_exercises_for_conditional("Mixed Conditional"),
        "extra_examples": [
            "If I had studied medicine, I'd be a doctor now.",
            "If he had left on time, he wouldn't be stuck in traffic right now."
        ]
    }
}

##############################################################################
# HELPER: get_current_data()
##############################################################################
def get_current_data():
    """Returns (data_dict, item_key) for whichever Tense/Conditional is chosen."""
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
# SIDEBAR CODE
##############################################################################
st.sidebar.title("Grammar Categories")

cat_choice = st.sidebar.radio("Select a category:", [GrammarCategory.TENSES.value, GrammarCategory.CONDITIONALS.value])
if cat_choice == GrammarCategory.TENSES.value:
    st.session_state.selected_category = GrammarCategory.TENSES
else:
    st.session_state.selected_category = GrammarCategory.CONDITIONALS

if st.session_state.selected_category == GrammarCategory.TENSES:
    st.sidebar.subheader("Select a Tense")
    tense_opts = ["Select a tense..."] + [f"{k}. {tenses_data[k]['name']}" for k in tenses_data]
    chosen_tense = st.sidebar.selectbox("Choose a tense:", tense_opts)
    if chosen_tense != "Select a tense...":
        key_str = chosen_tense.split('.')[0].strip()
        if key_str != st.session_state.selected_item_key:
            st.session_state.selected_item_key = key_str
            reset_questions()
    else:
        st.session_state.selected_item_key = None
        reset_questions()
else:
    st.sidebar.subheader("Select a Conditional")
    cond_opts = ["Select a conditional..."] + [f"{k}. {conditionals_data[k]['name']}" for k in conditionals_data]
    chosen_cond = st.sidebar.selectbox("Choose a conditional:", cond_opts)
    if chosen_cond != "Select a conditional...":
        key_str = chosen_cond.split('.')[0].strip()
        if key_str != st.session_state.selected_item_key:
            st.session_state.selected_item_key = key_str
            reset_questions()
    else:
        st.session_state.selected_item_key = None
        reset_questions()

##############################################################################
# SCREENS
##############################################################################
def show_welcome():
    st.title("Welcome to the Grammar Genius Game! 🎉✨🎮")
    st.write("""
    Get ready to boost your English grammar skills in a fun and interactive way!
    
    1. Use the sidebar to choose Tenses or Conditionals.
    2. Select which Tense/Conditional you want to practice.
    3. Each item has 20 multiple-choice exercises, including negative & question forms.
    4. Answer them all to unlock a special 'Expert!' badge!
    5. You can also review your answers afterward.
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
    st.write("Great job! Feel free to pick another item from the sidebar if you wish.")

def show_explanation_and_questions():
    data_dict, item_key = get_current_data()
    if not data_dict or not item_key:
        return

    info = data_dict[item_key]

    st.header(info["name"])
    st.subheader("How is it formed?")
    for form_type, form_rule in info["formation"].items():
        st.markdown(f"**{form_type}:** {form_rule}")

    st.subheader("When do we use it?")
    for usage in info["usage_explanation"]:
        st.write("- " + usage)

    with st.expander("More Examples"):
        if "extra_examples" in info:
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

    # If all answered, user gets a badge
    if answered_count == total_questions:
        st.success(f"You've completed all {total_questions} exercises for {info['name']}!")
        st.markdown(f"**Badge Unlocked:** *{info['name']} Expert!* 🏆")
        if st.button("Review Your Answers"):
            st.session_state.review_mode = True
        return

    # Display each usage case
    for i, case in enumerate(usage_cases):
        answer_key = f"answer_{item_key}_{i}"
        submit_key = f"submit_{item_key}_{i}"

        # If already answered
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

        choices = case.get("choices", [])
        correct_choice = case.get("correct_choice", "")
        explanation = case.get("explanation", "")

        st.session_state.setdefault(answer_key, "")
        user_answer = st.selectbox("Select your answer:", ["-- Select --"] + choices, key=answer_key)

        if st.button("Submit", key=submit_key):
            st.session_state.answers.append(user_answer)
            st.session_state.submitted_questions.add(submit_key)

            # Determine motivational message
            msg_index = len(st.session_state.answers) - 1
            if msg_index < len(st.session_state["randomized_messages"]):
                msg = st.session_state["randomized_messages"][msg_index]
            else:
                msg = st.session_state["randomized_messages"][-1]

            if user_answer == "-- Select --":
                st.warning("You haven't selected an option yet.")
                st.session_state.answers.pop()
                st.session_state.submitted_questions.discard(submit_key)
                st.stop()
            elif user_answer == correct_choice:
                st.success("Correct! " + msg)
                if explanation:
                    st.info(f"Explanation: {explanation}")
            else:
                st.warning("Incorrect. Try again?")
                st.session_state.answers.pop()
                st.session_state.submitted_questions.discard(submit_key)
                st.stop()

            st.write(f"Your answer: {user_answer}")

##############################################################################
# MAIN EXECUTION
##############################################################################
def main():
    # If no item is selected, show welcome
    if st.session_state.selected_item_key is None:
        show_welcome()
    else:
        show_explanation_and_questions()

if __name__ == "__main__":
    main()
