import streamlit as st
import random

##############################################################################
# 1) PAGE CONFIG (No 'theme' param to avoid TypeError)
##############################################################################
st.set_page_config(
    page_title="Grammar Genius App",
    layout="wide"
)

##############################################################################
# 2) SESSION STATE
##############################################################################
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Tenses"  # default category is "Tenses"
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
# 3) DEFINE TWO CSS THEMES (Dark, Light)
##############################################################################
DARK_CSS = """
<style>
/* Dark theme: black main background, dark blue sidebar, white text, orange headings */
body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBody"] {
    background-color: #000000 !important; /* black */
    color: #ffffff !important; /* white text */
}
[data-testid="stSidebar"] {
    background-color: #013369 !important; /* dark blue sidebar */
    color: #ffffff !important;
}
h1, h2, h3 {
    color: #ff5722 !important; /* orange headings */
    font-family: "Trebuchet MS", sans-serif;
}
main > div {
    padding-top: 20px;
}
</style>
"""

LIGHT_CSS = """
<style>
/* Light theme: white main background, lighter sidebar, black text, orange headings */
body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBody"] {
    background-color: #ffffff !important; /* white main background */
    color: #000000 !important; /* black text */
}
[data-testid="stSidebar"] {
    background-color: #f0f0f0 !important; /* light grey sidebar */
    color: #000000 !important;
}
h1, h2, h3 {
    color: #ff5722 !important; /* orange headings */
    font-family: "Trebuchet MS", sans-serif;
}
main > div {
    padding-top: 20px;
}
</style>
"""

