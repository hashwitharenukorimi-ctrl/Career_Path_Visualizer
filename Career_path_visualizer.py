import streamlit as st
import ollama
import sqlite3
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# CAREER DATABASE
# ============================================================

career_data = {

    "Software Developer": {
        "skills": [
            "Python",
            "Java",
            "DSA",
            "OOP",
            "DBMS",
            "SQL",
            "Git"
        ],

        "roadmap": [
            "Programming Fundamentals",
            "Object-Oriented Programming",
            "Data Structures & Algorithms",
            "DBMS & SQL",
            "Git & GitHub",
            "Backend Development",
            "Build Projects",
            "Placement Preparation"
        ],

        "jobs": [
            "Software Developer",
            "Backend Developer",
            "Application Developer",
            "Software Engineer"
        ],

        "projects": [
            "Student Management System",
            "Expense Tracker",
            "Online Quiz Application"
        ]
    },


    "AI/ML Engineer": {
        "skills": [
            "Python",
            "Mathematics",
            "Statistics",
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "Generative AI",
            "Model Deployment"
        ],

        "roadmap": [
            "Python",
            "NumPy & Pandas",
            "Mathematics",
            "Statistics",
            "Machine Learning",
            "Deep Learning",
            "Generative AI",
            "Model Deployment",
            "Build AI Projects"
        ],

        "jobs": [
            "AI Engineer",
            "ML Engineer",
            "Deep Learning Engineer",
            "NLP Engineer",
            "Generative AI Engineer"
        ],

        "projects": [
            "AI Chatbot",
            "Image Classification System",
            "Document Question Answering System"
        ]
    },


    "Data Scientist": {
        "skills": [
            "Python",
            "Statistics",
            "NumPy",
            "Pandas",
            "SQL",
            "Data Visualization",
            "Machine Learning"
        ],

        "roadmap": [
            "Python",
            "Statistics",
            "NumPy & Pandas",
            "SQL",
            "Data Visualization",
            "Machine Learning",
            "Data Science Projects"
        ],

        "jobs": [
            "Data Scientist",
            "Data Analyst",
            "Business Analyst",
            "Research Analyst"
        ],

        "projects": [
            "House Price Prediction",
            "Customer Churn Prediction",
            "Student Performance Analysis"
        ]
    },


    "Web Developer": {
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Python",
            "SQL",
            "Git"
        ],

        "roadmap": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Backend Development",
            "Databases",
            "APIs",
            "Full Stack Projects"
        ],

        "jobs": [
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
            "Web Developer"
        ],

        "projects": [
            "Portfolio Website",
            "College Website",
            "E-Commerce Website"
        ]
    },


    "Cloud Engineer": {
        "skills": [
            "Linux",
            "Networking",
            "AWS",
            "Azure",
            "Docker",
            "Kubernetes",
            "Python"
        ],

        "roadmap": [
            "Linux",
            "Networking",
            "Cloud Fundamentals",
            "AWS/Azure",
            "Docker",
            "Kubernetes",
            "Cloud Projects"
        ],

        "jobs": [
            "Cloud Engineer",
            "Cloud Administrator",
            "Cloud Developer",
            "Cloud Architect"
        ],

        "projects": [
            "Cloud File Storage",
            "Cloud Website Deployment",
            "Cloud Monitoring System"
        ]
    },


    "Cybersecurity Analyst": {
        "skills": [
            "Networking",
            "Linux",
            "Python",
            "Cybersecurity",
            "Cryptography",
            "Security Tools"
        ],

        "roadmap": [
            "Networking",
            "Linux",
            "Python",
            "Cybersecurity Fundamentals",
            "Cryptography",
            "Security Labs",
            "Security Projects"
        ],

        "jobs": [
            "Cybersecurity Analyst",
            "SOC Analyst",
            "Security Engineer",
            "Security Consultant"
        ],

        "projects": [
            "Password Strength Checker",
            "Network Monitoring System",
            "Phishing Detection System"
        ]
    },


    "Data Engineer": {
        "skills": [
            "Python",
            "SQL",
            "Databases",
            "ETL",
            "Data Warehousing",
            "Apache Spark",
            "Cloud"
        ],

        "roadmap": [
            "Python",
            "SQL",
            "Databases",
            "ETL",
            "Data Warehousing",
            "Apache Spark",
            "Cloud Data Platforms"
        ],

        "jobs": [
            "Data Engineer",
            "Big Data Engineer",
            "ETL Developer",
            "Data Platform Engineer"
        ],

        "projects": [
            "ETL Pipeline",
            "Sales Data Pipeline",
            "Real-Time Data Processing System"
        ]
    },


    "QA / Test Engineer": {
        "skills": [
            "Software Testing",
            "Manual Testing",
            "Automation Testing",
            "Selenium",
            "Python",
            "Java",
            "API Testing"
        ],

        "roadmap": [
            "Software Testing",
            "Test Cases",
            "Bug Tracking",
            "API Testing",
            "Selenium",
            "Automation Testing",
            "Testing Projects"
        ],

        "jobs": [
            "QA Engineer",
            "Test Engineer",
            "Automation Tester",
            "SDET"
        ],

        "projects": [
            "Website Testing Project",
            "API Testing Project",
            "Automation Framework"
        ]
    }
}


