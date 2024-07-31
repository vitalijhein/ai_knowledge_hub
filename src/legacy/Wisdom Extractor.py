from openai import OpenAI
import streamlit as st
import os
import requests
directory= 'downloads/'
if not os.path.exists(directory):
    os.makedirs(directory)

st.set_page_config(page_title="PDSGN ", page_icon="🚀", layout="wide", )     
OPENAI_API_KEY = ""
CLIENT_OPENAI = OpenAI(api_key=OPENAI_API_KEY)
NOTION_TOKEN = ""
DATABASE_ID = ""

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

@st.cache_data()
def create_prompt(desired_output):
    prompt = f"""
You extract surprising, insightful, and interesting information from text content. You are interested in insights related to the purpose and meaning of life, human flourishing, the role of technology in the future of humanity, artificial intelligence and its affect on humans, memes, learning, reading, books, continuous improvement, and similar topics.

Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

STEPS
1. Extract a summary of the content in 50 words or less, including who is presenting and the content being discussed into a section called SUMMARY.
2. Extract 20 to 50 of the most surprising, insightful, and/or interesting ideas from the input in a section called IDEAS:. If there are less than 50 then collect all of them. Make sure you extract at least 20.
3. Extract 15 to 30 of the most surprising, insightful, and/or interesting quotes from the input into a section called QUOTES:. Use the exact quote text from the input.
4. Extract 15 to 30 of the most practical and useful personal habits of the speakers, or mentioned by the speakers, in the connt into a section called HABITS. Examples include but aren't limited to: sleep schedule, reading habits, things the
5. Extract 15 to 30 of the most surprising, insightful, and/or interesting valid facts about the greater world that were mentioned in the content into a section called FACTS:.
6. Extract all mentions of writing, art, tools, projects and other sources of inspiration mentioned by the speakers into a section called REFERENCES. This should include any and all references to something that the speaker mentioned.
7. Extract the 15 to 30 of the most surprising, insightful, and/or interesting recommendations that can be collected from the content into a section called RECOMMENDATIONS.

OUTPUT INSTRUCTIONS
Only output Markdown.
Extract at least 20 ideas from the content.
Extract at least 10 items for the other output sections.
Do not give warnings or notes; only output the requested sections.
You use bulleted lists for output, not numbered lists.
Do not repeat ideas, quotes, facts, or resources.
Do not start items with the same opening words.
Ensure you follow ALL these instructions when creating your output.

INPUT
INPUT:
"""


    messages = [{"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": "Content:\n" + f"{desired_output}"}]


    response = CLIENT_OPENAI.chat.completions.create(
          model="gpt-4-1106-preview",
          #model="gpt-3.5-turbo-1106",
          messages=messages,
          seed=123,
          temperature=0.5,
          top_p=0.5,
          timeout=120,
    )
    output = response.choices[0].message.content
    return output




# Function to append blocks to an existing page
@st.cache_data()
def append_blocks_to_page(page_id, blocks):
     # Create a block for the YouTube video
    #blocks.append(youtube_url)
    append_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.patch(append_url, json={"children": blocks}, headers=headers)
    print(response)
    return response.json()

@st.cache_data()
def create_page(video_title, chunks):
    # Create the initial data payload with the first chunk
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": video_title,  # replace with your actual title
                        },
                    },
                ],
            },
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": chunks[0]}}]
                }
            }
        ]
    }
    create_url = "https://api.notion.com/v1/pages"
    response = requests.post(create_url, json=data, headers=headers)
    return response.json()

@st.cache_data()
def split_content(content, chunk_size=1900):
    return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

st.title("Book Extractor 🚀")
desired_outcome = st.text_input("Paste article contents here 👇", placeholder='You articles content...')
title = st.text_input("Paste article title here 👇", placeholder='You articles content...')

if st.button("Start"):
    output_openai = create_prompt(desired_outcome)
    st.write(output_openai)

    chunks = split_content(output_openai)
    # Create the first page

    first_page_response = create_page(title, chunks)
    first_page_id = first_page_response.get("id")
    # Append remaining chunks to the page
    for chunk in chunks[1:]:
        block = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}]
            }
        }
        append_blocks_to_page(first_page_id, [block])