##############################################################################
# 4) TENSES AND CONDITIONALS DATA -- Insert your actual data below
##############################################################################
tenses_data = {
    "1": {
        "name": "Present Simple",
        "formation": {
            "Positive": "Subject + base form (e.g., 'I eat')",
            "Negative": "Subject + do not/does not + base form (e.g., 'I do not eat')",
            "Question": "Do/Does + subject + base form? (e.g., 'Do you eat?')",
            "Short answer": "'Yes, I do.' / 'No, I don't.'"
        },
        "usage_explanation": [
            "General or always true facts.",
            "Situations that are more or less permanent.",
            "Habits or things done regularly.",
            "Short actions happening now (e.g., sports commentary).",
            "Regular events (often with always, often, never)."
        ],
        "usage_cases": [
            {"title": "Expressing facts and general truths",
             "question": "Does water boil if you heat it up?"},
            {"title": "Describing habits",
             "question": "What do you usually do after waking up?"},
            {"title": "Talking about permanent situations",
             "question": "Where do you live?"},
            {"title": "Regular events",
             "question": "How often do you go to the gym?"},
            {"title": "Describing routines",
             "question": "What time do you start work every day?"},
            {"title": "Present commentary",
             "question": "Does the commentator describe the players' actions as they happen?"},
            {"title": "General preferences",
             "question": "Which type of music do you prefer?"},
            {"title": "Timetabled events",
             "question": "When does the train leave?"},
            {"title": "Stating a general ability",
             "question": "Do you speak Spanish fluently?"},
            {"title": "Describing personality traits",
             "question": "Does your friend often help others?"}
        ],
        "extra_examples": [
            "I always wake up at 7 AM.",
            "My brother doesn't eat fish.",
            "Do we need more milk?",
            "The Earth revolves around the Sun.",
            "They never watch TV in the morning."
        ]
    },
    "2": {
        "name": "Past Simple",
        "formation": {
            "Positive": "Subject + past form (e.g., 'I ate')",
            "Negative": "Subject + did not + base form (e.g., 'I did not eat')",
            "Question": "Did + subject + base form? (e.g., 'Did you eat?')",
            "Short answer": "'Yes, I did.' / 'No, I didn't.'"
        },
        "usage_explanation": [
            "Completed actions in the past.",
            "Actions that happened at a specific time.",
            "A series of actions in the past.",
            "Past habits or situations (often with 'used to')."
        ],
        "usage_cases": [
            {"title": "Completed actions at a specific time",
             "question": "What did you do yesterday evening?"},
            {"title": "A specific past event",
             "question": "Did you attend the concert last Friday?"},
            {"title": "A series of events",
             "question": "What happened after you arrived home?"},
            {"title": "Past habits",
             "question": "Where did you usually spend your summer holidays as a child?"},
            {"title": "Situations that no longer exist",
             "question": "Did you live in another country before?"},
            {"title": "Historical facts",
             "question": "Which year did the Second World War end?"},
            {"title": "Personal achievements",
             "question": "What was the best meal you ever cooked?"},
            {"title": "Past trips or experiences",
             "question": "Where did you travel last year?"},
            {"title": "Old favorites",
             "question": "Which TV shows did you like when you were younger?"},
            {"title": "Childhood memories",
             "question": "Did you have a favorite toy when you were a kid?"}
        ],
        "extra_examples": [
            "I visited my grandparents last weekend.",
            "They watched a movie yesterday.",
            "Did you talk to your friend about the issue?",
            "She cooked dinner last night.",
            "We didn’t see them at the party."
        ]
    },
    "3": {
        "name": "Present Continuous",
        "formation": {
            "Positive": "Subject + am/is/are + verb-ing (e.g., 'I am eating')",
            "Negative": "Subject + am/is/are + not + verb-ing (e.g., 'I am not eating')",
            "Question": "Am/Is/Are + subject + verb-ing? (e.g., 'Are you eating?')",
            "Short answer": "'Yes, I am.' / 'No, I'm not.'"
        },
        "usage_explanation": [
            "Actions happening right now, at this moment.",
            "Temporary situations, not always true but happening around now.",
            "Trends or changing situations.",
            "Annoying habits (often with 'always')."
        ],
        "usage_cases": [
            {"title": "Actions happening now",
             "question": "What are you doing at this very moment?"},
            {"title": "Temporary situations",
             "question": "Are you staying with your parents this week?"},
            {"title": "Trends",
             "question": "Is online learning becoming more popular these days?"},
            {"title": "Changing situations",
             "question": "Is your town growing quickly?"},
            {"title": "Annoying habits",
             "question": "Are you always forgetting your keys?"},
            {"title": "Unusual behavior",
             "question": "Are you eating more vegetables than usual lately?"},
            {"title": "Current projects",
             "question": "Are you working on any new skills right now?"},
            {"title": "Near-future plans",
             "question": "Are you meeting your friends later today?"},
            {"title": "Ongoing processes",
             "question": "Are they building a new mall in your neighborhood?"},
            {"title": "Temporary states",
             "question": "Is your friend studying abroad this semester?"}
        ],
        "extra_examples": [
            "I am studying English right now.",
            "She is currently watching a documentary.",
            "We are planning a trip for the holidays.",
            "He is getting better at playing the guitar.",
            "They are always arguing over small things."
        ]
    },
    "4": {
        "name": "Past Continuous",
        "formation": {
            "Positive": "Subject + was/were + verb-ing (e.g., 'I was eating')",
            "Negative": "Subject + was/were + not + verb-ing (e.g., 'I was not eating')",
            "Question": "Was/Were + subject + verb-ing? (e.g., 'Were you eating?')",
            "Short answer": "'Yes, I was.' / 'No, I wasn't.'"
        },
        "usage_explanation": [
            "Actions in progress at a specific moment in the past.",
            "Background activities interrupted by another event.",
            "Two ongoing actions happening at the same time in the past.",
            "Setting a scene or giving context in a narrative."
        ],
        "usage_cases": [
            {"title": "Action in progress at a specific time",
             "question": "What were you doing at 8 PM yesterday?"},
            {"title": "Interrupted actions",
             "question": "What were you doing when the phone rang?"},
            {"title": "Background actions",
             "question": "Were you reading a book while it started to rain?"},
            {"title": "Parallel actions",
             "question": "Were they watching TV while you were cooking dinner?"},
            {"title": "Setting a scene",
             "question": "Were people talking loudly during the presentation?"},
            {"title": "Ongoing past habit",
             "question": "Were you always coming late to class last year?"},
            {"title": "Emphasis on duration",
             "question": "Were you studying for hours before the exam?"},
            {"title": "Temporary past states",
             "question": "Were you living with your grandparents last summer?"},
            {"title": "Action before a specific event",
             "question": "Were you already waiting for the bus when it arrived?"},
            {"title": "Ongoing background detail",
             "question": "Were you listening to music while working on the report?"}
        ],
        "extra_examples": [
            "I was reading a book when you knocked on the door.",
            "She was sleeping at noon yesterday.",
            "They were discussing the plan while I listened.",
            "We were watching a movie when the power went out.",
            "He was working late all last week."
        ]
    },
    "5": {
        "name": "Present Perfect",
        "formation": {
            "Positive": "Subject + have/has + past participle (e.g., 'I have eaten')",
            "Negative": "Subject + have/has + not + past participle (e.g., 'I have not eaten')",
            "Question": "Have/Has + subject + past participle? (e.g., 'Have you eaten?')",
            "Short answer": "'Yes, I have.' / 'No, I haven't.'"
        },
        "usage_explanation": [
            "Actions that happened at an unspecified time or continue until now.",
            "Life experiences without mentioning a specific time.",
            "Actions that started in the past and continue to the present.",
            "Recent events with words like 'just' or 'already'.",
            "Repeated actions up to now."
        ],
        "usage_cases": [
            {"title": "Life experiences",
             "question": "Have you ever traveled to an exotic country?"},
            {"title": "Unspecified time",
             "question": "Have you finished reading that novel yet?"},
            {"title": "Recent events",
             "question": "Have you already eaten breakfast today?"},
            {"title": "Repeated actions up to now",
             "question": "How many times have you seen that movie?"},
            {"title": "Actions continuing until now",
             "question": "How long have you lived in this city?"},
            {"title": "Past events with present relevance",
             "question": "Have you heard the latest news about the new policy?"},
            {"title": "Using 'just'",
             "question": "Have you just arrived at the station?"},
            {"title": "Using 'yet'",
             "question": "Have you submitted your assignment yet?"},
            {"title": "Using 'already'",
             "question": "Have you already called your parents today?"},
            {"title": "Achievements in your life",
             "question": "Have you won any competitions recently?"}
        ],
        "extra_examples": [
            "I have visited London three times.",
            "She has lost her keys again!",
            "They have never tried sushi before.",
            "We have already watched that film.",
            "He has just finished his homework."
        ]
    },
    "6": {
        "name": "Future Simple",
        "formation": {
            "Positive": "Subject + will + base form (e.g., 'I will eat')",
            "Negative": "Subject + will + not + base form (e.g., 'I will not eat')",
            "Question": "Will + subject + base form? (e.g., 'Will you eat?')",
            "Short answer": "'Yes, I will.' / 'No, I won't.'"
        },
        "usage_explanation": [
            "Decisions made at the moment of speaking.",
            "Predictions about the future.",
            "Promises or offers.",
            "Future facts or certainties."
        ],
        "usage_cases": [
            {"title": "Spontaneous decisions",
             "question": "What will you do if it starts raining now?"},
            {"title": "Predictions",
             "question": "Will computers eventually replace teachers?"},
            {"title": "Promises",
             "question": "Will you help me move these boxes?"},
            {"title": "Offers",
             "question": "Will you have some tea?"},
            {"title": "Future facts",
             "question": "Will the sun rise at 6 AM tomorrow?"},
            {"title": "Immediate plans",
             "question": "Will you go shopping after work?"},
            {"title": "Looking ahead",
             "question": "Will you travel abroad next year?"},
            {"title": "Future routines",
             "question": "Will we see each other every weekend?"},
            {"title": "Predicted success",
             "question": "Will you achieve your language goals soon?"},
            {"title": "Change of mind",
             "question": "Will you still want that gift tomorrow?"}
        ],
        "extra_examples": [
            "I will talk to you later.",
            "They will be here soon.",
            "She will probably come to the party.",
            "We will see what happens next.",
            "He will finish the project on time."
        ]
    },
    "7": {
        "name": "Future Continuous",
        "formation": {
            "Positive": "Subject + will be + verb-ing (e.g., 'I will be eating')",
            "Negative": "Subject + will + not + be + verb-ing (e.g., 'I will not be eating')",
            "Question": "Will + subject + be + verb-ing? (e.g., 'Will you be eating?')",
            "Short answer": "'Yes, I will.' / 'No, I won't.'"
        },
        "usage_explanation": [
            "Actions that will be in progress at a specific time in the future.",
            "Polite inquiries about someone's plans.",
            "Future events expected to be continuing.",
            "Overlapping or background activities in the future."
        ],
        "usage_cases": [
            {"title": "Action in progress at a future time",
             "question": "What will you be doing at 8 PM tomorrow?"},
            {"title": "Polite inquiries",
             "question": "Will you be joining us for dinner later?"},
            {"title": "Expected future events",
             "question": "Will they be traveling throughout Europe next month?"},
            {"title": "Overlapping future actions",
             "question": "Will you be working while they visit your house?"},
            {"title": "Scene setting in the future",
             "question": "Will the team be practicing on the field at that time?"},
            {"title": "Future background action",
             "question": "Will you be studying when the guests arrive?"},
            {"title": "Predicting a continuing state",
             "question": "Will you be living in the city or the countryside next year?"},
            {"title": "Alternative future plans",
             "question": "Will we be taking the train or driving ourselves to the conference?"},
            {"title": "Scheduled but extended actions",
             "question": "Will you be practicing the piano all afternoon?"},
            {"title": "Establishing a future timeline",
             "question": "Will you be waiting for us at the airport when we arrive?"}
        ],
        "extra_examples": [
            "I will be working at 8 PM tomorrow.",
            "She will be studying abroad next semester.",
            "They will be driving through the mountains this weekend.",
            "We will be waiting for your call.",
            "He will be sleeping by the time you get home."
        ]
    }
}

