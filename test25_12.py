import streamlit as st
import random
from enum import Enum

##############################################################################
# 1) PAGE CONFIG: No 'theme' param to avoid older Streamlit issues
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

# Ensure randomized_messages is defined before shuffling
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
# 4) CUSTOM CSS: Dark background, orange headings, dark-blue sidebar
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
# 5) MASSIVE TENSES AND CONDITIONALS DATA
##############################################################################
def build_20_exercises_for_tense(tense_name):
    """
    Returns a list of 20 usage cases for a given tense_name,
    each is a multiple-choice exercise with an explanation.
    We'll vary them slightly: some negative, some questions, etc.
    """
    usage_cases = []
    for i in range(1, 21):
        question_type = "multiple_choice"
        # We'll define different patterns for variety
        if i % 3 == 1:
            # Affirmative pattern
            question = f"He ________ {tense_name} practice each week (#{i})."
            choices = ["does", "do", "doesn't"]
            correct_choice = "does"
            explanation = f"In {tense_name}, 'He' often uses 'does' for emphasis in statements."
        elif i % 3 == 2:
            # Negative pattern
            question = f"They ________ {tense_name} properly yet (#{i})."
            choices = ["haven't done", "didn't do", "don't do"]
            correct_choice = "haven't done"
            explanation = f"Negative forms in {tense_name} can use 'haven't' + participle for certain contexts."
        else:
            # Question pattern
            question = f"________ you handle {tense_name} tasks every day (#{i})?"
            choices = ["Do", "Will", "Have"]
            correct_choice = "Do"
            explanation = f"To form a question in {tense_name}, we often start with 'Do' for a general question."

        usage_cases.append({
            "title": f"Case #{i}",
            "context": f"Practice scenario for {tense_name}, example {i}.",
            "question_type": question_type,
            "question": question,
            "choices": choices,
            "correct_choice": correct_choice,
            "explanation": explanation
        })
    return usage_cases

def build_20_exercises_for_conditional(cond_name):
    """
    Returns 20 usage cases for a given conditional name,
    each is a multiple-choice exercise with an explanation.
    We'll vary them slightly: some negative, some questions, etc.
    """
    usage_cases = []
    for i in range(1, 21):
        question_type = "multiple_choice"
        if i % 3 == 1:
            question = f"If you ________ me, I might finish the {cond_name} earlier (#{i})."
            choices = ["help", "helps", "helped"]
            correct_choice = "help"
            explanation = f"For a {cond_name}, we often use 'if' + present simple, then a modal in the main clause."
        elif i % 3 == 2:
            question = f"If we don't hurry, we ________ the deal in {cond_name} (#{i})."
            choices = ["won't get", "wouldn't get", "haven't got"]
            correct_choice = "won't get"
            explanation = f"Typical future {cond_name} structure uses 'won't' + base form for negative outcomes."
        else:
            question = f"________ they learn quickly if they needed {cond_name} advice (#{i})?"
            choices = ["Would", "Do", "Are"]
            correct_choice = "Would"
            explanation = f"For hypothetical {cond_name}, 'Would' + subject is common in the main clause."

        usage_cases.append({
            "title": f"Case #{i}",
            "context": f"Practice scenario for {cond_name}, example {i}.",
            "question_type": question_type,
            "question": question,
            "choices": choices,
            "correct_choice": correct_choice,
            "explanation": explanation
        })
    return usage_cases