def to_obsidian():
    system_prompt_to_obsidian = """
Write detailed notes on a specific topic, adhering to the following structure and guidelines.
The goal is to produce notes that are not only informative and well-structured but also engaging and easy to navigate. Through this method, you aim to facilitate a deeper understanding of the topic and stimulate curiosity for further exploration.

Guidelines:
1. Title Creation: Craft a title that is both succinct and descriptive, effectively summarizing the main idea of the notes. The title should immediately convey the core subject matter to the reader. For instance, a title like "Product and Media Are New Leverage" clearly communicates that the discussion will revolve around the innovative use of products and media as leverage tools.
2. Explanation and Context: Begin with an introductory sentence that sets the stage for the in-depth discussion. This should introduce the key concepts being explored, such as Digital Product, media, and leverage. Provide an overview that elucidates why these concepts are significant and how they interconnect. This foundational explanation is crucial for preparing the reader for the detailed examination that follows.
3. Use of [[Double Brackets]] for Key Terms: Utilize [[double brackets]] to emphasize critical terms or concepts throughout the notes. This method not only highlights essential ideas but also signals to the reader that these terms are pivotal for understanding the broader discussion or for potential further exploration within a larger database or collection of notes.Select terms that are vital to the discussion for this special notation, especially those you plan to detail further in related notes.
4. Bullet Points for Subtopics: Organize the main topic into distinct subtopics or thematic areas, presented as bullet points. Each bullet should address a different facet of the primary topic. Introduce each bullet point with a bolded subheading that succinctly captures the essence of the subtopic, aiding in the organizational clarity and scan-ability of the notes. Offer a brief yet informative explanation for each subtopic, ensuring relevance to the main theme. Aim for conciseness to maintain focus and avoid diluting the primary message.
5. Clarity and Brevity: Employ clear, straightforward language to express complex ideas, making the content accessible to readers with varying degrees of familiarity with the subject matter.
Strive for brevity in your explanations, ensuring each bullet point serves as a compact summary that, while standalone, also complements the overarching theme of the notes.

Input: 
"""

def find_md_files(directory = "C:\Users\v.hein\iCloudDrive\iCloud~md~obsidian\new_vault"):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append((file, os.path.join(root, file)))
    return md_files

# Example usage
directory_path = '/path/to/your/directory'  # Change this to the directory you want to search
markdown_files = find_md_files(directory_path)

for file_name, file_path in markdown_files:
    print(f'File Name: {file_name}, Path: {file_path}')



def to_obsidian():
    system_prompt_to_obsidian = """
Write detailed notes on a specific topic, adhering to the following structure and guidelines.
The goal is to produce notes that are not only informative and well-structured but also engaging and easy to navigate. Through this method, you aim to facilitate a deeper understanding of the topic and stimulate curiosity for further exploration.

Guidelines:
1. Title Creation: Craft a title that is both succinct and descriptive, effectively summarizing the main idea of the notes. The title should immediately convey the core subject matter to the reader. For instance, a title like "Product and Media Are New Leverage" clearly communicates that the discussion will revolve around the innovative use of products and media as leverage tools.
2. Explanation and Context: Begin with an introductory sentence that sets the stage for the in-depth discussion. This should introduce the key concepts being explored, such as Digital Product, media, and leverage. Provide an overview that elucidates why these concepts are significant and how they interconnect. This foundational explanation is crucial for preparing the reader for the detailed examination that follows.
3. Use of [[Double Brackets]] for Key Terms: Utilize [[double brackets]] to emphasize critical terms or concepts throughout the notes. This method not only highlights essential ideas but also signals to the reader that these terms are pivotal for understanding the broader discussion or for potential further exploration within a larger database or collection of notes.Select terms that are vital to the discussion for this special notation, especially those you plan to detail further in related notes.
4. Bullet Points for Subtopics: Organize the main topic into distinct subtopics or thematic areas, presented as bullet points. Each bullet should address a different facet of the primary topic. Introduce each bullet point with a bolded subheading that succinctly captures the essence of the subtopic, aiding in the organizational clarity and scan-ability of the notes. Offer a brief yet informative explanation for each subtopic, ensuring relevance to the main theme. Aim for conciseness to maintain focus and avoid diluting the primary message.
5. Clarity and Brevity: Employ clear, straightforward language to express complex ideas, making the content accessible to readers with varying degrees of familiarity with the subject matter.
Strive for brevity in your explanations, ensuring each bullet point serves as a compact summary that, while standalone, also complements the overarching theme of the notes.

Input: 
"""
