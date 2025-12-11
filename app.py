# app.py
import streamlit as st
import time
from src.puzzle_generator import generate_puzzle
from src.adaptive_engine import AdaptiveEngine
from src.tracker import SessionTracker

QUESTIONS_PER_ROUND = 10
LEVEL_NAMES = ["Easy","Medium","Hard","Warrior"]
DEFAULT_LR = 0.45
DEFAULT_TARGET = 0.72

st.set_page_config(page_title="Math Adventures", page_icon="🎯")
st.title("Math Adventures — Demo (Streamlit)")

# session init
if "name" not in st.session_state:
    st.session_state.name = None
if "engine" not in st.session_state:
    st.session_state.engine = None
if "tracker" not in st.session_state:
    st.session_state.tracker = None
if "q_num" not in st.session_state:
    st.session_state.q_num = 0
if "current_puzzle" not in st.session_state:
    st.session_state.current_puzzle = None
    st.session_state.current_answer = None
    st.session_state.start_time = None
if "round_active" not in st.session_state:
    st.session_state.round_active = False
if "answer_input" not in st.session_state:
    st.session_state.answer_input = ""

def start_round(init_level):
    st.session_state.engine = AdaptiveEngine(init_level=init_level, max_level=3, lr=DEFAULT_LR, target=DEFAULT_TARGET)
    st.session_state.tracker = SessionTracker()
    st.session_state.q_num = 0
    st.session_state.current_puzzle = None
    st.session_state.current_answer = None
    st.session_state.start_time = None
    st.session_state.round_active = True
    st.session_state.answer_input = ""

def create_next():
    if not st.session_state.round_active:
        return
    if st.session_state.current_puzzle is None and st.session_state.q_num < QUESTIONS_PER_ROUND:
        level = st.session_state.engine.get_level()
        p,a = generate_puzzle(level)
        st.session_state.current_puzzle = p
        st.session_state.current_answer = a
        st.session_state.start_time = time.monotonic()
        st.session_state.answer_input = ""

# UI
if st.session_state.name is None:
    name = st.text_input("What's your name?")
    if st.button("Start"):
        if name.strip():
            st.session_state.name = name.strip()
            st.experimental_rerun()
    st.stop()

st.write(f"Hi **{st.session_state.name}**")

if not st.session_state.round_active:
    st.write("Choose starting difficulty:")
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        if st.button("1 Easy"):
            start_round(0)
            st.experimental_rerun()
    with c2:
        if st.button("2 Medium"):
            start_round(1)
            st.experimental_rerun()
    with c3:
        if st.button("3 Hard"):
            start_round(2)
            st.experimental_rerun()
    with c4:
        if st.button("4 Warrior"):
            start_round(3)
            st.experimental_rerun()
    st.stop()

# active round
create_next()
if st.session_state.q_num >= QUESTIONS_PER_ROUND and st.session_state.current_puzzle is None:
    st.session_state.round_active = False

if not st.session_state.round_active:
    st.subheader("Round finished")
    tr = st.session_state.tracker
    if tr:
        st.write(f"Accuracy: {tr.accuracy()*100:.1f}%")
        st.write(f"Avg time: {tr.avg_time():.2f}s")
        st.write(f"Final level: {LEVEL_NAMES[st.session_state.engine.get_level()]}")
        for a in tr.attempts:
            st.write(f"- {LEVEL_NAMES[a.difficulty]} | Correct: {a.correct} | Time: {a.time_taken:.2f}s | Ans: {a.user_answer} | True: {a.correct_answer}")
    if st.button("Play again"):
        st.session_state.engine = None
        st.session_state.tracker = None
        st.session_state.q_num = 0
        st.session_state.current_puzzle = None
        st.session_state.current_answer = None
        st.session_state.start_time = None
        st.session_state.round_active = False
        st.experimental_rerun()
    st.stop()

# show question
st.write(f"Question {st.session_state.q_num + 1} / {QUESTIONS_PER_ROUND}")
level = st.session_state.engine.get_level()
st.write(f"Difficulty: **{LEVEL_NAMES[level]}**")
st.write(f"### {st.session_state.current_puzzle} = ?")

with st.form("answer_form"):
    ans_in = st.text_input("Your answer:", key="answer_input")
    submit = st.form_submit_button("Submit")
if submit:
    if st.session_state.start_time is None:
        st.error("Timer error - resetting question")
        st.session_state.current_puzzle = None
        st.session_state.current_answer = None
        st.session_state.start_time = None
        st.experimental_rerun()
    try:
        user = int(ans_in)
    except:
        st.error("Enter a whole number")
        st.stop()
    elapsed = time.monotonic() - st.session_state.start_time
    correct = (user == st.session_state.current_answer)
    # log, include true answer
    st.session_state.tracker.log_attempt(level, correct, elapsed, user, st.session_state.current_answer)
    st.session_state.engine.update(correct, elapsed)
    # capture true answer for immediate feedback
    true_ans = st.session_state.current_answer
    st.session_state.q_num += 1
    st.session_state.current_puzzle = None
    st.session_state.current_answer = None
    st.session_state.start_time = None
    st.session_state.answer_input = ""
    if correct:
        st.success(f"Correct! Time: {elapsed:.2f}s")
    else:
        st.error(f"Incorrect — correct answer was {true_ans}")
    st.experimental_rerun()