# ---------------------------------------------------------
# Data for Conditionals
# ---------------------------------------------------------
conditionals_data = {
    "0": {
        "name": "Zero Conditional",
        "formation": {
            "Positive": "If + present simple, present simple (e.g., 'If you heat water, it boils.')",
            "Negative": "If + present simple, present simple (negative) (e.g., 'If you don’t water plants, they die.')",
            "Question": "Do/Does + subject + base form in each clause as needed.",
            "Short answer": "N/A for conditionals (though you can still say 'Yes, it does.' etc.)"
        },
        "usage_explanation": [
            "Facts and things that are always true under certain conditions.",
            "General truths, scientific facts, or cause-and-effect relationships."
        ],
        "usage_cases": [
            {"title": "General truths",
             "question": "What happens if you leave ice in the sun?"},
            {"title": "Scientific facts",
             "question": "If you mix red and white paint, what do you get?"},
            {"title": "Cause and effect",
             "question": "What happens if people don't sleep enough?"},
            {"title": "Routine results",
             "question": "If I don't set an alarm, what usually happens?"},
            {"title": "Universal truths",
             "question": "If the Earth spins, does it create day and night?"},
            {"title": "Health tips",
             "question": "If you don't exercise regularly, how does your body react?"},
            {"title": "Lifestyle cause/effect",
             "question": "If you drink coffee late at night, does it keep you awake?"},
            {"title": "Safety warnings",
             "question": "If you touch a hot stove, what happens?"},
            {"title": "Everyday logic",
             "question": "If you drive too fast, what occurs?"},
            {"title": "Practical knowledge",
             "question": "If you press Ctrl+S in most programs, what happens?"}
        ],
        "extra_examples": [
            "If you freeze water, it becomes ice.",
            "If you heat metal, it expands.",
            "If I am tired, I go to bed early.",
            "If people eat too much sugar, they gain weight.",
            "If you scratch me, I bleed."
        ]
    },
    "1": {
        "name": "First Conditional",
        "formation": {
            "Positive": "If + present simple, will + base form (e.g., 'If you work hard, you will succeed.')",
            "Negative": "If + present simple, will + not + base form (e.g., 'If you don't hurry, we won't catch the train.')",
            "Question": "Will + subject + base form in the main clause, present simple in the if-clause.",
            "Short answer": "Yes, I will. / No, I won't, etc."
        },
        "usage_explanation": [
            "Real or likely future situations.",
            "Cause-and-effect in the future.",
            "Promises or threats based on a future condition."
        ],
        "usage_cases": [
            {"title": "Likely future",
             "question": "If you study hard, what will happen to your exam results?"},
            {"title": "Conditional promise",
             "question": "If you help me move, will I buy you dinner?"},
            {"title": "Threat or warning",
             "question": "If you don't lock the door, what might happen?"},
            {"title": "Future cause-and-effect",
             "question": "If we water the plants every day, what will they do?"},
            {"title": "Planning events",
             "question": "If the weather is good tomorrow, what will you do?"},
            {"title": "Result of an action",
             "question": "If you press the button, what will the machine do?"},
            {"title": "Advising a friend",
             "question": "If you stay up too late, how will you feel in the morning?"},
            {"title": "Travel arrangements",
             "question": "If we buy the tickets online, will we save money?"},
            {"title": "Job prospects",
             "question": "If you learn another language, will it help your career?"},
            {"title": "Conditional threat",
             "question": "If you don't listen, will it cause more problems?"}
        ],
        "extra_examples": [
            "If it rains, I will take an umbrella.",
            "If I find your keys, I will call you immediately.",
            "If we don't leave now, we'll be late.",
            "If she studies, she will pass the test.",
            "If you invite me, I will definitely come."
        ]
    },
    "2": {
        "name": "Second Conditional",
        "formation": {
            "Positive": "If + past simple, would + base form (e.g., 'If I had more time, I would travel.')",
            "Negative": "If + past simple, would + not + base form (e.g., 'If I didn't have to work, I wouldn't stay at home.')",
            "Question": "Would + subject + base form in the main clause, past simple in the if-clause.",
            "Short answer": "Yes, I would. / No, I wouldn't."
        },
        "usage_explanation": [
            "Unreal or imaginary situations in the present/future.",
            "Hypothetical situations where the condition is unlikely or impossible.",
            "Talking about dreams, wishes, or improbable scenarios."
        ],
        "usage_cases": [
            {"title": "Improbable future",
             "question": "If you won the lottery, what would you buy first?"},
            {"title": "Imaginary scenario",
             "question": "If you could live anywhere in the world, where would you live?"},
            {"title": "Dream job",
             "question": "If you didn't have to work for money, how would you spend your time?"},
            {"title": "Hypothetical ability",
             "question": "If you could speak every language, where would you travel?"},
            {"title": "Regret or desire",
             "question": "If you had more free time, what new hobby would you start?"},
            {"title": "Relationship advice",
             "question": "If your friend asked you for a big favor, would you help him?"},
            {"title": "Personal preference",
             "question": "If you could change one thing about yourself, what would it be?"},
            {"title": "Alternative present",
             "question": "If you weren’t here right now, where would you be?"},
            {"title": "Utopian idea",
             "question": "If you could end one global problem, which one would you choose?"},
            {"title": "Curiosity question",
             "question": "If you found a magic lamp, what would you wish for?"}
        ],
        "extra_examples": [
            "If I had a car, I would drive to the beach.",
            "If he were taller, he could play basketball better.",
            "If I didn't have to work, I'd travel more.",
            "I would adopt a puppy if I lived in a bigger house.",
            "We would go camping if we had a tent."
        ]
    },
    "3": {
        "name": "Third Conditional",
        "formation": {
            "Positive": "If + past perfect, would + have + past participle (e.g., 'If I had known, I would have come earlier.')",
            "Negative": "If + past perfect, would + not + have + past participle",
            "Question": "Would + subject + have + past participle in the main clause, past perfect in the if-clause.",
            "Short answer": "Yes, I would have. / No, I wouldn't have."
        },
        "usage_explanation": [
            "Talking about past situations that did not happen.",
            "Imagining different outcomes if the past had been different.",
            "Expressing regrets or hypothetical changes to past events."
        ],
        "usage_cases": [
            {"title": "Regret",
             "question": "If you had studied harder, how might your exam results have changed?"},
            {"title": "Missed opportunity",
             "question": "If you had taken that job offer, where would you be now?"},
            {"title": "Alternate history",
             "question": "If a key historical event hadn't happened, how would the world differ?"},
            {"title": "Past relationships",
             "question": "If you had stayed in touch with your old friend, would things be different now?"},
            {"title": "Personal decisions",
             "question": "If you had chosen a different major, what career path would you have?"},
            {"title": "Avoiding mistakes",
             "question": "If you had read the instructions carefully, would you have made fewer errors?"},
            {"title": "Emphasizing outcomes",
             "question": "If we had arrived earlier, would we have caught the train?"},
            {"title": "Hypothetical inventions",
             "question": "If someone had invented a time machine, how would the past have changed?"},
            {"title": "Canceled plans",
             "question": "If they had not canceled the event, would you have gone?"},
            {"title": "Different future now",
             "question": "If you had moved abroad, where would you be living today?"}
        ],
        "extra_examples": [
            "If I had known about the party, I would have come.",
            "She wouldn't have missed the flight if she had left earlier.",
            "If we had prepared better, we could have won.",
            "I would have helped if I had realized you were struggling.",
            "They would have visited us if they had had more time."
        ]
    },
    "4": {
        "name": "Mixed Conditional",
        "formation": {
            "Positive": "If + past perfect, would + base form (e.g., 'If I had studied harder, I would be a doctor now.')",
            "Negative": "If + past perfect, would + not + base form",
            "Question": "Would + subject + base form in the main clause, past perfect in the if-clause.",
            "Short answer": "Yes, I would. / No, I wouldn't."
        },
        "usage_explanation": [
            "Combines a past hypothetical condition with a present/future hypothetical result.",
            "Shows how a change in the past would affect the present.",
            "Used when the time in the if-clause and the time in the main clause are different."
        ],
        "usage_cases": [
            {"title": "Past affects present",
             "question": "If you had taken that course, would you have a better job today?"},
            {"title": "Regret with present consequences",
             "question": "If I had saved more money, would I be living in a nicer apartment now?"},
            {"title": "Different past = different now",
             "question": "If you had grown up in a different country, what language would you speak at home?"},
            {"title": "Changing a past mistake",
             "question": "If she had listened to advice, would she be in trouble now?"},
            {"title": "Opportunity missed",
             "question": "If I had learned to code earlier, would I be working in tech?"},
            {"title": "Emotional reflection",
             "question": "If you had apologized sooner, would your friend still be upset?"},
            {"title": "Alternative reality in present",
             "question": "If we had met years ago, do you think we would be closer friends today?"},
            {"title": "Personal growth",
             "question": "If you had read more books in your teens, would you be more knowledgeable now?"},
            {"title": "Financial changes",
             "question": "If they had invested in Bitcoin early, would they be rich now?"},
            {"title": "Life path reflection",
             "question": "If he had joined the army, would he be living in a different city today?"}
        ],
        "extra_examples": [
            "If I had studied medicine, I would be a doctor now.",
            "If he had left on time, he wouldn't be stuck in traffic right now.",
            "We would own a house now if we had saved money more diligently.",
            "If she had married him, she would be living abroad today.",
            "If you had eaten breakfast, you wouldn't be so hungry now."
        ]
    }
}