# ============================================================
# SQLITE DATABASE
# ============================================================

DB_NAME = "careerpilot.db"


def get_connection():

    return sqlite3.connect(DB_NAME)


def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    # Conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            created_at TEXT NOT NULL

        )
    """)

    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            conversation_id INTEGER,

            role TEXT NOT NULL,

            content TEXT NOT NULL,

            created_at TEXT NOT NULL,

            FOREIGN KEY(conversation_id)
            REFERENCES conversations(id)

        )
    """)

    conn.commit()

    conn.close()


create_database()


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def create_conversation(title):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversations
        (title, created_at)

        VALUES (?, ?)
        """,

        (
            title,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    conversation_id = cursor.lastrowid

    conn.commit()

    conn.close()

    return conversation_id


def save_message(
    conversation_id,
    role,
    content
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages
        (conversation_id, role, content, created_at)

        VALUES (?, ?, ?, ?)
        """,

        (
            conversation_id,
            role,
            content,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    conn.commit()

    conn.close()


def get_conversations():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, created_at

        FROM conversations

        ORDER BY id DESC
        """
    )

    conversations = cursor.fetchall()

    conn.close()

    return conversations


def get_messages(conversation_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content

        FROM messages

        WHERE conversation_id = ?

        ORDER BY id ASC
        """,

        (conversation_id,)
    )

    messages = cursor.fetchall()

    conn.close()

    return messages


