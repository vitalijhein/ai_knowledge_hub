import streamlit as st
from datetime import datetime
import sys
import re
import uuid

sys.path.append('C:\\Users\\vital\\streamlit_suite\\src')
from my_utils.mongo_database import MongoDatabase
my_mdb = MongoDatabase()
TODAY = datetime.now().strftime("%d-%m-%y")
def sanitize_key(text):
    """Sanitize the question text to create a valid MongoDB key."""
    # Remove punctuation and replace spaces with underscores
    return re.sub(r'\W+', '_', text).lower()

def upsert_journal_entry(key, journal_type, journal_id_string, formatted_date):
    journal_id = formatted_date + journal_id_string
    # Directly use the value associated with `key` in st.session_state
    journal_entry_value = st.session_state[key]
    
    # Use the `key` itself as a part of the document key in MongoDB, or sanitize another identifier as needed
    sanitized_key = sanitize_key(key)  # Adjust this line as needed

    journal_entry = {sanitized_key: journal_entry_value, "date": formatted_date}

    query_dict = {"id": journal_id}
    update_dict = {"$set": journal_entry}
    
    my_mdb.upsert_into_collection(journal_type, query_dict, update_dict)

def load_existing_entry(journal_type, journal_id_string, formatted_date):
    # Generate the journal_id using the current date and provided id string
    journal_id = formatted_date + journal_id_string

    # Attempt to find the existing entry in the database
    existing_entry = my_mdb.find_the_record_in_col_mdb(journal_type, {"id": journal_id})
    empty_array = []
    if existing_entry:
        # Iterate over each key-value pair in the entry, excluding '_id' and 'id'
        for key, value in existing_entry.items():
            if key not in ('_id', 'id'):  # Exclude MongoDB's _id and the entry's id
                # Assuming keys are in the format '_description_suffix'
                # Split the key on '_' and take everything after the first split as the suffix for text_area
                suffix = key[1:]  # Removes the leading underscore from the key
                st.session_state[f'{key}'] = value  # Populate the session state
                empty_array.append(key)
    return empty_array




def save_to_json(collection_name, journal_id_string, formatted_date):
    journal_id = formatted_date + journal_id_string

    # Create a unique identifier for the journal entry
    journal_entry = {"id": journal_id, "date": formatted_date}
    
    # Collect answers from session state and add them to the journal entry dynamically
    for key, value in st.session_state.items():
        if key.startswith('text_area_'):
            # Extract the part of the key that follows 'text_area_'
            question_suffix = key[len('text_area_'):]
            # Check if the suffix is numeric, indicating it's one of the dynamically created keys
            if question_suffix.isdigit():
                # Use the sanitized key version for MongoDB document
                sanitized_key = f'_question_{question_suffix}'
                journal_entry[sanitized_key] = value
    
    # Construct the query dictionary to find the existing entry
    query_dict = {"id": journal_id}
    # Construct the update dictionary with the new data to upsert
    update_dict = {"$set": journal_entry}
    
    # Add or update the journal entry in the MongoDB collection
    my_mdb.upsert_into_collection(collection_name, query_dict, update_dict)
    
    # Update the journal entries in session state for display or further operations (optional)
    if 'journal_entries' not in st.session_state:
        st.session_state['journal_entries'] = [journal_entry]
    else:
        # Update the existing entry in the session state, if it exists; otherwise, append it
        index = next((index for (index, d) in enumerate(st.session_state['journal_entries']) if d["id"] == journal_id), None)
        if index is not None:
            st.session_state['journal_entries'][index] = journal_entry
        else:
            st.session_state['journal_entries'].append(journal_entry)

def generate_journal_page(questions, journal_type, journal_id_suffix, formatted_date, question_description = None):
    st.header(journal_type)
    #if existing_entry:
    #    keys_sorted = sorted([key for key in existing_entry.keys() if key not in ('_id', 'id')], key=lambda x: int(x.split('__')[-1]))
    #st.write(st.session_state)
    for i, question in enumerate(questions, start=1):
        question_cleaned = sanitize_key(question)
        key = f"{question_cleaned}_{i}"  # Unique key generation
        if key not in st.session_state:
            st.session_state[key] = ""
        
        st.subheader(question)
        # Use the unique key for each text area
        if question_description:
            st.text_area(question_description[i-1], key=key, on_change=upsert_journal_entry, args=(key, journal_type, journal_id_suffix, formatted_date))
        else:
            st.text_area(question, key=key, on_change=upsert_journal_entry, args=(key, journal_type, journal_id_suffix, formatted_date))