##############################################################################
# 5) HELPER FUNCTIONS
##############################################################################
def reset_questions():
    """Reset answers, submitted questions, and review mode. Also reshuffle motivational messages."""
    st.session_state.answers = []
    st.session_state.submitted_questions = set()
    st.session_state.review_mode = False
    random.shuffle(st.session_state.randomized_messages)

def get_current_data():
    """Return the dictionary and item key for whichever Tense/Conditional is chosen."""
    if st.session_state.selected_category == "Tenses":
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
# 6) SIDEBAR: Category & Theme Toggles
##############################################################################
st.sidebar.title("Grammar Categories")

# Category toggle
category = st.sidebar.radio("Select a category:", ["Tenses", "Conditionals"])
st.session_state.selected_category = category

# Depending on category, build the list of tenses or conditionals
if st.session_state.selected_category == "Tenses":
    st.sidebar.subheader("Select a Tense")
    tense_options = ["Select a tense..."] + [f"{key}. {tenses_data[key]['name']}" for key in tenses_data]
    selected_option = st.sidebar.selectbox("Choose a tense to practice:", tense_options)
    if selected_option != "Select a tense...":
        current_key = selected_option.split('.')[0].strip()
        if current_key != st.session_state.selected_item_key:
            st.session_state.selected_item_key = current_key
            reset_questions()
    else:
        st.session_state.selected_item_key = None
        reset_questions()
