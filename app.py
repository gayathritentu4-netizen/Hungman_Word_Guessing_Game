import random
import streamlit as st

st.set_page_config(page_title="Hangman Game", page_icon="🎯")

st.title("🎯 Hangman Word Guessing Game")
st.write("Guess the secret word before you run out of chances!")

# Load words
with open("English_words.txt", "r") as file:
    words = [
        line.strip().upper()
        for line in file
        if line.strip().isalpha() and len(line.strip()) >= 4
    ]

# Hangman drawings, from empty to complete
stages = [
    "  -----\n  |   |\n      |\n      |\n      |\n=========",
    "  -----\n  |   |\n  O   |\n      |\n      |\n=========",
    "  -----\n  |   |\n  O   |\n  |   |\n      |\n=========",
    "  -----\n  |   |\n  O   |\n /|   |\n      |\n=========",
    "  -----\n  |   |\n  O   |\n /|\\  |\n      |\n=========",
    "  -----\n  |   |\n  O   |\n /|\\  |\n /    |\n=========",
    "  -----\n  |   |\n  O   |\n /|\\  |\n / \\  |\n========="
]

def new_game():
    st.session_state.secret = random.choice(words)
    st.session_state.guessed = []
    st.session_state.wrong = 0
    st.session_state.finished = False

if "secret" not in st.session_state:
    new_game()

# Display the game
st.subheader("Your Word")

display = " ".join(
    letter if letter in st.session_state.guessed else "_"
    for letter in st.session_state.secret
)

st.markdown(f"## {display}")

st.code(stages[st.session_state.wrong])

st.write(f"Wrong attempts: {st.session_state.wrong} / 6")

# Check game status
if display.replace(" ", "") == st.session_state.secret:
    st.success("🎉 Congratulations! You Won!")
    st.write("Correct word:", st.session_state.secret)
    st.session_state.finished = True

elif st.session_state.wrong >= 6:
    st.error("Game Over! You Lost!")
    st.write("Correct word:", st.session_state.secret)
    st.session_state.finished = True

# Letter buttons
if not st.session_state.finished:
    st.write("### Choose a letter")

    for row in ["ABCDEFGHI", "JKLMNOPQR", "STUVWXYZ"]:
        cols = st.columns(len(row))
        for col, letter in zip(cols, row):
            with col:
                if st.button(
                    letter,
                    key=letter,
                    disabled=letter in st.session_state.guessed
                ):
                    st.session_state.guessed.append(letter)

                    if letter not in st.session_state.secret:
                        st.session_state.wrong += 1

                    st.rerun()

if st.button("🔄 Restart Game"):
    new_game()
    st.rerun()