# 7 Tenses: Present Simple, Past Simple, Present Continuous, Past Continuous, Present Perfect, Future Simple, Future Continuous
tenses_data = {
    "1": {
        "name": "Present Simple",
        "formation": {
            "Positive": "Subject + base form",
            "Negative": "Subject + do not/does not + base form",
            "Question": "Do/Does + subject + base form?",
            "Short answer": "'Yes, I do.' / 'No, I don't.'"
        },
        "usage_explanation": [
            "General truths or repeated actions.",
            "Habits or routines."
        ],
        "usage_cases": build_20_exercises_for_tense("Present Simple"),
        "extra_examples": [
            "I play tennis every weekend.",
            "He doesn't like coffee."
        ]
    },
    "2": {
        "name": "Past Simple",
        "formation": {
            "Positive": "Subject + past form",
            "Negative": "Subject + did not + base form",
            "Question": "Did + subject + base form?",
            "Short answer": "'Yes, I did.' / 'No, I didn't.'"
        },
        "usage_explanation": [
            "Completed actions in the past.",
            "Actions at a specific time."
        ],
        "usage_cases": build_20_exercises_for_tense("Past Simple"),
        "extra_examples": [
            "I visited France last year.",
            "They didn't see the movie."
        ]
    },
    "3": {
        "name": "Present Continuous",
        "formation": {
            "Positive": "Subject + am/is/are + verb-ing",
            "Negative": "Subject + am/is/are + not + verb-ing",
            "Question": "Am/Is/Are + subject + verb-ing?",
            "Short answer": "'Yes, I am.' / 'No, I'm not.'"
        },
        "usage_explanation": [
            "Actions happening now.",
            "Temporary situations or changing states."
        ],
        "usage_cases": build_20_exercises_for_tense("Present Continuous"),
        "extra_examples": [
            "I am studying English right now.",
            "She isn't working today."
        ]
    },
    "4": {
        "name": "Past Continuous",
        "formation": {
            "Positive": "Subject + was/were + verb-ing",
            "Negative": "Subject + was/were + not + verb-ing",
            "Question": "Was/Were + subject + verb-ing?",
            "Short answer": "'Yes, I was.' / 'No, I wasn't.'"
        },
        "usage_explanation": [
            "Actions in progress at a moment in the past.",
            "Background actions interrupted by another event."
        ],
        "usage_cases": build_20_exercises_for_tense("Past Continuous"),
        "extra_examples": [
            "They were walking when it started to rain.",
            "I wasn't sleeping at midnight."
        ]
    },
    "5": {
        "name": "Present Perfect",
        "formation": {
            "Positive": "Subject + have/has + past participle",
            "Negative": "Subject + have/has + not + past participle",
            "Question": "Have/Has + subject + past participle?",
            "Short answer": "'Yes, I have.' / 'No, I haven't.'"
        },
        "usage_explanation": [
            "Actions with unspecified time or continuing until now.",
            "Life experiences or events affecting the present."
        ],
        "usage_cases": build_20_exercises_for_tense("Present Perfect"),
        "extra_examples": [
            "I have seen that movie before.",
            "She hasn't finished her homework."
        ]
    },
    "6": {
        "name": "Future Simple",
        "formation": {
            "Positive": "Subject + will + base form",
            "Negative": "Subject + will + not + base form",
            "Question": "Will + subject + base form?",
            "Short answer": "'Yes, I will.' / 'No, I won't.'"
        },
        "usage_explanation": [
            "Spontaneous decisions, predictions, promises/offers.",
            "Future facts or certainties."
        ],
        "usage_cases": build_20_exercises_for_tense("Future Simple"),
        "extra_examples": [
            "We will travel next year.",
            "He won't agree to that plan."
        ]
    },
    "7": {
        "name": "Future Continuous",
        "formation": {
            "Positive": "Subject + will be + verb-ing",
            "Negative": "Subject + will + not + be + verb-ing",
            "Question": "Will + subject + be + verb-ing?",
            "Short answer": "'Yes, I will.' / 'No, I won't.'"
        },
        "usage_explanation": [
            "Actions that will be in progress at a future time.",
            "Polite inquiries about someone's plans."
        ],
        "usage_cases": build_20_exercises_for_tense("Future Continuous"),
        "extra_examples": [
            "They will be waiting for you at 7 PM.",
            "I won't be working tomorrow afternoon."
        ]
    }
}

def build_20_exercises_for_conditional_name(cond_name):
    """
    Helper for building 20 usage cases for each conditional item.
    """
    usage_cases = []
    for i in range(1,21):
        if i % 3 == 1:
            question = f"If you ________ the {cond_name}, you might succeed (#{i})."
            choices = ["fulfill", "fulfills", "fulfilling"]
            correct_choice = "fulfill"
            explanation = f"Typically 'if' + present simple (like 'you fulfill') for {cond_name} scenario."
        elif i % 3 == 2:
            question = f"If they didn't hurry, they ________ the result in {cond_name} (#{i})."
            choices = ["wouldn't get", "won't get", "haven't got"]
            correct_choice = "wouldn't get"
            explanation = f"For hypothetical {cond_name}, 'wouldn't' + base form is common in the main clause."
        else:
            question = f"________ you manage the {cond_name} if you needed help (#{i})?"
            choices = ["Would", "Do", "Have"]
            correct_choice = "Would"
            explanation = f"For hypothetical or uncertain {cond_name}, 'Would' + subject is typical."

        usage_cases.append({
            "title": f"Case #{i}",
            "context": f"Real-life scenario for {cond_name}, example {i}",
            "question_type": "multiple_choice",
            "question": question,
            "choices": choices,
            "correct_choice": correct_choice,
            "explanation": explanation
        })
    return usage_cases

