import streamlit as st
import json
import random

# Load the JSON data
def load_data():
    with open('questions.json') as f:
        data = json.load(f)
    categories = list(data.keys())
    return data, categories

data, categories = load_data()

# Flatten the data and randomize the order of the questions
def get_questions(data, selected_category):
    if selected_category == 'All':
        questions = [q for sublist in data.values() for q in sublist]
    else:
        questions = [q for q in data[selected_category]]
    random.shuffle(questions)
    return questions

# Let the user select a category
categories.insert(0, "All")
selected_category = st.selectbox('Select a category', categories)

# Initialize session state variables
if 'category' not in st.session_state:
    st.session_state.category = selected_category
    st.session_state.questions = get_questions(data, selected_category)
elif st.session_state.category != selected_category:
    # The selected category has changed, so update the questions
    st.session_state.category = selected_category
    st.session_state.questions = get_questions(data, selected_category)

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

if 'answer_checked' not in st.session_state:
    st.session_state.answer_checked = False

# Move to the next question
def next_question():
    st.session_state['question_index'] += 1
    if st.session_state['question_index'] >= len(st.session_state['questions']):
        st.session_state['question_index'] = 0
        st.session_state['questions'] = get_questions(data, selected_category)  # Re-randomize the questions
    st.session_state['answer_checked'] = False

current_question = st.session_state['questions'][st.session_state['question_index']]
st.markdown(current_question['question'])

# Displaying the choices in original order
choices = list(current_question['choices'].values())
choice = st.radio("Choices", choices, index=0)

# Button to check the answer
if st.button('Check Answer'):
    correct_answer = current_question['answer']
    text = current_question['reason']

    if choice == correct_answer:
        st.success("Correct!")
        st.session_state['answer_checked'] = True
    else:
        st.error(f"Incorrect. {text}")

# Button to continue to the next question
if st.session_state['answer_checked']:
    if st.button('Continue', on_click=next_question):
        pass  # The next_question function is called when the button is clicked.