else:
    st.sidebar.subheader("Select a Conditional")
    conditional_options = ["Select a conditional..."] + [f"{key}. {conditionals_data[key]['name']}" for key in conditionals_data]
    selected_option = st.sidebar.selectbox("Choose a conditional to practice:", conditional_options)
    if selected_option != "Select a conditional...":
        current_key = selected_option.split('.')[0].strip()
        if current_key != st.session_state.selected_item_key:
            st.session_state.selected_item_key = current_key
            reset_questions()
    else:
        st.session_state.selected_item_key = None
        reset_questions()

# Theme toggle
theme_choice = st.sidebar.radio("Choose a Theme:", ["Dark", "Light"], index=0)
if theme_choice == "Dark":
    st.markdown(DARK_CSS, unsafe_allow_html=True)
else:
    st.markdown(LIGHT_CSS, unsafe_allow_html=True)

##############################################################################
# 7) SCREENS
##############################################################################
def show_welcome():
    """Welcome screen, no name input, no balloons."""
    st.title("Welcome to the Grammar Genius Game! 🎉✨🎮")
    st.write("""
    Get ready to boost your English grammar skills in a fun and interactive way!
    
    1. Use the sidebar to choose either Tenses or Conditionals.
    2. Select which Tense/Conditional you want to practice.
    3. Read how it's formed, when to use it, and see extra examples.
    4. Answer the questions, receiving motivational feedback each time.
    5. Once you finish all questions, you'll earn a special badge!

    Let's begin!
    """)