# 5 Conditionals: Zero, First, Second, Third, Mixed
conditionals_data = {
    "0": {
        "name": "Zero Conditional",
        "formation": {
            "Positive": "If + present simple, present simple",
            "Negative": "If + present simple, present simple (negative)",
            "Question": "Do/Does + subject + base form",
            "Short answer": "N/A"
        },
        "usage_explanation": [
            "Facts always true under certain conditions.",
            "General truths or cause-and-effect."
        ],
        "usage_cases": build_20_exercises_for_conditional_name("Zero Conditional"),
        "extra_examples": [
            "If you heat water, it boils.",
            "If you press Ctrl+S, your document is saved."
        ]
    },
    "1": {
        "name": "First Conditional",
        "formation": {
            "Positive": "If + present simple, will + base form",
            "Negative": "If + present simple, will + not + base form",
            "Question": "Will + subject + base form?",
            "Short answer": "Yes, I will. / No, I won't."
        },
        "usage_explanation": [
            "Real or likely future situations.",
            "Cause-and-effect in the future."
        ],
        "usage_cases": build_20_exercises_for_conditional_name("First Conditional"),
        "extra_examples": [
            "If it rains, I will take an umbrella.",
            "If we don't hurry, we'll miss the train."
        ]
    },
    "2": {
        "name": "Second Conditional",
        "formation": {
            "Positive": "If + past simple, would + base form",
            "Negative": "If + past simple, would + not + base form",
            "Question": "Would + subject + base form?",
            "Short answer": "Yes, I would. / No, I wouldn't."
        },
        "usage_explanation": [
            "Unreal or imaginary situations in the present/future.",
            "Hypothetical or unlikely scenarios."
        ],
        "usage_cases": build_20_exercises_for_conditional_name("Second Conditional"),
        "extra_examples": [
            "If I had a car, I would drive to the beach.",
            "If she were here, she'd fix this quickly."
        ]
    },
    "3": {
        "name": "Third Conditional",
        "formation": {
            "Positive": "If + past perfect, would + have + past participle",
            "Negative": "If + past perfect, would + not + have + past participle",
            "Question": "Would + subject + have + past participle?",
            "Short answer": "Yes, I would have. / No, I wouldn't have."
        },
        "usage_explanation": [
            "Talking about past situations that didn't happen.",
            "Imagining different outcomes if the past had changed."
        ],
        "usage_cases": build_20_exercises_for_conditional_name("Third Conditional"),
        "extra_examples": [
            "If I had known, I would have come earlier.",
            "We wouldn't have missed the flight if we had left on time."
        ]
    },
    "4": {
        "name": "Mixed Conditional",
        "formation": {
            "Positive": "If + past perfect, would + base form",
            "Negative": "If + past perfect, would + not + base form",
            "Question": "Would + subject + base form? (main clause), past perfect (if-clause)",
            "Short answer": "Yes, I would. / No, I wouldn't."
        },
        "usage_explanation": [
            "Combines a past hypothetical condition with a present or future result.",
            "Used when the time in the if-clause and main clause differ."
        ],
        "usage_cases": build_20_exercises_for_conditional_name("Mixed Conditional"),
        "extra_examples": [
            "If I had studied medicine, I would be a doctor now.",
            "She would be living in Spain if she had married Juan."
        ]
    }
}

##############################################################################
# 6) HELPER: reset_questions, get_current_data defined above
##############################################################################

##############################################################################
# 7) SIDEBAR CODE
##############################################################################
st.sidebar.title("Grammar Categories")

category = st.sidebar.radio("Select a category:", [GrammarCategory.TENSES.value, GrammarCategory.CONDITIONALS.value])
# Convert the chosen string back to the enum
if category == "Tenses":
    st.session_state.selected_category = GrammarCategory.TENSES