def main():
    # get journaling strategy with tabs 
    d = st.date_input("Please select your journal date.", datetime.now().date(), format="DD.MM.YYYY")
    formatted_date = d.strftime('%d.%m.%Y')

    st.write('You selected:', formatted_date)
    tab1, tab2, tab3 = st.tabs(["Morning Pages", "Daily Lists", "Owl"])
    with tab1:
        # Define your questions
        journal_type ="Morning Pages"
        journal_id = "_morning_pages"
        existing_entry = load_existing_entry(journal_type, journal_id, formatted_date)  # Attempt to load existing entry before rendering UI

        questions = [
            "What are you thinking about right now?",
            "What concerns you?",
            "What are your goals?",
            "What did you dream about?",
            "How do you feel?",
            "What do you see around you?",
            "Why do you approach a particular situation the way you do?",
            "Why do you replay certain scenarios the way you do?",
            "Where do you need help?",
            "What can you do to make yourself feel good?",
            "What are your values and why?",
            "What journey are you on?",
            "What is really annoying you right now?",
            "What made you smile?",
            "What are you grateful for?",
            "What do you like about yourself?",
            "Where do you want to be heading?",
            "What have you learned recently?"
        ]
        generate_journal_page(questions, journal_type,journal_id, formatted_date)
        # Optionally, add the button at the end of the journaling tab or at the end of all tabs
        if st.button('Save Journal Entry', key='save'+ journal_id):
            save_to_json(journal_type, journal_id, formatted_date)
    with tab2:
        # Define your questions
        journal_type ="Lists"
        journal_id = "_lists"
        load_existing_entry(journal_type, journal_id, formatted_date)  # Attempt to load existing entry before rendering UI

        questions = [
            "Favorite books and your current reads, reviews and lists of recommendations",
            "Favorite films and Netflix series, what you’re watching now and your to-watch list",
            "Favorite meals, recipes, must-try dishes, restaurant reviews.",
            "Fitness routine and tracker.",
            "News items or thought-provoking stories that spark your interest",
            "Home improvement log, what needs to be done, supplies to buy"
        ]
        generate_journal_page(questions, journal_type, journal_id, formatted_date)
        

        # Optionally, add the button at the end of the journaling tab or at the end of all tabs
        if st.button('Save Journal Entry', key='save'+ journal_id):
            save_to_json(journal_type, journal_id, formatted_date)

    with tab3:
        journal_type ="Knowledge Work"
        journal_id = "_knowledgework"
        load_existing_entry(journal_type, journal_id, formatted_date)  # Attempt to load existing entry before rendering UI

        questions = [
            "What is the core lesson or insight?",
            "Set the scence with personal experience or observation.",
            "Share the Journey",
            "Unveil the Outcome",
            "Extract the Universal Lesson",
            "Encourage Reflection",
            "Polish with Relatable Analogies and Metaphors",
            "Engage with Visuals and Examples"
        ]
        
        question_description = [
            "Start by pinpointing the main takeaway or lesson you want your readers to gain from your post. This could be a programming concept, a problem-solving strategy, or a personal development insight gained through your work.",
            """Begin your story by setting the context. This could involve describing a particular challenge you faced in your project, the initial setbacks, or your thought process at the beginning. The aim is to draw your readers into the situation as if they were experiencing it themselves.""",
            """Dive into the narrative of your journey. This part should cover:\n\n
- The challenges: Detail the specific problems or obstacles you encountered.\n
- The actions: Describe the steps you took to address these challenges. This is a great place to incorporate technical knowledge or project-specific strategies you applied.\n
- The learning moments: Highlight any moments of realization or insight that were pivotal to your progress.""",
            "Reveal the result of your efforts. This doesn’t always have to be a success story; sometimes, the most valuable lessons come from failure. The key is to share what you learned and how it changed your approach or understanding.",
            "Distill the unique, project-specific experience into a broader lesson that readers can apply in their own lives or work. This helps connect your personal story back to the core insight you identified at the beginning.",
            "End your post by prompting readers to reflect on their own experiences or challenges. Ask questions or propose actions they can take based on the lessons shared. This not only makes your post more interactive but also encourages readers to apply what they've learned.",
            "Throughout your post, use analogies, metaphors, and simple language to explain complex concepts. This makes your content more accessible and engaging to a wider audience.",
            "Wherever possible, include diagrams, code snippets, screenshots, or before-and-after comparisons to visually complement your narrative. This helps break down information and makes it easier for readers to follow along."
        ]
        generate_journal_page(questions, journal_type, journal_id, formatted_date, question_description)
        

        # Optionally, add the button at the end of the journaling tab or at the end of all tabs
        if st.button('Save Journal Entry', key='save'+ journal_id):
            save_to_json(journal_type, journal_id, formatted_date)


if __name__ == "__main__":
    main()