def show_review(data_dict, item_key):
    """Review screen: show answered questions, each with a trophy 🏆."""
    st.header("Review Your Answers")
    usage_cases = data_dict[item_key]["usage_cases"]
    for i, case in enumerate(usage_cases):
        answer_key = f"answer_{item_key}_{i}"
        st.write(f"**{case['title']}**")
        st.write(f"Question: {case['question']}")
        # Mark answers with a trophy
        user_answer = st.session_state.get(answer_key, "")
        st.write(f"Your answer: {user_answer} 🏆")
    st.write("Feel free to pick another item from the sidebar if you want.")

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

    st.write("### Practice Questions")
    colA, colB = st.columns(2)
    colA.metric("Questions Answered", f"{answered_count}")
    colB.metric("Total Questions", f"{total_questions}")

    progress_val = int((answered_count / total_questions) * 100)
    st.progress(progress_val)

    # If user has completed all 10 usage cases
    if answered_count == total_questions:
        st.success(f"You've answered all 10 questions for {info['name']}!")
        st.markdown(f"**Badge Unlocked:** *{info['name']} Expert!* 🏆")

        if st.button("Review Your Answers"):
            st.session_state.review_mode = True
        return

    # Display each question
    for i, case in enumerate(usage_cases):
        answer_key = f"answer_{item_key}_{i}"
        submit_key = f"submit_{item_key}_{i}"

        if submit_key in st.session_state.submitted_questions:
            # Already answered
            st.write(f"**{case['title']}**")
            st.write(case["question"])
            user_answer = st.session_state.get(answer_key, "")
            st.write(f"Your answer: {user_answer}")
            continue

        # Two-column question layout
        q_col, a_col = st.columns([2, 3])
        with q_col:
            st.write(f"**{case['title']}**")
            st.write(case["question"])
        with a_col:
            st.text_input("Your answer:", key=answer_key)
            if st.button("Submit", key=submit_key):
                user_answer = st.session_state.get(answer_key, "")
                st.session_state.answers.append(user_answer)
                st.session_state.submitted_questions.add(submit_key)

                # Display next motivational message
                msg_index = len(st.session_state.answers) - 1
                if msg_index < len(st.session_state.randomized_messages):
                    msg = st.session_state.randomized_messages[msg_index]
                else:
                    msg = st.session_state.randomized_messages[-1]

                # Show the message
                if msg[0].isupper():
                    new_msg = f"{msg[0].lower() + msg[1:]}"
                else:
                    new_msg = msg

                st.success(new_msg)
                st.write(f"Your answer: {user_answer}")

##############################################################################
# 8) MAIN
##############################################################################
def main():
    if st.session_state.selected_item_key is None:
        show_welcome()
    else:
        show_explanation_and_questions()

if __name__ == "__main__":
    main()