else:
    st.session_state.selected_category = GrammarCategory.CONDITIONALS

# Grammar item selector
if st.session_state.selected_category == GrammarCategory.TENSES:
    st.sidebar.subheader("Select a Tense")
    tense_options = ["Select a tense..."] + [f"{key}. {tenses_data[key]['name']}" for key in tenses_data]
    selected_option = st.sidebar.selectbox("Choose a tense:", tense_options)
    if selected_option != "Select a tense...":
        key_str = selected_option.split('.')[0].strip()
        if key_str != st.session_state.selected_item_key:
            st.session_state.selected_item_key = key_str
            reset_questions()
    else:
        st.session_state.selected_item_key = None
        reset_questions()
else:
    st.sidebar.subheader("Select a Conditional")
    conditional_options = ["Select a conditional..."] + [f"{key}. {conditionals_data[key]['name']}" for key in conditionals_data]
    selected_option = st.sidebar.selectbox("Choose a conditional:", conditional_options)
    if selected_option != "Select a conditional...":
        key_str = selected_option.split('.')[0].strip()
        if key_str != st.session_state.selected_item_key:
            st.session_state.selected_item_key = key_str
            reset_questions()
    else:
        st.session_state.selected_item_key = None
        reset_questions()

##############################################################################
# 8) SCREENS
##############################################################################
def show_welcome():
    st.title("Welcome to the Grammar Genius Game! 🎉✨🎮")
    st.write("""
    Get ready to boost your English grammar skills in a fun and interactive way!
    
    1. Use the sidebar to choose Tenses or Conditionals.
    2. Select which Tense/Conditional you want to practice.
    3. Each item has 20 multiple-choice exercises (including negative & question forms).
    4. After answering all exercises, you'll earn a special badge and can review your answers!
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
    st.write("Great job! Feel free to pick another grammar item from the sidebar if you want.")

def show_explanation_and_questions():
    # Determine which dictionary to use
    if st.session_state.selected_category == GrammarCategory.TENSES:
        data_dict = tenses_data
    else:
        data_dict = conditionals_data

    item_key = st.session_state.selected_item_key
    if not item_key:
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

    st.write("### Practice Exercises (Multiple Choice)")
    colA, colB = st.columns(2)
    colA.metric("Exercises Answered", f"{answered_count}")
    colB.metric("Total Exercises", f"{total_questions}")

    progress_val = int((answered_count / total_questions) * 100)
    st.progress(progress_val)

    # If all answered, award a badge
    if answered_count == total_questions:
        st.success(f"You've completed all {total_questions} exercises for {info['name']}!")
        st.markdown(f"**Badge Unlocked:** *{info['name']} Expert!* 🏆")
        if st.button("Review Your Answers"):
            st.session_state.review_mode = True
        return

    # Show each usage case
    for i, case in enumerate(usage_cases):
        answer_key = f"answer_{item_key}_{i}"
        submit_key = f"submit_{item_key}_{i}"

        # If the user already submitted this question, just show their answer
        if submit_key in st.session_state.submitted_questions:
            st.write(f"**{case['title']}**")
            if "context" in case:
                st.write(f"Context: {case['context']}")
            st.write(case["question"])
            user_answer = st.session_state.get(answer_key, "")
            st.write(f"Your answer: {user_answer}")
            continue

        # Display question
        st.write(f"**{case['title']}**")
        if "context" in case:
            st.write(f"Context: {case['context']}")
        st.write(case["question"])

        choices = case.get("choices", [])
        correct_choice = case.get("correct_choice", None)
        explanation = case.get("explanation", "")

        st.session_state.setdefault(answer_key, "")
        user_answer = st.selectbox("Select your answer:", ["-- Select --"] + choices, key=answer_key)

        # Submission
        if st.button("Submit", key=submit_key):
            st.session_state.answers.append(user_answer)
            st.session_state.submitted_questions.add(submit_key)

            # Find a motivational message
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
            elif correct_choice and user_answer == correct_choice:
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
# 9) MAIN FUNCTION
##############################################################################
def main():
    # 1) If no item chosen, show welcome, else the practice screen
    if st.session_state.selected_item_key is None:
        show_welcome()
    else:
        show_explanation_and_questions()

if __name__ == "__main__":
    main()