def delete_conversation(conversation_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM messages

        WHERE conversation_id = ?
        """,

        (conversation_id,)
    )

    cursor.execute(
        """
        DELETE FROM conversations

        WHERE id = ?
        """,

        (conversation_id,)
    )

    conn.commit()

    conn.close()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "conversation_id" not in st.session_state:

    st.session_state.conversation_id = None


if "interview_question" not in st.session_state:

    st.session_state.interview_question = ""


if "interview_feedback" not in st.session_state:

    st.session_state.interview_feedback = ""


if "progress" not in st.session_state:

    st.session_state.progress = {}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_match_score(
    user_skills,
    career_skills
):

    user_skills_lower = [
        skill.lower().strip()
        for skill in user_skills
    ]

    matched = 0

    for skill in career_skills:

        if skill.lower() in user_skills_lower:

            matched += 1

    score = int(
        (matched / len(career_skills)) * 100
    )

    return score


def get_missing_skills(
    user_skills,
    career_skills
):

    user_skills_lower = [
        skill.lower().strip()
        for skill in user_skills
    ]

    missing = []

    for skill in career_skills:

        if skill.lower() not in user_skills_lower:

            missing.append(skill)

    return missing


def ask_ollama(prompt):

    try:

        response = ollama.chat(

            model="llama3.2",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response[
            "message"
        ]["content"]

    except Exception as e:

        return (
            "⚠️ **Ollama connection problem.**\n\n"
            "Please make sure Ollama is running "
            "and `llama3.2` is installed.\n\n"
            f"Technical error: `{e}`"
        )


# ============================================================
# SIDEBAR — STUDENT PROFILE
# ============================================================

st.sidebar.title("🚀 CareerPilot AI")

st.sidebar.caption(
    "Your Personal Career GPS"
)

st.sidebar.markdown("---")

st.sidebar.subheader("👤 Student Profile")


student_name = st.sidebar.text_input(
    "Your Name",
    "Student"
)


year = st.sidebar.selectbox(
    "Current Year",

    [
        "1st Year",
        "2nd Year",
        "3rd Year",
        "4th Year"
    ]
)


goal = st.sidebar.selectbox(
    "Career Goal",

    [
        "Software Job",
        "AI Career",
        "Data Career",
        "Web Development",
        "Cloud Career",
        "Cybersecurity",
        "Not Sure"
    ]
)


skill_input = st.sidebar.text_area(
    "Your Current Skills",

    "Python, HTML, SQL"
)


user_skills = [

    skill.strip()

    for skill in skill_input.split(",")

    if skill.strip()
]


# ============================================================
# SIDEBAR — CHAT HISTORY
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("💬 Chat History")


# New Chat button

if st.sidebar.button(
    "➕ New Chat",
    use_container_width=True
):

    st.session_state.messages = []

    st.session_state.conversation_id = None

    st.rerun()


# Get previous conversations

conversations = get_conversations()


if len(conversations) == 0:

    st.sidebar.caption(
        "Your conversations will appear here."
    )

else:

    for conversation in conversations:

        conversation_id = conversation[0]

        title = conversation[1]

        # Chat button

        if st.sidebar.button(
            f"💬 {title}",
            key=f"conversation_{conversation_id}",
            use_container_width=True
        ):

            old_messages = get_messages(
                conversation_id
            )

            st.session_state.messages = [

                {
                    "role": role,
                    "content": content
                }

                for role, content in old_messages
            ]

            st.session_state.conversation_id = (
                conversation_id
            )

            st.rerun()


# ============================================================
# DELETE CHAT
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("🗑️ Manage History")


if len(conversations) > 0:

    delete_option = st.sidebar.selectbox(

        "Select conversation",

        conversations,

        format_func=lambda x: x[1],

        key="delete_chat_select"
    )


    if st.sidebar.button(
        "🗑️ Delete Selected Chat",
        use_container_width=True
    ):

        delete_id = delete_option[0]

        delete_conversation(
            delete_id
        )

        if (
            st.session_state.conversation_id
            == delete_id
        ):

            st.session_state.messages = []

            st.session_state.conversation_id = None

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🚀 CareerPilot AI")

st.subheader(
    "Your Personal Career GPS powered by AI"
)

st.write(
    "Analyze your skills → discover career matches → "
    "identify skill gaps → build your roadmap → "
    "practice interviews."
)

st.markdown("---")


# ============================================================
# DASHBOARD
# ============================================================

st.header(
    f"👋 Welcome, {student_name}!"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🎓 Education",
        year
    )


with col2:

    st.metric(
        "🧠 Skills",
        len(user_skills)
    )


with col3:

    st.metric(
        "🎯 Goal",
        goal
    )


with col4:

    st.metric(
        "💼 Careers",
        len(career_data)
    )


# ============================================================
# CAREER MATCH ENGINE
# ============================================================

st.markdown("---")

st.header("🎯 Career Match Engine")

st.write(
    "See which careers match your current skill set."
)


career_scores = []


for career_name, data in career_data.items():

    score = get_match_score(
        user_skills,
        data["skills"]
    )

    career_scores.append(
        (
            career_name,
            score
        )
    )


career_scores.sort(
    key=lambda x: x[1],
    reverse=True
)


top_careers = career_scores[:5]


for career_name, score in top_careers:

    col1, col2, col3 = st.columns(
        [3, 4, 1]
    )


    with col1:

        st.write(
            f"### {career_name}"
        )


    with col2:

        st.progress(
            score / 100
        )


    with col3:

        st.write(
            f"**{score}%**"
        )


best_career = career_scores[0][0]

best_score = career_scores[0][1]


st.success(
    f"🏆 Your strongest current match is "
    f"**{best_career}** with a "
    f"**{best_score}% skill match**."
)


# ============================================================
# TABS
# ============================================================

st.markdown("---")


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(

    [
        "🧠 Skill Gap",
        "🗺️ Career GPS",
        "💡 Projects",
        "🤖 AI Mentor",
        "🎤 Interview Arena",
        "🔄 Career Compare"
    ]
)


# ============================================================
# TAB 1 — SKILL GAP
# ============================================================

with tab1:

    st.header(
        "🧠 Skill Gap Analyzer"
    )


    selected_career = st.selectbox(

        "Choose a career to analyze",

        list(career_data.keys()),

        key="skill_gap_career"
    )


    selected_data = career_data[
        selected_career
    ]


    missing = get_missing_skills(

        user_skills,

        selected_data["skills"]
    )


    user_skills_lower = [

        x.lower()

        for x in user_skills
    ]


    matched = [

        skill

        for skill in selected_data["skills"]

        if skill.lower()
        in user_skills_lower
    ]


    score = get_match_score(

        user_skills,

        selected_data["skills"]
    )


    st.metric(
        "Career Readiness",
        f"{score}%"
    )


    st.progress(
        score / 100
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "✅ Skills You Have"
        )


        if matched:

            for skill in matched:

                st.write(
                    f"✅ {skill}"
                )

        else:

            st.info(
                "No matching skills yet."
            )


    with col2:

        st.subheader(
            "⚠️ Skills To Learn"
        )


        if missing:

            for skill in missing:

                st.write(
                    f"🔸 {skill}"
                )

        else:

            st.success(
                "Excellent! You have all listed skills."
            )


# ============================================================
# TAB 2 — CAREER GPS
# ============================================================

with tab2:

    st.header(
        "🗺️ Your Career GPS"
    )


    gps_career = st.selectbox(

        "Select your target career",

        list(career_data.keys()),

        key="gps_career"
    )


    gps_data = career_data[
        gps_career
    ]


    st.write(
        f"### 🎯 Destination: {gps_career}"
    )


    st.write(
        "Follow these milestones to reach your target role."
    )


    for index, step in enumerate(

        gps_data["roadmap"],

        start=1
    ):

        if step not in st.session_state.progress:

            st.session_state.progress[
                step
            ] = False


        completed = st.checkbox(

            f"Step {index}: {step}",

            value=st.session_state.progress[step],

            key=f"roadmap_{gps_career}_{index}"
        )


        st.session_state.progress[
            step
        ] = completed


        if completed:

            st.success(
                "Completed ✓"
            )


    completed_count = sum(

        st.session_state.progress.get(
            step,
            False
        )

        for step in gps_data["roadmap"]
    )


    total = len(
        gps_data["roadmap"]
    )


    percentage = int(

        (completed_count / total)
        * 100
    )


    st.markdown("---")


    st.subheader(
        "📊 Roadmap Progress"
    )


    st.progress(
        percentage / 100
    )


    st.write(
        f"**{completed_count}/{total} milestones "
        f"completed — {percentage}%**"
    )


# ============================================================
# TAB 3 — PROJECT GENERATOR
# ============================================================

with tab3:

    st.header(
        "💡 AI Project Generator"
    )


    project_career = st.selectbox(

        "Choose your target career",

        list(career_data.keys()),

        key="project_career"
    )


    project_level = st.selectbox(

        "Project difficulty",

        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


    project_interest = st.text_input(

        "What are you interested in?",

        "Education and AI"
    )


    if st.button(

        "✨ Generate My Project",

        use_container_width=True
    ):

        prompt = f"""

You are an expert software project mentor.

Student:
{student_name}

Year:
{year}

Target Career:
{project_career}

Current Skills:
{", ".join(user_skills)}

Project Difficulty:
{project_level}

Student Interest:
{project_interest}

Create ONE unique project.

Give:

1. Project Name
2. Problem Statement
3. Main Features
4. Technology Stack
5. Skills Learned
6. How it helps the student's resume
7. Possible future improvements

Keep the explanation student-friendly.
"""


        with st.spinner(
            "🤖 Designing your project..."
        ):

            result = ask_ollama(
                prompt
            )


        st.markdown(
            result
        )


# ============================================================
# TAB 4 — AI CAREER MENTOR
# ============================================================

with tab4:

    st.header(
        "🤖 AI Career Mentor"
    )


    st.write(
        "Your conversation is automatically saved "
        "in Chat History."
    )


    # --------------------------------------------------------
    # DISPLAY CURRENT CONVERSATION
    # --------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask your AI Career Mentor..."
    )


    if question:

        # ====================================================
        # CREATE NEW CONVERSATION
        # ====================================================

        if (
            st.session_state.conversation_id
            is None
        ):

            # Use first question as title

            title = question.strip()[:40]

            if len(question) > 40:

                title += "..."

            st.session_state.conversation_id = (

                create_conversation(
                    title
                )
            )


        conversation_id = (
            st.session_state.conversation_id
        )


        # ====================================================
        # SAVE USER MESSAGE
        # ====================================================

        st.session_state.messages.append(

            {
                "role": "user",
                "content": question
            }
        )


        save_message(

            conversation_id,

            "user",

            question
        )


        # Display question

        with st.chat_message("user"):

            st.markdown(
                question
            )


        # ====================================================
        # PREVIOUS CONVERSATION
        # ====================================================

        previous_conversation = ""


        for message in st.session_state.messages:

            previous_conversation += (

                f"{message['role'].upper()}: "
                f"{message['content']}\n\n"
            )


        # ====================================================
        # AI CONTEXT
        # ====================================================

        context = f"""

You are CareerPilot AI,
a personalized AI career mentor.

STUDENT PROFILE

Name:
{student_name}

Education:
B.Tech CSE

Current Year:
{year}

Career Goal:
{goal}

Current Skills:
{", ".join(user_skills)}

Best Career Match:
{best_career}

Best Match Score:
{best_score}%

CURRENT CONVERSATION:

{previous_conversation}

NEW STUDENT QUESTION:

{question}

INSTRUCTIONS:

1. Give personalized advice.
2. Consider the student's year.
3. Consider the student's current skills.
4. Consider the student's career goal.
5. Give practical steps.
6. Keep explanations simple.
7. Do not give unnecessarily complicated explanations.
8. If useful, give examples.
9. Help with internships and placements when relevant.
10. Remember the context of the conversation.

Answer the student's question.
"""


        # ====================================================
        # OLLAMA RESPONSE
        # ====================================================

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "🤖 CareerPilot is thinking..."
            ):

                answer = ask_ollama(
                    context
                )


            st.markdown(
                answer
            )


        # ====================================================
        # SAVE AI RESPONSE
        # ====================================================

        st.session_state.messages.append(

            {
                "role": "assistant",
                "content": answer
            }
        )


        save_message(

            conversation_id,

            "assistant",

            answer
        )


# ============================================================
# TAB 5 — INTERVIEW ARENA
# ============================================================

with tab5:

    st.header(
        "🎤 AI Interview Arena"
    )


    interview_career = st.selectbox(

        "Interview for",

        list(career_data.keys()),

        key="interview_career"
    )


    if st.button(

        "🎯 Generate Interview Question",

        use_container_width=True
    ):

        prompt = f"""

You are a technical interviewer.

Conduct an interview for a B.Tech CSE student.

Target Role:
{interview_career}

Student Year:
{year}

Current Skills:
{", ".join(user_skills)}

Generate ONE technical interview question.

Start with:

INTERVIEW QUESTION:

Do not provide the answer.
"""


        with st.spinner(
            "🎤 Interviewer is preparing..."
        ):

            question = ask_ollama(
                prompt
            )


        st.session_state.interview_question = (
            question
        )


        st.session_state.interview_feedback = ""


    if st.session_state.interview_question:

        st.markdown(
            st.session_state.interview_question
        )


        answer = st.text_area(

            "✍️ Your Answer",

            height=180
        )


        if st.button(

            "📊 Evaluate My Answer",

            use_container_width=True
        ):

            if answer.strip() == "":

                st.warning(
                    "Please write your answer first."
                )

            else:

                evaluation_prompt = f"""

You are an expert technical interviewer.

Career:
{interview_career}

Question:
{st.session_state.interview_question}

Student Answer:
{answer}

Evaluate the answer.

Give:

Technical Knowledge: /10
Accuracy: /10
Clarity: /10
Communication: /10
Overall Score: /10

Then provide:

1. What was good
2. What can be improved
3. A better answer approach
4. One interview tip

Be constructive and student-friendly.
"""


                with st.spinner(
                    "🤖 Evaluating your answer..."
                ):

                    feedback = ask_ollama(
                        evaluation_prompt
                    )


                st.session_state.interview_feedback = (
                    feedback
                )


    if st.session_state.interview_feedback:

        st.markdown("---")

        st.subheader(
            "📊 Interview Evaluation"
        )

        st.markdown(
            st.session_state.interview_feedback
        )


# ============================================================
# TAB 6 — CAREER COMPARISON
# ============================================================

with tab6:

    st.header(
        "🔄 Career Comparison"
    )


    col1, col2 = st.columns(2)


    with col1:

        career1 = st.selectbox(

            "Career 1",

            list(career_data.keys()),

            index=0,

            key="career_compare_1"
        )


    with col2:

        career2 = st.selectbox(

            "Career 2",

            list(career_data.keys()),

            index=1,

            key="career_compare_2"
        )


    data1 = career_data[
        career1
    ]


    data2 = career_data[
        career2
    ]


    st.markdown("---")


    c1, c2 = st.columns(2)


    with c1:

        st.subheader(
            f"🚀 {career1}"
        )


        st.write(
            "### 🧠 Skills"
        )


        for skill in data1["skills"]:

            st.write(
                f"• {skill}"
            )


        st.write(
            "### 💼 Jobs"
        )


        for job in data1["jobs"]:

            st.write(
                f"• {job}"
            )


    with c2:

        st.subheader(
            f"🤖 {career2}"
        )


        st.write(
            "### 🧠 Skills"
        )


        for skill in data2["skills"]:

            st.write(
                f"• {skill}"
            )


        st.write(
            "### 💼 Jobs"
        )


        for job in data2["jobs"]:

            st.write(
                f"• {job}"
            )


    score1 = get_match_score(

        user_skills,

        data1["skills"]
    )


    score2 = get_match_score(

        user_skills,

        data2["skills"]
    )


    st.markdown("---")


    st.subheader(
        "🎯 Your Personal Match"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            career1,
            f"{score1}%"
        )


    with col2:

        st.metric(
            career2,
            f"{score2}%"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🚀 CareerPilot AI | Personalized Career Guidance | "
    "Streamlit + Ollama + Llama 3.2 + SQLite"
)