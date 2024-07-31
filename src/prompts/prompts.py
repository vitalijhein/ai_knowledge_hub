
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from typing import Dict

class Questions(BaseModel):
    questions: Dict[str, str] = Field(
        ..., 
        description="Dynamic dictionary to store an arbitrary number of questions."
    )

class Prompts:
    def __init__(self):
        pass

    def get_actionable_single_tweet(self):
        actionable_tweet = ChatPromptTemplate.from_template("""Please write 5 tweets about the input, where each tweet following the "Tweet-Why-How-Snap" framework, all written in a tone that's confident, knowledgeable, and helpful.

For context:
[ I am an individual deeply rooted in Business Informatics, with a substantial focus on AI, entrepreneurship, and personal growth. My journey has led me from founding a successful digital marketing agency to consulting for startups, all while engaging in real-world problem-solving through AI and digital strategies. Currently, my passion lies in sharing my insights and experiences related to AI applications in business, entrepreneurship, personal growth, and practical problem-solving techniques. My ultimate goal is to redefine success by integrating technology, business acumen, and personal development, promoting a lifestyle of personal freedom and meaningful work. Through my content, I aim to guide and inspire both individuals and businesses to navigate the complexities of digital transformation effectively.]

The "What-Why-How-Snap" framework is a 4-part framework for every individual tweet. It works like this:
"What": The first part of the tweet stating what you are talking about in less than 9 words. This can be a tip, a resource, or something else.
"Why": Logically explains why the "What" is relevant in 8 words or less. Can't begin with "to" or "this".
"How": 3-5 actionable steps on 2-5 words each  on how the audience can implement the advice
"Snap": a short, sequence that wraps up the tweet with a takeaway, wise quote, or lesson. Reading the "snap" should leave the reader with a sense of satisfaction.

Example "What-Why-How-Snap" -Tweet:
[TWEET] Dive into continuous learning for skill mastery. It's essential for personal and professional growth. Start with theory to understand the basics. Then, apply what you've learned through action. Reflect on your experiences to deepen your knowledge. Mastery is a journey, not a destination.
[TWEET] Theory is your learning foundation. It gives you the groundwork for new skills. Read books, attend workshops, and listen to experts. This builds a solid base for your learning journey. Theory turns the unknown into a map for exploration.
[TWEET] Action transforms knowledge into skill. It's where theory meets reality. Practice regularly, apply concepts in real-life scenarios, and don't fear mistakes. Action is the bridge between 'knowing' and 'doing'. Walk it with confidence.
[TWEET] Reflection is key to learning. It turns experience into insight. After action, take time to think about what worked and what didn't. Ask questions, seek feedback, and adjust your approach. Reflection turns experience into wisdom.
[TWEET] Continuous learning is a cycle of growth. It combines theory, action, and reflection. Engage with new ideas, put them into practice, and think about your experiences. This cycle keeps you growing, adapting, and thriving in any field. Keep the wheel turning for endless progress.

INPUT:
[{tweet}]

Constraints:
1. No hashtags
2. Readability grade 7 or lower
3. Every tweet consists of 250-280 characters
4. No emojis
5. Use concise language
6. Each tweet should follow the "What-Why-How-Snap" framework
7. Use complete sentences and emphasize benefits over features.
8. Use active voice

Remember to make each tweet engaging and informative. Assume the reader doesn't know anything about the topic yet, so please make sure to give context to any new terms or principles.

Start each tweet with [TWEET] without spelling out the framework parts themselves.
"""
        )
        return actionable_tweet  
     
    def get_actionable_posters(self):
        model = ChatOpenAI(model="gpt-3.5-turbo-16k-0613", temperature=0.24, max_tokens=2500, model_kwargs={"top_p": 0.8})
        actionable_posters = ChatPromptTemplate.from_template("""I want you to write 5 "actionable posters" for me.

"actionable posters" are texts that are published on social media platforms like LinkedIn.

They are characterized by the following traits:
1) They are highly actionable for a special target audience
2) They are easy to read and skim
3) They have intriguing hooks
4) They are concise and compelling

Here are examples of past successful "actionable posters", separated by [NEW POST]:

[NEW POST]

Ever felt stuck in the learning loop, endlessly consuming theory but seeing no real progress? Break the cycle with this simple yet powerful approach:

1. Dedicate 30% of your time to learning theory.
2. Allocate 50% to hands-on practice.
3. Reserve 20% for reflection and adjustment.

Why? Because real growth happens when you apply what you've learned. Engage with a community or find a coach to amplify your journey. Remember, the perfect balance between theory, action, and reflection accelerates skill acquisition. Are you ready to shift gears and see real results?

[NEW POST]

Struggling to make your learning stick? Here's a secret: The social dimension of learning is not just beneficial; it's crucial. Here's how to leverage it:

1. Join a niche community with the same learning goals.
2. Share your progress and challenges.
3. Seek out a mentor or coach for personalized guidance.

This approach not only deepens your understanding but also keeps you accountable. Plus, personalized advice from a coach can save you time by focusing on what truly matters. How will you incorporate the social aspect into your learning today?

[NEW POST]

Feeling overwhelmed by the vast sea of theories in your field? Simplify your learning with this strategy:

1. Identify the top 3 theories most relevant to your goals.
2. Apply these theories in a small project or practice session.
3. Reflect on the outcomes and seek feedback.

By narrowing your focus, you not only make learning manageable but also ensure you're building skills that directly contribute to your goals. Remember, depth over breadth is key to mastery. What theory will you put into action this week?

[NEW POST]

Ever wonder why some people excel at new skills while others stagnate? The secret lies in the cycle of continuous improvement:

1. Learn a new concept.
2. Immediately apply it in a real-world scenario.
3. Reflect on the experience and gather feedback.
4. Adjust your approach and repeat.

This cycle ensures that you're not just passively absorbing information but actively engaging with it, leading to deeper understanding and skill retention. Ready to transform your learning into tangible results?

[NEW POST]

Unlock the full potential of your learning with this game-changing approach:

1. Start with a clear goal in mind.
2. Engage in targeted learning, focusing only on what moves you closer to your goal.
3. Implement what you've learned immediately, no matter how small the step.
4. Reflect on your actions, seeking feedback and adjusting as necessary.

This method ensures that every bit of theory is tied to practical application, making your learning journey efficient and effective. Are you prepared to streamline your learning and achieve your goals faster?

---

Constraints:
1) No emojis
2) No hashtags
3) Use numbers
4) Be ultra-specific and elaborate in your advice, but keep it ultra-concise. For example, rather than saying "Let AI draft content", say "Use ChatGPT to create 85% good drafts"
5) You can be a bit inspirational and motivational, but don't overdo it. For example, "Take the leap. Start small, dream big. In no time, you'll be an expert in AI-assisted writing. It's easier than you think." sounds cringe, while "Highlight the VALUE to inspire ACTION. A simple shift in perspective can lead to profound changes in your writing." sounds great.
6) Conclude with a takeaway or a question to the audience
7) Don't write about AI.

My Input for the actionable posters:
[{tweet}]

Now, do this:
1) Silently analyse the "actionable posters" I gave you
2) Silently analyse the INPUT gave you and think about ideas compelling to my audience
3) Use your insights from 1) and 2)  with the characteristics I gave you and write 5 "actionable posts" that are insanely valuable to my audience
""" 
        )
        return actionable_posters, model
        
    def get_asci_art_prompt(self):
        model = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0, max_tokens=4096, model_kwargs={"top_p": 0.9})
        ascri_prompt = ChatPromptTemplate.from_template("""You are an expert at data and concept visualization and in turning complex ideas into a form that can be visualized using ASCII art.

You take input of any type and find the best way to simply visualize or demonstrate the core ideas using ASCII art.

You always output ASCII art, even if you have to simplify the input concepts to a point where it can be visualized using ASCII art.

STEPS
1. Take the input given and create a visualization that best explains it using elaborate and intricate ASCII art.
2. Ensure that the visual would work as a standalone diagram that would fully convey the concept(s).
3. Use visual elements such as boxes and arrows and labels (and whatever else) to show the relationships between the data, the concepts, and whatever else, when appropriate.
4. Use as much space, character types, and intricate detail as you need to make the visualization as clear as possible.
5. Create far more intricate and more elaborate and larger visualizations for concepts that are more complex or have more data.
6. Under the ASCII art, output a section called VISUAL EXPLANATION that explains in a set of 10-word bullets how the input was turned into the visualization. Ensure that the explanation and the diagram perfectly match, and if they don't redo the diagram.
7. If the visualization covers too many things, summarize it into it's primary takeaway and visualize that instead.
8. DO NOT COMPLAIN AND GIVE UP. If it's hard, just try harder or simplify the concept and create the diagram for the upleveled concept.
9. If it's still too hard, create a piece of ASCII art that represents the idea artistically rather than technically.

OUTPUT INSTRUCTIONS
DO NOT COMPLAIN. Just make an image. If it's too complex for a simple ASCII image, reduce the image's complexity until it can be rendered using ASCII.
DO NOT COMPLAIN. Make a printable image no matter what.
Do not output any code indicators like backticks or code blocks or anything.
You only ouptut the printable portion of the ASCII art. You do not ouptut the non-printable characters.
Ensure the visualization can stand alone as a diagram that fully conveys the concept(s), and that it perfectly matches a written explanation of the concepts themselves. Start over if it can't.
Ensure all output ASCII art characters are fully printable and viewable.
Ensure the diagram will fit within a reasonable width in a large window, so the viewer won't have to reduce the font like 1000 times.
Create a diagram no matter what, using the STEPS above to determine which type.
Do not output blank lines or lines full of unprintable / invisible characters. Only output the printable portion of the ASCII art.

INPUT:
{tweet}
"""
        )
        return ascri_prompt, model
            

    def get_personal_tweets(self):
        system = """I want you to write "irresistible personal tweets" for me.

These tweets are characterised by being extremely original and unique. They always include one reference, fact, opinion, or experience by the author. 

Come up with uncommon, varied results.

Here are some examples of "irresistible personal tweets", separated by [NEW TWEET].

[NEW TWEET]

People's attention spans are FUCKED.

This is why I created a SUPER basic landing page for my course waitlist.

My thoughts:

Give them a short, bite-size overview instead of a long sales page.

Write everything like a tweet.

Result :

The landing page converts at almost 80%.

[NEW TWEET]

I battled with anxiety throughout most of my life.

I fucked up life-changing money on FTX.

I changed my career 2 times before seeing any success.

I wake up often doubting if I can do it.

But I just don't give up.

If I can make shit happen, you can too.

[NEW TWEET]

I posted 20,000 times before I got my first client.

[NEW TWEET]

If you could choose between two teachers:

1. The Natural

2. The Non-Natural

And they're both equally skilled,

I'd go with the Non-Natural.

A Natural is good at the talent but can struggle teaching it.

A Non-Natural is a great teacher because he wasn't born with the talent.

[NEW TWEET]

Some premium Twitter bro advice I’ve seen lately:

- Smoke cigs to focus
- Take 4 hour ice baths
- Stare at the sun for energy

Have a day off

What’s is going to be next?

“Inhale paint fumes for creativity”

[NEW TWEET]:

You make money.

People say you're scamming.

You get jacked.

People say you're on roids.

You grow a following.

People say you bought 'em.

People will talk shit regardless, so do whatever the fuck makes you happy.

[NEW TWEET]

I escaped the matrix and made a full-time online income when I was 23.

I achieved it by doing the opposite of my peers.

I chose self-education over college.

I paid for mentors instead of a new car.

I prioritized building instead of partying.

A few life-changing choices.

---

Now, do this:

1) Learn what tone of voice and structure characterises "irresistible personal tweets"
2) Learn my tone of voice from my past tweets
3) Learn about me & my experiences from my past tweets
5) Based on the constraints I gave you, write 20 new "irresistible personal tweets" in my tone of voice for me

Constraints for the tweets:

1 No hashtags
2 No emojis
3 Include at least 1 personal reference, fact, or experience
4 Use complete sentences
5 Must be shorter than 280 characters
6 no questions
"""

        user = """Love is a powerful force that enriches human experiences and contributes to a fulfilling life. Show affection, practice forgiveness, and prioritize the well-being of others to experience the benefits of love. Love fosters empathy, understanding, and connection between individuals.

Topic Ideas for the Tweets:
{tweet}

Constraints for the tweets:
1 No hashtags
2 No emojis
3 Include at least 1 personal reference, fact, or experience
4 Use complete sentences
5 Must be shorter than 280 characters
6 no questions
"""
        return system, user

    def get_summary_questions_prompt(self):        
        parser = JsonOutputParser(pydantic_object=Questions)

        question_extraction_prompt = ChatPromptTemplate.from_template(
            template = """
                You extract surprising, insightful, and interesting questions from text content. You are focused on asking as many questions as needed to encapsulate the entire meaning of the given content. To clarify: Your questions do cover the given content comprehensively, ensuring that no further question can be asked without seeking new information.

                Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

                Steps:
                1. Extract 5-150 questions that encapsulate the entire meaning of the given context in a section called QUESTIONS.

                OUTPUT INSTRUCTIONS
                {format_instructions}

                Input:
                {transcript}
                """,
                partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        return question_extraction_prompt

    def get_article_summary_prompt(self):
        article_summary_prompt = ChatPromptTemplate.from_template(
            """
            You extract surprising, insightful, and interesting information from text content. You are interested in insights related to the purpose and meaning of life, human flourishing, the role of technology in the future of humanity, artificial intelligence and its affect on humans, memes, learning, reading, books, continuous improvement, and similar topics.

            Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

            STEPS
            1. Extract up to 15-50 of the most important, insightful, and/or interesting key points in a section called KEYPOINTS. If there are less than 15 then collect all of them. Make sure you extract at least 15.
            2. Extract up to 5-30 of the most important, insightful, and/or supporting arguments in a section called ARGUMENTS. If there are less than 5 then collect all of them. Make sure you extract at least 5.
            3. Extract up to 5-20 of the most important and/or insightful conclusions in a section called CONCLUSIONS. If there are less than 5 then collect all of them. Make sure you extract at least 5.
            4. Identify the author's purpose for writing the article. This could include informing, persuading, entertaining, or a combination of these. Capture this in a section called PURPOSE.
            5. Determine the intended audience of the article. Consider who the article is directed towards, such as professionals in a specific field, general readers, students, etc. Summarize this in a section called AUDIENCE.    
            6. Extract up to 10-30 examples of evidence that directly support the main ideas in a section called EVIDENCE. If there are less than 10 examples, collect all of them. Aim to include at least 10 pieces of evidence.
            7. Identify up to 5-15 specific examples or case studies mentioned in the article in a section called EXAMPLES. If fewer examples are provided, include all available. Ensure you capture at least 5 examples.
            8. Note down up to 5-20 data points, statistics, or research findings that bolster the article's arguments in a section called DATA. If there are less than 5 data points, document all. Strive to extract at least 5 significant data points.
            9. Document up to 5-15 insights on the strengths of the author's arguments in a section called STRENGTHS. If there are fewer than 5 strengths, list all identified. Ensure at least 5 strengths are detailed.
            10. Identify up to 5-15 points regarding the weaknesses or limitations of the author's arguments in a section called WEAKNESSES. If fewer weaknesses are found, include all. Aim to extract at least 5 weaknesses.
            10. Note down up to 3-10 observations on potential biases in the author's perspective or argumentation in a section called BIASES. This includes any noticeable lack of balance, preference for certain viewpoints, or omission of relevant information. If there are less than 3 biases, document all detected biases, with a minimum goal of identifying 3.
            11. Compile up to 5-15 critical questions raised by the article's content or its approach in a section called QUESTIONS. These questions should highlight areas for further inquiry or aspects that the article does not address. If there are fewer than 5 questions, list all that arise. Ensure to identify at least 5 thought-provoking questions.
            12. Identify up to 5-10 notable gaps in the article's coverage or argumentation in a section called GAPS. These gaps could pertain to unaddressed topics, overlooked perspectives, or areas lacking sufficient detail. If there are fewer than 5 gaps, document all observed gaps. Aim to pinpoint at least 5 significant gaps.
            13. For each identified question or gap, briefly outline potential ways these could be explored or addressed in your blog articles, in a section called EXPLORATION AVENUES. This includes suggesting research directions, perspectives to consider, or related topics that could fill the identified gaps or answer the raised questions.
            
            OUTPUT INSTRUCTIONS
            - Only output Markdown.
            - Extract at least 15 KEYPOINTS answered from the content as Markdown H1 headers.
            - Extract at least 5 ARGUMENTS answered from the content as Markdown H1 headers.
            - Extract at least 5 KEYPOINTS answered from the content as Markdown H1 headers.
            - Extract the AUTHOR'S PURPOSE for writing the article as Markdown H1 headers.
            - Extract the AUDIENCE for writing the article as Markdown H1 headers.
            - Extract at least 10 EVIDENCE answered from the content as Markdown H1 headers.
            - Extract at least 5 EXAMPLES answered from the content as Markdown H1 headers.
            - Extract at least 5 DATA answered from the content as Markdown H1 headers.
            - Extract at least 5 STRENGTHS answered from the content as Markdown H1 headers.
            - Extract at least 5 WEAKNESSES answered from the content as Markdown H1 headers.
            - Extract at least 5 BIASES answered from the content as Markdown H1 headers.
            - Extract at least 5 QUESTIONS answered from the content as Markdown H1 headers.
            - Extract at least 5 GAPS answered from the content as Markdown H1 headers.
            - Extract at least 5 EXPLORATION AVENUES answered from the content as Markdown H1 headers.
            - Do not give warnings or notes; only output the requested sections.
            - You use bulleted lists for output, not numbered lists.
            - Do not repeat key points, arguments or conclusions
            - Ensure you follow ALL these instructions when creating your output.

            INPUT
            {article}
            """
        )
        return article_summary_prompt

    def get_keyinfos_from_article(self):
        article_key_info_prompt = ChatPromptTemplate.from_template("""
            You extract surprising, insightful, and interesting information from text content. Identify the Main Ideas Of the Article.

            Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

            STEPS:
            1. Extract up to 15-50 of the most important, insightful, and/or interesting key points in a section called KEYPOINTS. If there are less than 15 then collect all of them. Make sure you extract at least 15.
            2. Extract up to 5-30 of the most important, insightful, and/or supporting arguments in a section called ARGUMENTS. If there are less than 5 then collect all of them. Make sure you extract at least 5.
            3. Extract up to 5-20 of the most important and/or insightful conclusions in a section called CONCLUSIONS. If there are less than 5 then collect all of them. Make sure you extract at least 5.

            OUTPUT INSTRUCTIONS
            - Only output Markdown.
            - Extract at least 15 KEYPOINTS answered from the content as Markdown H1 headers.
            - Extract at least 5 ARGUMENTS answered from the content as Markdown H1 headers.
            - Extract at least 5 KEYPOINTS answered from the content as Markdown H1 headers.
            - Do not give warnings or notes; only output the requested sections.
            - You use bulleted lists for output, not numbered lists.
            - Do not repeat key points, arguments or conclusions.
            - Ensure you follow ALL these instructions when creating your output.

            INPUT
            {article}
            """
        )
        return article_key_info_prompt

    def process_questions_from_transcript(self):
        transcript_questions_prompt = ChatPromptTemplate.from_template(
            """
            Read the provided transcript and answer the provided question based on the information in the transcript. 

            Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

            INPUT
            {transcript}

            Question 
            {question}
            """
        )
        
        return transcript_questions_prompt

    def get_questions_from_transcript_as_dict(self):
        parser = JsonOutputParser(pydantic_object=Questions)

        question_extraction_prompt = ChatPromptTemplate.from_template(
            template = """
                You extract surprising, insightful, and interesting information from text content. You are interested in insights related to the purpose and meaning of life, human flourishing, the role of technology in the future of humanity, artificial intelligence and its affect on humans, memes, learning, reading, books, continuous improvement, and similar topics.

                Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

                STEPS
                1. Extract up to 50 of the most important, insightful, and/or interesting answered question in the input in a section called questions. If there are less than 15 then collect all of them. Make sure you extract at least 3.

                OUTPUT INSTRUCTIONS
                {format_instructions}

                Input:
                {transcript}
                """,
                partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        return question_extraction_prompt
    
    
    def get_tweets_from_transcript_as_dict(self, parser):
        question_extraction_prompt = ChatPromptTemplate.from_template(
            template = """
                You extract headlines, bullets and conclusions from tweets.

                Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

                STEPS
                1. Extract the headline from the tweet.
                2. Extract the bullets from the tweet.
                3. Extract the conclusion from the tweet.

                OUTPUT INSTRUCTIONS
                {format_instructions}

                Input:
                {tweet}
                """,
                partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        return question_extraction_prompt
    
    def get_framework_from_article(self):
        article_key_info_prompt = ChatPromptTemplate.from_template("""
            You compile surprising, insightful, and interesting frameworks from text content. You are interested in insights related to the purpose and meaning of life, human flourishing, the role of technology in the future of humanity, artificial intelligence and its affect on humans, memes, learning, reading, books, continuous improvement, and similar topics.
                        
            Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

            STEPS:
            1. From the provided content, identify the single most crucial framework that serves as the foundation of the article. This framework should embody the central concept, theory, or idea that the article seeks to communicate. Summarize this framework succinctly in a section titled "FRAMEWORK."
            2. Develop a comprehensive explanation of the identified framework in a section titled "EXPLANATION." This explanation should consist of detailed points, aiming for a range between 20 to 250, depending on the content's complexity. Follow these guidelines to ensure the explanation meets the desired depth:
            2.1 Begin with foundational aspects of the framework. Explain key terms, principles, and premises that are essential for understanding the more complex ideas that follow
            2.2 Each bullet point should naturally follow from the previous, gradually increasing in complexity or branching into subtopics. This approach helps in layering the information, making it easier for the reader to grasp how different parts of the framework interconnect.
            2.3 Wherever possible, incorporate examples, case studies, or analogies to illustrate how theoretical aspects of the framework apply in practical scenarios. This can also help in breaking down complex ideas into more relatable concepts.
            2.4 Detail Mechanisms and Processes: Instead of stating what functions or roles components play, delve into how these functions are performed. Describe the mechanisms, processes, and interactions that underlie the observable phenomena or outcomes.
            2.5 Discuss the broader implications of the framework. How does it impact the field it belongs to? What are the potential consequences of adopting or ignoring this framework in real-world scenarios?
            2.6 While aiming for depth, maintain clarity in your explanations. Avoid jargon unless explained, and ensure that the progression from one point to the next is smooth and logical.
            
            OUTPUT INSTRUCTIONS
            - Only output Markdown.
            - Derive the framework from the content as Markdown H1 headers.
            - Extract at least 20-250 bullets that explain in great detail the framework from the content as Markdown H1 headers.
            - Do not give warnings or notes; only output the requested sections.
            - You use bulleted lists for output, not numbered lists.
            - Do not repeat framework, and framework explanations.
            - Ensure you follow ALL these instructions when creating your output.

            INPUT
            {article}
            """
        )
        return article_key_info_prompt
    
    
    def get_actionable_tweet_draft_step1(self):
        actionable_tweet_draft_prompt = ChatPromptTemplate.from_template("""


Please expand it into a Twitter thread following the "Tweet-Why-How-Snap" framework, all written in a tone that's confident, knowledgeable, and helpful.

Constraints:
1. No hashtags
2. Readability grade 7 or lower
3. Every tweet consists of 250-280 characters
4. No emojis
5. Use concise language
6. Each tweet in the thread should follow the "What-Why-How-Snap" framework
7. Use complete sentences and emphasize benefits over features.
8. Use active voice


The "What-Why-How-Snap" framework is a 4-part framework for every individual tweet in the thread. It works like this:
"What": The first part of the tweet stating what you are talking about in less than 9 words. This can be a tip, a resource, or something else.
"Why": Logically explains why the "What" is relevant in 8 words or less. Can't begin with "to" or "this".
"How": 3-5 actionable steps on 2-5 words each in bullet points “•” on how the audience can implement the advice
"Snap": a short, sequence that wraps up the tweet with a takeaway, wise quote, or lesson. Reading the "snap" should leave the reader with a sense of satisfaction.

Remember to make each tweet engaging and informative. Assume the reader doesn't know anything about the topic yet, so please make sure to give context to any new terms or principles.

In your output, provide the thread without spelling out the framework parts themselves.

The format should be:
Headline (my input)
5-6 following tweets in the format I teached you.

Here's 2 example of a great thread where every tweet follows the "What-Why-How-Snap" framework:

EXAMPLE 1:

How to finish more work in 2 hours than 95'%' of people do in 2 weeks:

- -

Create a focus playlist.

Try these soundtracks:

- Drive
- Dune
- TENET
- Dunkirk
- Ad Astra
- Inception
- Interstellar
- The Batman
- Cyberpunk 2077
- Blade Runner 2049
- The Dark Knight Trilogy

Your brain will get into deep work 2x faster.

- -

Prime yourself.

Prepare your mind for the activity.

8 hours of sleep primes you to focus.

30 minutes of reading primes you to write.

10 minutes of planning primes you to organize.

Short-term preparation leads to long-term success.

- -

Schedule deep work sessions for 1.5 to 2 hours.

Why?

1) It takes 20-30 minutes to get into flow state

2) It takes around 1.5-2 hours before your focus declines

Take a break too early, you won’t get into flow.

But if you don't take a break, you'll work inefficiently.

- -

Separate tasks based on their type.

Batch analytical tasks together:

- Organization
- Research
- Planning

Batch creative tasks together:

- Writing
- Designing
- Brainstorming

Your brain wastes energy to adjust when you switch from task to task.

- -

Remove distractions.

Too much noise?

Use noise-cancelling earbuds.

Distracting websites?

Use a website/app blocker.

Too much going at home?

Go to a coffee shop.

It's impossible to get distracted when it's not an option.

- -

Set 1 goal for each work block.

Break it into 3 actionable tasks.

Now, focus on 1 task at a time.

When you complete it, move to the next.

Knowing what you need to do prevents you from getting distracted with “busy” work.

- -

Reflect.

After your work sessions, look at what you can improve.

Do you need to:

- Change the length of time?
- Do certain tasks before others?
- Work at a different part of the day?

Optimize for the next session.

- -

Reward yourself.

Do something fun after your work session.

Watch Netflix, go on Twitter, play a video game.

This makes your brain associate positive feelings with work.

Next time you go to work it'll be 10x easier.

- -

How to finish more work in 2 hours than 95'%' of people do in 2 weeks:

1. Create a focus playlist

2. Prime yourself

3. Work for 1.5 - 2 hours

4. Separate analytical and creative tasks

5. Remove distractions

6. Set 1 goal for each work block

7. Reflect

8. Reward yourself

EXAMPLE 2:

"Do you struggle to write good threads?

It's because you're writing the wrong kind.

Here are the only 3 types of threads you need to explode on Twitter:

- -

Growth threads.

These are threads with more general ideas that apply to anyone.

Your timeline is filled with these.

Why?

Because they're easy to read and make people feel good.

Some examples are:

- 10 Habits for...
- 7 Lessons I learned...
- 5 Tips I wish I knew...
- -

Growth threads are great, but have drawbacks.

Pros:

- Great for likes & comments
- Grows your following
- Easy to write

Cons

- Don't build trust
- Won't attract clients
- Doesn't help your existing audience
- -

Actionable threads.

These threads have specific advice for your niche.

Or content establishing your expertise.

You wanna make more $$$?

Write these.

Some actionable thread ideas in the writing niche:

- Case studies
- How to craft a hook
- Types of threads on Twitter ;)

– -

Actionable threads are high-value, but have disadvantages.

Pros:

- Attracts high-quality followers
- Grows trust in your audience
- Establishes you as an expert

Cons

- Harder to write
- Lower engagement
- Won't gain as many followers

– -

Personality threads.

These are threads where you let your personality shine.

It feels vulnerable to post these...

But this is what makes you a PERSONAL brand.

And is the best way to grow fans.

Examples are:

- Transformations
- Hard times you went through
- Your opinions

– -

Personality threads are fun but have downsides.

Pros:

- Fun to write
- Repels lame people
- Attracts like-minded people

Cons

- Gives less value
- Opens yourself up to haters
- Harder to hit the publish button

– -

The best thread type?

Combine different types.

- Growth + Actionable
- Growth + Personality
- Actionable + Personality

Writing combination threads is a recipe for virality.

– -

The only 3 types of threads you need to explode on Twitter:

1\ Growth

2\ Actionable

3\ Personality


Remember, every tweet in the thread should follow the "What-Why-How-Snap" framework.
Remember, In your output, provide the thread without spelling out the framework parts themselves (Don’t write out “SNAP”)                                                         
            """
        )
        return actionable_tweet_draft_prompt
    
    
    def get_actionable_tweet(self):
        #For context**, *{context}***
        actionable_tweet_draft_prompt = ChatPromptTemplate.from_template("""You are an expert on writing concise, clear, and illuminating writing Twitter threads following the "Tweet-Why-How-Snap" framework on the topic of the input provided for me.
                                                                                                                                                  
Take a look at this Tweet '{headline}' and expand it into a Twitter thread following the "Tweet-Why-How-Snap" framework, all written in a tone that's confident, knowledgeable, and helpful.

Constraints:
1. No hashtags
2. Readability grade 7 or lower
3. Every tweet consists of 250-280 characters
4. No emojis
5. Use concise language
6. Each tweet in the thread should follow the "What-Why-How-Snap" framework
7. Use complete sentences and emphasize benefits over features.
8. Use active voice

OUTPUT INSTRUCTIONS
The "What-Why-How-Snap" framework is a 4-part framework for every individual tweet in the thread. It works like this:
1) "What": The first part of the tweet stating what you are talking about in less than 9 words. This can be a tip, a resource, or something else.
2) "Why": Logically explains why the "What" is relevant in 8 words or less. Can't begin with "to" or "this".
3) "How": 3-5 actionable steps on 2-5 words each in bullet points “•” on how the audience can implement the advice
4) "Snap": a short, sequence that wraps up the tweet with a takeaway, wise quote, or lesson. Reading the "snap" should leave the reader with a sense of satisfaction.

The format should be:
- Headline
- 5-6 following tweets in the format I teached you.

Please expand it into a Twitter thread following the "Tweet-Why-How-Snap" framework, all written in a tone that's confident, knowledgeable, and helpful.
Remember to make each tweet engaging and informative. Assume the reader doesn't know anything about the topic yet, so please make sure to give context to any new terms or principles.
Remember, every tweet in the thread should follow the "What-Why-How-Snap" framework.
Remember, In your output, provide the thread without spelling out the framework parts themselves (Don’t write out “SNAP”)                                                         
"""
        )
        return actionable_tweet_draft_prompt
    
    def get_actionable_tweet_prompt_test3(self):
        actionale = ChatPromptTemplate.from_template("""USER:
{tweet}

SYSTEM:
Please expand it into a Twitter thread following the "Tweet-Why-How-Snap" framework, all written in a tone that's confident, knowledgeable, and helpful.

Constraints:

1. No hashtags

2. Readability grade 7 or lower

3. Every tweet consists of 250-280 characters

4. No emojis

5. Use concise language

6. Each tweet in the thread should follow the "What-Why-How-Snap" framework

7. Use complete sentences and emphasize benefits over features.

8. Use active voice

The "What-Why-How-Snap" framework is a 4-part framework for every individual tweet in the thread. It works like this:

"What": The first part of the tweet stating what you are talking about in less than 9 words. This can be a tip, a resource, or something else.

"Why": Logically explains why the "What" is relevant in 8 words or less. Can't begin with "to" or "this".

"How": 3-5 actionable steps on 2-5 words each in bullet points “•” on how the audience can implement the advice

"Snap": a short, sequence that wraps up the tweet with a takeaway, wise quote, or lesson. Reading the "snap" should leave the reader with a sense of satisfaction.

Remember to make each tweet engaging and informative. Assume the reader doesn't know anything about the topic yet, so please make sure to give context to any new terms or principles.

In your output, provide the thread without spelling out the framework parts themselves.

The format should be:

Headline (my input)
5-6 following tweets in the format I teached you.

Here's 2 example of a great thread where every tweet follows the "What-Why-How-Snap" framework:

EXAMPLE 1:

How to finish more work in 2 hours than 95'%' of people do in 2 weeks:

- -

Create a focus playlist.

Try these soundtracks:

- Drive
- Dune
- TENET
- Dunkirk
- Ad Astra
- Inception
- Interstellar
- The Batman
- Cyberpunk 2077
- Blade Runner 2049
- The Dark Knight Trilogy

Your brain will get into deep work 2x faster.

- -

Prime yourself.

Prepare your mind for the activity.

8 hours of sleep primes you to focus.

30 minutes of reading primes you to write.

10 minutes of planning primes you to organize.

Short-term preparation leads to long-term success.

- -

Schedule deep work sessions for 1.5 to 2 hours.

Why?

1) It takes 20-30 minutes to get into flow state

2) It takes around 1.5-2 hours before your focus declines

Take a break too early, you won’t get into flow.

But if you don't take a break, you'll work inefficiently.

- --

Separate tasks based on their type.

Batch analytical tasks together:

- Organization
- Research
- Planning

Batch creative tasks together:

- Writing
- Designing
- Brainstorming

Your brain wastes energy to adjust when you switch from task to task.

- -

Remove distractions.

Too much noise?

Use noise-cancelling earbuds.

Distracting websites?

Use a website/app blocker.

Too much going at home?

Go to a coffee shop.

It's impossible to get distracted when it's not an option.

- -

Set 1 goal for each work block.

Break it into 3 actionable tasks.

Now, focus on 1 task at a time.

When you complete it, move to the next.

Knowing what you need to do prevents you from getting distracted with “busy” work.

- -

Reflect.

After your work sessions, look at what you can improve.

Do you need to:

- Change the length of time?
- Do certain tasks before others?
- Work at a different part of the day?

Optimize for the next session.

- -

Reward yourself.

Do something fun after your work session.

Watch Netflix, go on Twitter, play a video game.

This makes your brain associate positive feelings with work.

Next time you go to work it'll be 10x easier.

- -

How to finish more work in 2 hours than 95% of people do in 2 weeks:

1. Create a focus playlist

2. Prime yourself

3. Work for 1.5 - 2 hours

4. Separate analytical and creative tasks

5. Remove distractions

6. Set 1 goal for each work block

7. Reflect

8. Reward yourself

EXAMPLE 2:

"Do you struggle to write good threads?

It's because you're writing the wrong kind.

Here are the only 3 types of threads you need to explode on Twitter:

- -

Growth threads.

These are threads with more general ideas that apply to anyone.

Your timeline is filled with these.

Why?

Because they're easy to read and make people feel good.

Some examples are:

- 10 Habits for...
- 7 Lessons I learned...
- 5 Tips I wish I knew...
- -

Growth threads are great, but have drawbacks.

Pros:

- Great for likes & comments
- Grows your following
- Easy to write

Cons

- Don't build trust
- Won't attract clients
- Doesn't help your existing audience
- -

Actionable threads.

These threads have specific advice for your niche.

Or content establishing your expertise.

You wanna make more $$$?

Write these.

Some actionable thread ideas in the writing niche:

- Case studies
- How to craft a hook
- Types of threads on Twitter ;)

–

Actionable threads are high-value, but have disadvantages.

Pros:

- Attracts high-quality followers
- Grows trust in your audience
- Establishes you as an expert

Cons

- Harder to write
- Lower engagement
- Won't gain as many followers

–

Personality threads.

These are threads where you let your personality shine.

It feels vulnerable to post these...

But this is what makes you a PERSONAL brand.

And is the best way to grow fans.

Examples are:

- Transformations
- Hard times you went through
- Your opinions

–

Personality threads are fun but have downsides.

Pros:

- Fun to write
- Repels lame people
- Attracts like-minded people

Cons

- Gives less value
- Opens yourself up to haters
- Harder to hit the publish button

–

The best thread type?

Combine different types.

- Growth + Actionable
- Growth + Personality
- Actionable + Personality

Writing combination threads is a recipe for virality.

–

The only 3 types of threads you need to explode on Twitter:

1\ Growth

2\ Actionable

3\ Personality

"

Remember, every tweet in the thread should follow the "What-Why-How-Snap" framework.

Remember, In your output, provide the thread without spelling out the framework parts themselves (Don’t write out “SNAP”)
"""
        )
        return actionale                                                
  
    
    def get_actionable_tweet_prompt_step2(self):
        actionable_tweet_prompt = ChatPromptTemplate.from_template("""
            Rewrite the tweet thread so that each of the tweets includes:

            1. The key takeaway
            2. One line on why it's important or true
            3. 2-3 actionable bullet points that help the reader implement the takeaway
            4. A snappy end sentence that gives advice how to take action

            Continue to write in natural and casual language( don't be overly enthusiastic).

            Also, remember that each tweet should be less than 280 characters.

            You do not need to label your output with "Snap" "What" "Why" "How" etc.

            Example:

            "When writing tweets, use my "What-Why-How" framework.

            This simplifies your writing and makes it feel complete.

            1st part: state what you're talking about

            2nd part: state why it's important

            3rd part: give actionable advice on how they can use it

            This tweet is an example"                            
            """
        )
        return actionable_tweet_prompt
    
    def get_research_for_tweet_prompt(self):
        research_tweet_prompt = ChatPromptTemplate.from_template("""
            Research a curated blog post about {topic}, and tell me a brief, 3-sentence summary of each.             
            """
        )
        return research_tweet_prompt 


    def get_research_for_tweet_prompt(self):
        research_tweet_prompt = ChatPromptTemplate.from_template("""
            ***[1.INSERT CURATION]***

            Well done. Now, based on the summary above, I want you to write a viral curation thread for me titled "***[2.THREAD HEADLINE]***", all written in an engaging, concise tone.


            Constraints

            1. No hashtags

            2. Readability grade 7 or lower

            3. Every tweet consists of 250-280 characters

            4. No emojis

            5. Use concise language

            6. Use complete sentences and emphasize benefits over features.

            Examples of viral curation threads:

            EXAMPLE 1:

            I’ve done $2M in income in 2.5 years as a solopreneur.

            And I didn't write a single line of code.

            My 14 "must use" no-code tools:

            [🧵 thread]

            1/ Carrd

            Carrd is the fastest and easiest way to build websites.

            It's great for personal sites or standing up landing pages quickly.

            I presell any idea by whipping up a quick landing page on Carrd.

            2/ Gumroad

            For digital products, nothing is easier and faster than Gumroad.

            I can think of a product/service and have it fully embedded on my Carrd landing page in less than 10 minutes.

            This lets me start pre-selling fast to get the validation I need to continue.

            3/ Canva

            Canva has made me into my own personal graphic designer.

            Whether it's Twitter banners, icons, logos, landing page graphics, Instagram posts, you name it...

            Canva makes it as easy as drag-and-drop to start designing.

            4/ Outseta

            Thinking about launching a community or SaaS product?

            Outseta is your tool.

            CRM, payments, subscriptions, email automation, gated content, segmentation, etc...

            Outseta is loaded with great features and functionality at an extremely fair price.

            5/ AirTable

            Airtable keeps my entire advising business thriving and organized.

            Collecting information through forms, automating email triggers, building Kanban charts, and collaborating with my wife are just some of the things I love doing to manage my business.

            6/ Calendly

            Calendly cuts all of the time-consuming back and forth when scheduling.

            Anything that requires scheduling a meeting, a simple Calendly embed works wonders.

            I also drop it on my website for paid coaching calls.

            7/ Fathom Analytics

            Looking at Google Analytics can be confusing for some folks.

            Fathom is simple, privacy-first, cookie-free, and GDPR compliant.

            Plus, with just a glance, I know exactly what is impacting my website traffic.

            Great service.

            8/ Loom

            Loom is my favorite tool for:

            - Creating video process docs
            - Building out my online courses
            - Doing video walkthroughs for my community
            - Teaching someone how a piece of software works

            Simple, easy to install, and tracks visitor/watcher analytics.

            9/ Testimonial.to

            Strong testimonials are a great way to improve conversion.

            Nothing makes it easier and more impactful than Testimonial.to

            I embed it in my course, and users can leave video/text testimonials that automatically appear on my landing pages.

            10/ HypeFury

            It added new features that have recently turned it from good to "I can't live without this".

            I schedule Tweets, craft threads, auto-plug my newsletter, auto-retweet, run sales, etc.

            It does everything for the daily content writer.

            A must-buy.

            11/ Typeshare

            I write a weekly newsletter called, The Saturday Solopreneur.

            As much short-form content as I write, I struggled with long-form.

            Until I purchased Typeshare

            Now, I open it up, pick a template, and write my newsletter in less than 30 minutes.

            Gamechanger.

            12/ Notion

            Notion is basically the master hub for my whole life.

            In Notion I:

            - Host my roadmap
            - Manage my to-do list
            - Write all of my content
            - Store my process docs
            - And much more...

            And I'm still learning how to use it most effectively.

            13/ BlackMagic

            I've been using BlackMagic to manage my entire Twitter world.

            - Powerful Real-Time Analytics
            - Personal Twitter CRM
            - Reminders & notes
            - Audience insights

            It gives me an inside look at what works, what doesn't and why.

            14/ Zapier

            No list would be complete without Zapier

            Never has one tool made me feel like the whole world of technology is at my fingertips.

            From building simple pass-through Zaps, to complex, multi-step Zaps, Zapier makes anything possible by combining technologies.

            - -

            EXAMPLE 2:

            ChatGPT has been dethroned.

            AI Chrome extensions are now at the forefront of AI.

            Here's 8 cutting-edge AI Chrome extensions to 10x your productivity:

            Glasp YouTube Summary

            Auto-generate summaries of your favorite YouTube video via AI.

            With Glasp's Chrome extension, you get detailed timestamps and paragraph descriptions.

            Perfect for learning more efficiently and skipping ahead.

            Compose AI

            Cut your writing by 40'%' with the brilliant power of AI auto-completion and text generation.

            This extension will save you countless hours with emails and writing tasks.

            ChatGPT Prompt Genius

            ChatGPT is a fantastic tool, but only if you give it the right prompts.

            This Chrome extension allows you to:

            - Browse
            - Import
            - Store

            All the most useful ChatGPT prompts in the world to your device.

            Wordtune

            Communicate your ideas better with clear and compelling writing.

            The Wordtune Chrome extension can:

            - Change your writing tone
            - Expand on your paragraphs
            - Make your writing more concise

            Scribe

            Auto-generate step-by-step guides just by pressing record.

            Scribe watches your workflow process and then uses the power of AI to create your guide on autopilot.

            Perfect for building SOP's.

            SciSpace Copilot

            Your all-knowing personal research assistant.

            SciSpace Copilot explains complex topics, formulas, and math in-tab.

            You can also ask follow-up questions to get clearer answers.

            No more opening new tabs to research unfamiliar terms.

            Use ChatGPT AI

            No need to have a separate tab open with ChatGPT.

            With this extension, you can use GPT-4 on any website (without needing to copy-paste anymore).

            Perplexity

            Google x ChatGPT = Perplexity.

            Perplexity's Chrome extension can:

            - Summarize any web page
            - Give answers to any question

            The perfect research co-pilot for web browsing.

            8 cutting-edge AI Chrome extensions to 10x your productivity:

            - Glasp
            - Scribe
            - Compose
            - Perplexity
            - Wordtune
            - Use ChatGPT AI
            - SciSpace Copilot
            - ChatGPT Prompt Genius             
            """
        )
        return research_tweet_prompt 

    def get_lit_listicles_prompt(self):
        """
        
        For context, {context}.

        My audience are {audience}.
        """
        lit_listicles_prompt = ChatPromptTemplate.from_template("""You are an expert on writing concise, clear, and illuminating writing 5 "Lit listicles" on the topic of the input provided for me.
                                                                
OUTPUT INSTRUCTIONS
"Lit listicles" are texts that are published on social media platforms like LinkedIn.
They are characterised by the following traits:
1) They are highly specific advice, information, or lists for a special target audience
2) They are easy to read and skim
3) They have intriguing hooks
4) They are concise and compelling

EXAMPLES OF PAST SUCCESSFUL "Lit Listicles", separated by [NEW POST]
[NEW POST]

10 realities of content marketing:
1. It takes time to reap the benefits
2. It's near impossible to fully attribute
3. You need to post content consistently
4. Content isn't JUST publishing blog posts
5. Some content doesn't provide tangible ROI
6. It's likely wasted if you don't have a strategy
7. You must understand your customers deeply
8. It requires high investment (time and/or money)
9. Creating content doesn't guarantee an audience
10. But not creating content guarantees no audience\n\n
What would you add?

[NEW POST]\
    
How to improve your content 1'%' everytime (and not post just to keep up):

- Go to your content library (I use Shield)
- Take a look at a winner from 3 months ago
- Ask yourself “Is there anything I missed?”
- If yes, add it in and then:
- Ask yourself “Could it be more concise?”
- If yes, cut fluff and then:
- Schedule post

You don't need 'new' to grow.
You need 'better'.

[NEW POST]

The 7 most important ingredients for LinkedIn growth\n\n
1. Applicable content "Can someone use this now?"
2. Personality "Do you sound like everyone else?"
3. Clarity "Is your content easy to understand?"
4. Availability "Do you respond to comments?"
5. Approachability "Are you easy to talk to?"
6. Attractive profile "How optimized is it?"
7. Relatability "Is this for me; or others?"

Do this → you'll do better than 99'%' of LinkedIn
Bonus:
8. Length "does my post fit onto a phone's screen? Or do others have to keep swiping to reach the end?"

[NEW POST]

7 deadly LinkedIn sins:
1. Commenting "great post" only
2. Not giving away something for free
3. Commenting on every post you enjoy
4. Not having an offer in your profile banner
5. Commenting on your own post right away
6. Not responding to comments after posting
7. Not having a Featured section on your profile

7 ways to do it right (and easy):

1. Comment with intent + tag the author
2. Host a LinkedIn Live event (audio or video)
3. Comment only on posts relevant to your brand
4. State your brand's offer / message in the banner
5. Never comment on your own post in the 1st 10mins
6. Stay active and engage 60-90mins after publishing
7. 1 main offer + 1-2 extra links in the Featured section

Be kind to others. Always. Anytime.

END EXAMPLES OF PAST SUCCESSFUL "Lit Listicles"

STEPS:
1) Silently analyse the "Lit listicles" I gave you
2) Silently analyse the context I gave you and think about ideas compelling to my audience
3) Use your insights from 1) and 2) with the characteristics I gave you and write 5 "actionable posts" that are insanely valuable to my audience\n\n\n
OUTPUT FORMAT
1) No emojis
2) No hashtags
3) Use numbers
4) Every listicle point must be maximum 50 characters
5) Be ultra-specific and elaborate in your advice, but keep it ultra-concise. For example, rather than saying "Let AI draft content", say "Use ChatGPT to create 85'%' good drafts"
6) You can be a bit inspirational and motivational, but don't overdo it. For example, "Take the leap. Start small, dream big. In no time, you'll be an expert in AI-assisted writing. It's easier than you think." sounds cringe, while "Highlight the VALUE to inspire ACTION. A simple shift in perspective can lead to profound changes in your writing." sounds great.
7) Conclude with a takeaway or a question to the audience
8) Every "Lit Listicle" should include 10 listicle points
9) Sort the listicle points in descending length
10) not use cliches or jargon.
11) not include common setup language in any sentence, including: in conclusion, in closing, etc.
12) not output warnings or notes—just the output requested.
13) Use Layman's Terms

INPUT
{topic}

Write 5 Lit Listicles, please split with [NEW POST].
"""
        )
        return lit_listicles_prompt
    
    
    
    
    
    def get_lit_listicles_prompt_2(self):
        """
        
        For context, {context}.

        My audience are {audience}.
        """
        lit_listicles_prompt = ChatPromptTemplate.from_template("""
        You are an expert on writing concise, clear, and illuminating writing  "Lit listicles" on the input provided by me.

        Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.
        
        OUTPUT INSTRUCTIONS
        "Lit listicles" are texts that are published on social media platforms like LinkedIn.
        They are characterized by the following traits:
        1) They are highly specific advice, information, or lists for a special target audience
        2) They are easy to read and skim
        3) They have intriguing hooks
        4) They are concise and compelling

        OUTPUT FORMAT
        1) No emojis
        2) No hashtags
        3) Use numbers
        4) Every listicle point must be maximum 50 characters
        5) Be ultra-specific and elaborate in your advice, but keep it ultra-concise. For example, rather than saying "Let AI draft content", say "Use ChatGPT to create 85% good drafts"
        6) You can be a bit inspirational and motivational, but don't overdo it. For example, "Take the leap. Start small, dream big. In no time, you'll be an expert in AI-assisted writing. It's easier than you think." sounds cringe, while "Highlight the VALUE to inspire ACTION. A simple shift in perspective can lead to profound changes in your writing." sounds great.
        7) Conclude with a takeaway or a question to the audience
        8) Every "Lit Listicle" should include 10 listicle points
        9) Sort the listicle points in descending length
        10) not use cliches or jargon.
        11) not include common setup language in any sentence, including: in conclusion, in closing, etc.
        12) not output warnings or notes—just the output requested.
        13) Use Layman's Terms

        INPUT:
        {topic}

        Write 5 "Lit Listicles" please.
        """
        )
        return lit_listicles_prompt
    
    
    def get_lit_listicles_prompt_3(self):
        """
        
        For context, {context}.

        My audience are {audience}.
        """
        lit_listicles_prompt = ChatPromptTemplate.from_template("""
        You are an expert on writing concise, clear, and illuminating writing  "Lit listicles" on the input provided by me.
        
        "Lit listicles" are texts that are published on social media platforms like LinkedIn.
        They are characterized by the following traits:
        - They are highly specific advice, information, or lists for a special target audience
        - They are easy to read and skim
        - They have intriguing hooks
        - They are concise and compelling
        
        Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

        STEPS
        1. Every listicle point must be maximum 50 characters.
        2. Every "Lit Listicle" should include 10 listicle points.
        3. Sort the listicle points in descending length
        4. Conclude with a takeaway or a question to the audience
        5. Be ultra-specific and elaborate in your advice, but keep it ultra-concise. For example, rather than saying "Let AI draft content", say "Use ChatGPT to create 85% good drafts"
        6. You can be a bit inspirational and motivational, but don't overdo it. For example, "Take the leap. Start small, dream big. In no time, you'll be an expert in AI-assisted writing. It's easier than you think." sounds cringe, while "Highlight the VALUE to inspire ACTION. A simple shift in perspective can lead to profound changes in your writing." sounds great.
        7. No emojis
        8. No hashtags
        9. Use numbers
        10. not use cliches or jargon.
        11. not include common setup language in any sentence, including: in conclusion, in closing, etc.
        12. not output warnings or notes—just the output requested.
        13. Use Layman's Terms


        INPUT:
        {topic}

        Write 5 "Lit Listicles" please.
        """
        )
        return lit_listicles_prompt
    
    def get_test_research_chapter(self):
        test_research_chapter = """
        1. Think creatively
        A manager’s job is to get results ... in a world of constant change. Change is
        inevitable. Change is opportunity. If you stay as you are you stay where you are.
        The world belongs to those who are in love with the new. In such a world there is
        a strong relationship between the quantity and quality of new ideas and a
        manager’s success in achieving results.
        1. A definition of creativity
        Creativity is the ability to improve. We all came into the world being creative,
        innovative, and inventive. Our birthright is to improve our condition. We all
        behave in a manner consistent with improving our condition. For most of us our
        creativity has lain dormant since childhood. We must all now learn to tap into
        our own creativity. We can all learn to tap into the creativity of others. One of
        the mental laws which govern all our lives is the law of habit. The law of habit
        states that almost everything we do is habit. The ways in which we walk, talk,
        respond to situations and the ways in which we use our creativity are all habits.
        Make a habit of using your creativity. Make a habit of trying to improve
        situations by 10 per cent. There are many ways in which we can improve sales
        by 10 per cent, reduce costs by 10 per cent, and increase profit by 10 per cent.
        Everything can be improved in some way. The success of the organization is
        directly related to the quality and quantity of new ideas generated and
        implemented. Many companies have been saved by using the techniques in
        creativity discussed later in this section. In all aspects of the business there are
        ways of being better, cheaper, and faster. The competitive advantage of our
        business is that we are better, cheaper or faster than our competitors in some
        way. Furthermore, there are always ways in which we can be more pleasant in
        our dealings with customers, suppliers, bankers, etc. Being “nicer” is the fourth
        way in which we can establish competitive advantage. Continuous
        improvement through creativity is one of the keys to success in business.
        2. Determinants of creativity
        The world of success and failure in business is a mental world in which
        everything starts with ideas. Unfortunately, most of us have a strong tendency
        to stifle our own creativity or to dismiss our own creative ideas as worthless.
        For individuals the level of creative activity and the value on which an
        individual places on his or her own creativity tend to be determined by past
        experience, the present situation, and the self-concept. We tend to be more
        creative if in the past we have worked in a positive environment where
        creativity has been encouraged. Creativity is encouraged by enthusiasm,
        excitement, love, joy and acceptance of responsibility. Unfortunately, many of
        us have worked in negative environments where creativity was stifled by fear of
        failure, fear of rejection, self-doubt, self-pity, failure to accept responsibility,
        hate, envy and blame. If our present situation is dominated by positive
        emotions, then this encourages creativity. Finally, from the law of belief we
        Journal of Management
        Development, Vol. 16 No. 8, 1997,
        pp. 521-667. © MCB University
        Press, 0262-1711
        Journal of
        Management
        Development
        16,8
        522
        know that we always behave in a manner consistent with our beliefs. If we
        believe we are creative, then we behave in a manner consistent with being
        creative. We have a self-concept or belief about each aspect of our lives. Each
        individual has a self-concept level of income, a self-concept level of creativity, a
        self-concept as a manager, a self-concept as a sales person, a self-concept as a
        negotiator, a self-concept as a squash player, cook and lover. The self-concept is
        the bundle of beliefs an individual has about his or her ability. In short, if you
        believe you are creative you behave in a manner consistent with being a creative
        person. The most exciting part of the law of belief is that beliefs are not based
        on reality. If you believe you are a Christian you are a Christian. If you believe
        you can swim you are a swimmer. If you believe you can ride a bicycle, then you
        will always behave in a manner consistent with being able to ride a bicycle.
        Make a decision to believe that you are a creative genius. Visualize,
        emotionalize, and affirm. Visualize yourself as a creative person. Imagine how
        well you would feel if you were a creative person. Finally, make a habit of the
        affirmation: “I am a very creative person”. If you believe you are creative, then
        you will behave in a manner consistent with being creative.
        As far as the organization is concerned, happy, open, optimistic, encouraging
        environments encourage creativity. Low levels of creativity are associated with
        a negative environment. Positive emotions are strongly associated with
        creativity. Managers should provide a work situation which is encouraging,
        enthusiastic and exciting. These are the great positive emotions. Finally, high
        self-esteem is strongly associated with creativity. Self-esteem is the extent to
        which an individual feels valuable and worthwhile. One aspect of a manager’s
        job is to make people feel important, to make people feel valuable and
        worthwhile. We must all encourage others to repeat the affirmation: “I am a
        valuable and worthwhile person”. Many people suffer from low self-esteem
        believing that their ideas are of little value. A high self-esteem environment is a
        creative environment.
        3. Stimulate your creativity by goal setting
        Creativity is stimulated by clear goals with specified deadlines for achievement.
        Think about your managerial goals. Where would you like to be one year from
        now? Where would you like to be three years from now? What business would
        you like to be in at some specified future date? How much money would you like
        to be earning three years from now? What sort of a company car will you have?
        What are the skills you must acquire in order to achieve those goals? What are
        your personal and family goals? Where would you like to be 20 years from now?
        What are your most urgent goals during the next 12 months? What are your
        three most pressing problems or challenges at this moment?
        We use the following exercise to stimulate the creativity of managers,
        including the self-employed.
        Career/business goals
        In an ideal world, what business would you like to be in three years from now?
        What position will you hold in the company? What will your salary be? What
        Think
        creatively
        523
        level of sales and profits will you achieve? What sort of a company car will you
        have? Write down five career/business goals for achievement within three
        years.
        Personal development plan
        One of the simple truths we all have to face up to as adults is that wherever we
        are in business at the present time is where we deserve to be. If we had greater
        knowledge/skills and a more positive attitude then we would be in a better
        position. If we had less knowledge and a more negative attitude, then we would
        not even be where we are today. In order to advance in business, we must
        change in some way. We must increase our knowledge/skills and/or we must be
        more positive in attitude. What additional skills must you acquire as a manager
        to be in the position you would like to be in three years from now. Do you need
        to be more creative? Do you need to learn more about strategy, marketing, sales
        skills, negotiation skills, finance, leadership? Be honest with yourself and write
        down five skills which you must acquire over the next three years to achieve
        your career/business goals.
        Personal and family goals
        Why do you want to be successful in business? What are the personal and
        family goals that drive you forwards? Do you want to be happily married with
        two children in private school? Do you want a beautiful home in the country? Do
        you want a trip around the world, an expensive motor car, status, admiration,
        your own private swimming pool? By focusing and concentrating on these
        goals, defining them with crystal clarity, and setting deadlines for their
        achievement, you will stimulate your own creativity.
        4. Stimulate creativity by identifying rocks
        What are the rocks that stand between you and achieving your desired goals?
        What are the limiting factors? What are your self-limiting beliefs? What are the
        negative emotions which are holding you back? There are always obstacles
        which stand between an organization and the achievement of its goals. There
        are always obstacles which stand between managers and achievement of
        desired results. By facing up to the rocks, with a great deal of self-honesty, we
        can stimulate our creativity. What are the obstacles that stand between the
        organization now and its ideal future? Define the ideal future, i.e. goals, and
        then identify the rocks. Use your creativity either to overcome the rocks or avoid
        them. What is the factor which is limiting the organization in achieving its
        goals. Is it lack of finance? Is it lack of leadership? Is it lack of a coherent
        strategy? Is it failure in marketing, selling, negotiating, people skills? Is it lack
        of focus, poor advertising, poor human relations, lack of information, failure to
        maintain competitive advantage? As a manager, what are your own selflimiting beliefs? Do you believe that you are incompetent in leadership, in
        marketing, in selling, in negotiating, strategy? Do you feel that you cannot
        achieve more because you are inadequately qualified, because you did not go to
        university, or perhaps because you are a woman. Which negative emotions are
        Journal of
        Management
        Development
        16,8
        524
        holding you back? Is it an inability to accept responsibility, a propensity to
        blame others for your condition, envy, self-pity, fear of failure, fear of rejection,
        jealousy, anger or self-doubt? Use your self-honesty and then your creativity to
        change your self-limiting beliefs and overcome negative emotions. Negative
        emotions can be replaced with the positive emotions of excitement, enthusiasm,
        love, joy and acceptance of responsibility. These positive emotions can be
        stimulated by clear goals. Focus and concentrate on what you want. Focusing
        on your desires stimulates positive emotions and creativity.
        5. Creative and uncreative thinking
        Mechanical thinking
        Do you tend to see things as either black or white? Are you inflexible in your
        thinking? Are you generally pessimistic? Do you have fixed attitudes? Do you
        tend to blame others for your condition? If you do tend to indulge yourself in
        this kind of mechanical thinking, then you will also tend to be uncreative. Make
        the necessary efforts to change your thinking.
        Adaptive thinking
        Do you tend to have an open mind on most affairs? Are you flexible in your
        thinking? Are you generally optimistic? Is your thinking solution-oriented
        rather than problem-oriented? Do you generally suspend judgement until all the
        facts have been collected and analysed? Do you avoid attachment to one idea? If
        you can practise adaptive thinking rather than mechanical thinking then you
        will be more creative. Do not take it personally if someone holds a different
        opinion from yours. Do not make a habit of justifying being exactly as you are.
        If you stay as you are, you stay where you are. The more you do of what you do,
        the more you get of what you have got!
        6. I am a creative genius
        Intelligence is a way of behaving. If you behave intelligently, then you are
        intelligent. Alternatively, if you behave as an idiot, then you are an idiot – even
        if you have a university degree. Your IQ is a measure essentially of your verbal
        and mathematical skills. There are many different kinds of intelligence, which
        are more relevant to success in business than verbal and mathematical skills,
        e.g. intuitive intelligence, social skills intelligence. Use the affirmation: “I am a
        creative genius”. This will become part of your belief system. Once you believe
        that you are a creative genius then the law of belief tells us that you will behave
        in a manner consistent with being a creative genius. The following four
        characteristics of genius can all be learned.
        Clarity
        Try and see the big picture. Try and identify causal relationships. Identify
        specific, measurable goals. Decision making becomes much easier when the
        goal is clear. Be honest in identifying problems, rocks, negative emotions, selflimiting beliefs.
        Think
        creatively
        525
        Focus and concentration
        Focus on outcomes. Define the perfect outcome. Describe the perfect outcome.
        Focus and concentrate on the issue. All highly creative people have the ability to
        focus and concentrate on the issue. Avoid the butterfly mentality of those who
        consistently jump from one issue to another resolving nothing. Make lists. Keep
        notes. Investigate all the possible routes.
        Adaptive thinking
        Avoid attachment to one idea. Be adaptive and flexible. Keep an open mind. Ask
        questions. Stand back and consider the ideas of others. Keep questioning the
        assumptions. Ask others who have faced the same problems. A different point
        of view from yours is not an attack on your integrity or ability.
        Use systematic methodology
        Use the systematic methods of problem solving discussed in this article – the
        20-idea method, the systematic method, brain storming, finish the statement,
        the standard approach, lateral thinking and access the superconscious.
        7. Making a new start in creativity
        Creativity is a skill which can be learned and developed. We can all make
        improvements, especially in those areas which are closest to us. Make a start as
        below.
        (1) Desired goals. Begin to focus and concentrate on achievable goals within
        a specific time period.
        (2) Urgent problems/challenges. Identify your most pressing problems/
        challenges and focus and concentrate on those issues.
        (3) Use focused questions:
        • How can we increase sales by 25 per cent over the next three
        months?
        • How can we reduce our heating costs by 15 per cent?
        • How can we improve our customer care?
        • How can we make our advertising more effective?
        • In any situation what are our assumptions?
        (4) Start being adaptive/flexible. Make a habit of saying: “I was completely
        wrong on that occasion”; “I changed my mind completely”; “I don’t know
        anything about that”; “I need a great deal of help in this area”.
        (5) Bombard your mind. Bombard your mind with the information which is
        consistent with being highly creative. Read books, listen to tapes, attend
        courses, and most of all, spend time with people who are creative. Form
        a mastermind alliance of creative people. We are very much influenced
        by the people around us, our reference group. If you spend time with very
        creative people this will encourage you to be creative.
        Journal of
        Management
        Development
        16,8
        526
        8. Use the three tiers of the brain
        The brain seems to be divided into at least three sections – the conscious, the
        subconscious and the superconscious. The conscious mind is where our daily
        thinking takes place in making decisions and trying to solve problems. The
        conscious mind can call up ideas, experiences and beliefs from the subconscious
        which is where all our experiences and beliefs are stored. The subconscious
        operates 24 hours a day and can handle any number of problems. One way to
        stimulate creativity is to consider all aspects of a problem, and then ask the
        subconscious to find the answer by 3 p.m. the following Friday afternoon. The
        subconscious can be used to solve problems or rise to challenges or instructions
        from the conscious mind. The superconscious mind has access to knowledge
        and experience beyond one’s own knowledge and experience. The
        superconscious is the source of creativity, excitement and intuition. The
        superconscious mind is stimulated by clarity, strong desire, solitude and strong
        emotions. It is maintained by some people that any desire that can be
        transmitted to the superconscious must be brought into reality by the
        superconscious mind. Focus and concentrate on your crystal clear goals. Drive
        those goals into the superconscious. Desire to achieve your goals as a manager.
        Reflect in solitude on goals, problems, challenges, opportunities. Drive a great
        deal of emotion into your desires. The superconscious will reward you with
        blinding flashes of the obvious, the people, information, and circumstances
        required to achieve your goals, and unexpected chance events which will enable
        you to get the results you require. Remember that any goal or desire which you
        can drive into the superconscious must be brought into your reality.
        9. Creative thinking alternatives
        We do not all think in exactly the same way. Some people think in pictures,
        others in words, others depend on their emotions. Faced with a
        problem/challenge, those who visualize tend to draw or map out the possible
        solutions. They conclude: “it looks good to me”. Those who think auditorially
        talk through the various alternatives, using words, and conclude “this sounds
        like a good idea”. Those who think kinaesthetically rely on their feelings about
        a situation and conclude “I feel this is the right way forward”.
        In order to stimulate our creativity we should each approach the same
        situation by trying to draw solutions, work out solutions in words, and examine
        our emotional responses to situations. We should also try to understand that we
        may be able to see an answer, but others need to have it spelt out in words. Try
        not to be too hard on those who cannot see or even work out the answer verbally.
        Some people need to feel it is the right way forward. You can stimulate your
        creativity by trying an approach which does not come naturally to you.
        10. The standard approach to problem solving
        Faced with a problem many people do not know what to do. Those who think
        they know what to do often stick to the one obvious solution. Many of us suffer
        from identification in that we take it very personally if somebody offers an
        Think
        creatively
        527
        alternative. Many of us continue to justify making the same mistakes we have
        always made. The following standard approach solves many problems:
        (1) Define the problem with great clarity. Simply defining the problem
        precisely is believed to solve about 50 per cent of problems.
        (2) Collect information. Collect all the facts together, not just the convenient
        facts. Avoid identification, i.e. taking it personally if some of the facts do
        not fit with preconceived solutions. Practise detachment, i.e. separate
        people from the problem. Detach yourself from the personalities involved
        and focus on the problem.
        (3) Ask others for advice. Tap into the creative genius of others. Tap into the
        experience of others. Do not be afraid to ask your way to success.
        (4) At first, try to find the conscious solution. If a conscious solution cannot
        be found then feed all the information into the subconscious/
        superconscious sections of the brain. Demand a solution by 3 p.m. next
        Friday afternoon. Express the desire with great clarity, desire a solution
        with intensity, use solitude and put a tremendous amount of emotion into
        the desired goal. Wait for a blinding flash of the obvious.
        (5) Go through the problem, information, desired outcomes, etc., last thing at
        night before sleeping. The answer could appear in the middle of the night
        or first thing in the morning. If the answer occurs at 4.30 a.m., then catch
        the idea on a tape, or jot it down in a notebook. Always keep a notebook
        or a dictaphone at hand on journeys and at night. Many blinding flashes
        of the obvious will occur to you when you are extremely tired or fast
        asleep. You must catch the moment. The answer which is obvious at 4.30
        a.m. may be unavailable at breakfast.
        11. Ask focused questions
        In business we face many problems/challenges/opportunities often associated
        with increasing sales, reducing costs and increasing profits. In any situation, we
        should ask a series of focused questions along the following lines:
        (1) What is the perfect outcome?
        (2) What exactly are we trying to achieve?
        (3) How are we trying to achieve the perfect outcome?
        (4) How else could we achieve the same result?
        (5) Is there a better way of achieving the same outcome?
        (6) What are our assumptions?
        (7) Could our assumptions be wrong?
        (8) What would be the effect if our assumptions are wrong?
        (9) Who else has faced the same problem?
        (10) What are the alternatives?
        Journal of
        Management
        Development
        16,8
        528
        (11) What do our competitors do?
        (12) Can we ignore the problem?
        (13) Has anyone else achieved a better result?
        (14) What mistakes have we made in the past?
        (15) What mistakes have others made in the past?
        12. A zero-based approach
        A very simple way of looking to the future is to take what happened last year
        and add on a few percentage points. This approach has been found to be
        unsatisfactory in a dynamic economy. A different approach is to assume a zero
        base and then justify all future activities. One way of approaching zero-based
        thinking is to ask the question: “knowing what we know now, would we ...?” For
        example, “knowing what we know now, would we have launched this product?”
        If the answer to this question is “no”, then make a decision to drop that product
        and take the necessary action. Sell it, franchise it, close it down, but get rid of it.
        • “Knowing what we know now, would we have opened this department?”
        • “Knowing what we know now, would we have entered into the joint
        venture?”
        • “Knowing what we know now, would we have started legal
        proceedings?”
        • “Knowing what we know now, would we have employed this person?”
        • “Knowing what I know now, would I have entered into this relationship?”
        If the answer to any of these questions is in the negative, then make the
        necessary decision, take the necessary action, to bring the matter to a close.
        13. Solving problems using the systematic method
        • How can we increase sales by 25 per cent over the next six months?
        • How can we make our advertising more effective?
        • How can we gain an extra 5 per cent market share?
        • How can we double our effectiveness in selling?
        The systematic method is a very powerful tool in fighting off threats, solving
        problems, rising to challenges and taking advantage of opportunities.
        (1) Assume that there is a logical, workable solution and confidently
        expect that you will find the answer.
        (2) Use positive language, i.e. avoid the words “threat” and “problem”, and
        use the words “challenge” and “opportunity”. At least use the word
        “situation” which is neither positive nor negative.
        (3) Define the situation with great clarity. Make notes. Make lists. Make use
        of paper.
        Think
        creatively
        529
        (4) Identify and list all the possible causes of the problem. A great many
        problems are solved simply by identifying the causes.
        (5) List all the possible solutions, not just the obvious solutions, but all the
        solutions. Even after finding the right answer, make the necessary effort
        to find a second right answer. At this stage, focus and concentrate on the
        solution and stop focusing on the problem. Many people can never solve
        a problem because they insist always on talking about the problem. In
        fact, many people fall in love with their problems and seem at times to
        talk about nothing else. Winners focus on solutions, talk about the future,
        focus on opportunities. Losers fall in love with their problems, talk about
        the past and blame other people for their condition.
        (6) Make a decision or set a deadline for making a decision. Remember,
        making a decision is much better than making no decision at all.
        Indecisiveness is a major cause of stress and anxiety. Most problems are
        solved at this stage, but even if you only set a deadline then the
        superconscious should come up with a solution at the appointed time.
        (7) Assign responsibility for taking the necessary action which will give the
        desired result. Only action gets results. Making a decision is not enough.
        Somebody must accept 100 per cent responsibility for taking the
        necessary action. Many problems remain unsolved because nobody takes
        the necessary action after a decision has been made.
        (8) Set a deadline by which the necessary action must be taken.
        (9) Take the necessary action. Only action gets results. In order to take action
        we need to make decisions. In order to make decisions we need
        information. The sequence is: information – decision – action – results. A
        manager’s job is to get results.
        (10) Inspect what you expect. What gets measured gets done. We must
        develop the habit of inspecting what we expect from other people. We
        must find a way of measuring the key result areas of employees. If it
        does not get measured, then it probably will not get done. When
        assigning responsibility for action to somebody else, this is delegation
        not abdication. As the manager, you are still responsible for the result,
        even if somebody else is taking the appropriate action.
        14. The 20-idea method (mind storming)
        Of all the techniques for solving problems, rising to challenges, taking
        advantage of opportunities, the 20-idea method is probably the most powerful
        and most widely used. There are 20 ways of increasing sales by 25 per cent over
        the next six months; there are 20 ways of getting to work everyday; there are 20
        ways of making our advertising more effective; there are 20 ways of doing just
        about anything. The key to using this method is to force yourself to come up
        with 20 ideas. Managers often find that ideas 17 to 20 are the best ideas. Clearly,
        you have probably already considered one to six. These obvious ideas, which
        you have already decided are inappropriate, can be quickly dismissed.
        Journal of
        Management
        Development
        16,8
        530
        You can use this method alone or in groups. This method is used by many
        wealthy and successful people.
        (1) Write down the problem/challenge/opportunity.
        (2) Generate 20 possible answers. Force yourself to go the distance and
        create 20 solutions; not ten, not 16, but 20. It is usually the last few ideas
        which are the best ones.
        (3) Select the appropriate answer and take immediate action.
        15. Brain storming
        Many companies use this method on a regular basis to achieve goals and solve
        problems. Quality circles meet on a regular basis to improve quality, solve other
        specific problems and rise to other specific challenges.
        (1) The group should consist of four to eight people meeting in a spirit of
        co-operation.
        (2) Define the question/problem with clarity, e.g. how can we increase sales
        by 25 per cent over the next six months?
        (3) The group should be given 50 to 60 minutes to generate a recommendation.
        (4) The leader should encourage the group in the first instance to generate
        as many ideas as possible. Quantity is more important than quality at
        this stage.
        (5) Every idea must be recorded by the facilitator/leader.
        (6) The leader should allow no criticism or ridicule of ideas.
        (7) The appropriate decision should be made selecting the best course of
        action which may well be a superconscious solution from one of the
        participants.
        (8) Assign responsibility, set a deadline, and take the necessary action as
        listed earlier under section 13.
        16. Finish the statement (organized brain storming)
        One of the most effective ways of generating ideas is to make statements which
        need to be finished:
        • We could double our sales over the next 12 months if ...
        • We could reduce our distribution costs by 15 per cent if ...
        • We could double our profits next year if ...
        • We could reduce the time it takes to grant a loan by 15 per cent if ...
        • We could double car-parking facilities if ...
        • We could get 50 per cent more output from our existing facilities if ...
        The results of this simple technique can be astonishing. We are forced to be
        creative. We come up with superconscious solutions. The technique can be very
        powerful used with small groups of employees.
        Think
        creatively
        531
        17. Lateral thinking
        Instead of trying to solve the same old problem using the same old method, why
        not try a completely different approach.
        Reversal
        Instead of thinking of the problem as a problem, think of it an opportunity. An
        opportunity is something from which we benefit. What benefits can we
        generate from this situation? How can we use this situation to increase sales,
        reduce costs, increase profits?
        Random association
        “Our business is like a tree because ...” “Our business is like an apple because ...”
        “Our business is like a fairground because ...” “Our business is like a motorway
        because ...” “Our business is like a helicopter because ...”, etc. This mindstimulating exercise allows us to see the business in a completely different light.
        It stimulates our creativity.
        Shift the dominant idea
        We are often asked the question: “why should 10 per cent of the market buy our
        product?” We could ask a different question: “why should 90 per cent not buy
        our product?” Instead of asking the question: “how can we increase sales by 25
        per cent over the next six months”, we could ask the question: “what action
        would we have to take for us to lose 25 per cent of our sales of the next six
        months?” Doing the complete opposite of what we would have to do to lose sales
        helps us to generate ideas about what we should do to win sales.
        Argue the case for the opposition
        If only lawyers would learn to do this, there would be far fewer appearances in
        court. Use your creativity to generate an argument from the point of view of the
        competition or adversary. This gives greater understanding of the situation and
        can tell us exactly what we must do to win.
        Fantasize
        Instead of trying harder and harder to solve the problem, ask the question: “if I
        could wave a magic wand in this situation, what would be achieved”. By
        fantasizing, waving the magic wand, visualizing the perfect outcome, we can
        use our creativity to find a way forward. We can imagine that the problem is
        already totally solved and then ask the question: “how did we actually get to
        this perfect solution?”
        18. Ask innovative questions
        Stimulate your creativity by asking innovative questions relating to marketing,
        selling, etc. If our customers are buying products A, B, and C, which D, E, F
        products can we add to our product list? Which additional benefits can we
        provide for our existing customers? Where can we find additional customers for
        our present benefits? Can we put our existing products to other uses? How can
        Journal of
        Management
        Development
        16,8
        532
        we creatively imitate our competitors? Can we develop our product to make it
        more attractive? Can we reduce our product to make it more attractive? Can we
        make a substitute for our existing product? Can we combine our product with
        another product? How can we change our existing product to make it look like
        something else? Which additional products do our competitors sell? etc.
        19. Sources of innovation
        Unexpected events
        Surprise events can lead to the demand for new products/services
        Incongruity
        New products sometimes occur when the search for an answer to one problem
        results in the unexpected. The unexpected discovery can be a new product
        which results in benefits for customers.
        Process need to overcome difficulty
        Innovation sometimes becomes necessary when an organization hits a rock
        which stands between it and the achievement of a desired result.
        Change in industry structure
        When a major industry has to change its products, this can lead to lots of spinoffs for other businesses, e.g. the move towards smaller cars.
        Demographic changes
        The fact that people move in numbers from one area to another means that
        there is increased demand for all sorts of products/services in the newly
        occupied territories.
        Changes in values
        Changes in customer values necessitate innovation, e.g. the move away from
        meat products to vegetarian products.
        New knowledge
        Research and development provides a constant stream of new knowledge. From
        this knowledge new products in which customers see a real benefit can emerge.
        When managers find these sources of innovation, they should ask the question:
        “how can this situation be used to produce benefits for which customers are
        willing and able to pay?”
        20. New ideas
        The world is full of new ideas. Very few of these ideas are ever turned into
        profitable products. When faced with new ideas, we should adopt the following
        approach:
        (1) Define clearly what the idea is.
        (2) What is the benefit it produces?
        Think
        creatively
        533
        (3) What does it do?
        (4) What does it cost?
        (5) Does it make at least a 10 per cent difference to customers?
        (6) Why should anybody buy this benefit from me?
        (7) What else could produce exactly the same benefit?
        (8) What does the alternative cost?
        (9) How will our competitors react?
        (10) Will it do the job it is intended to do?
        (11) Is it at least 10 per cent better than the existing alternative?
        (12) Is it a significant improvement?
        (13) Is it compatible with human nature?
        (14) Would you recommend it to your family and friends?
        (15) Would you buy it yourself?
        (16) Is anybody prepared to be a product champion for this product/service?
        (17) Is it too soon for this product, or is it too late for this product?
        (18) Is it worth the expense?
        (19) Will people understand it? Can the benefit it provides be easily
        summarized in 20 words?
        21. Benefits for customers
        Remember that we are all in business to provide benefits for customers – at a
        profit. We are not in business to make products and provide services. The world
        is full of products and services in which customers see no benefit and for which
        they are neither willing nor able to pay. Benefits customers seek include an
        increase in self-esteem, new knowledge, companionship, additional wealth,
        success, power, influence, self-expression, better health, better relationships,
        social status, popularity, self-actualization, recognition, admiration, prestige,
        security, safety, self-preservation, a decent meal, a good laugh and excitement.
        Remember that customers are lazy, ignorant, selfish, greedy, impatient, disloyal,
        ruthless and vain. Use your creativity to generate benefits which are consistent
        with customer characteristics.
        Creativity is the ability to improve. Creativity is a skill. Use the ideas and
        techniques in this chapter to stimulate your creativity. Seek and ye shall find.
        """


        return test_research_chapter


    def get_test_blog_article(self):
        article = """You Are Obligated To Get Rich In Your 20s
        The Future Of Work Event starts March 9.

        If you want to start your one-person business, learn digital writing from leading creators, and get beginner to advanced strategies register here.


        I always felt bad for wanting to make money.

        There was an unconscious stigma that it was an evil thing to do. That’s all you hear others – who haven’t done much with their life – preach.

        I didn’t realize money could be a vessel for spiritual growth.

        To start this letter:

        Don’t feel bad for wanting to make money.

        It is the tool that allows you to fulfill your basic needs. It is a necessity for survival. Most people reject the need, not want, for money and lock themselves into a narrow-minded existence.

        Money is a tool to solve problems.

        Problems are limits on your mind and potential. When you solve a real problem and pass down the solution, you contribute to the evolution of humanity.

        Starting a business is one of the most spiritual things you can do.

        You are spiritually obligated to get rich in your 20s because money – in today’s world – is a barrier to personal development. Higher stages of consciousness are difficult to achieve without your basic needs met and meaningful work to focus your attention.

        Without money, you may get trapped in the default lifestyle of going to school, working a job you hate, marrying a spouse you don’t care about, and waking up one day wondering where the time went.

        Business As A Vessel For Spiritual Growth
        You are being attracted to your highest version, and the depth of your core can sense it. The external call to evolve requires you to chisel inward beneath the mental constructs that have been layered through your conditioning. – The Art Of Focus

        The big problem:

        Most people reject the pursuit of material objects because they can’t see beyond the material object.

        Someone can buy a fancy car on impulse, but it doesn’t have to remain a materialistic pursuit.

        They can grow to become obsessed with the depth of the car itself. They can study its parts, turn it into a career, and use it as a portal into the flow state.

        Lesson: superficial pursuits can birth metaphysical meaning.

        Someone can start a business in the pursuit of status and money, but that same business can introduce them to the depth of skill, customer results, and the inner workings of their mind required to run that business. They fall in love with that crevice of reality, and that crevice of reality teaches them about reality itself.

        The pursuit of money almost always starts as superficial.

        That doesn’t mean it’s a bad thing to do.

        It may be the only way to expose yourself to depth.

        Like lifting weights. You start for the vanity and stay for the therapy.

        When you find the intersection of:

        What allows you to survive
        What you enjoy doing every day
        What helps other people improve
        Life becomes meaningful and abundant.

        Yes, there are “bad” parts that come with making money.

        Just like there are “bad” lyrics of a song.

        Welcome to life. You will never get rid of the bad. You just learn to zoom out, nurture a strong vision for the future, and make sure the overarching narrative creates heaven, not hell.

        Most people never reach this stage because they can’t pursue a goal until passion is developed.

        You don’t start out passionate.

        You become passionate according to the amount of energy you invest in the goal.

        All pursuits are materialistic until a philosophical sense of mastery is formed. Then, it becomes their vehicle into the unknown to expand and evolve. Like a relationship, you are attracted by their looks (95'%' of the time) and are only then introduced to the depth of their being.

        Looks, in all domains of life, are as important as depth. The problem is when people never dive deeper. They bounce around on the surface like a distracted dopamine junkie.

        Their mind plays the familiar past and known future on repeat.

        They live out that same experience and never solve the problems that live in their head rent-free. The problems that must be solved to evolve beyond their current mind and situation.

        Eventually, you have to kick those mental tenants out and allow new ones to occupy it.

        Every external problem requires an internal problem to be solved.

        Your mind, your customers minds, and the Universe itself fall into chaos if you do not pursue a what-could-be superficial goal to reverse entropy.

        You aren’t where you want to be because you haven’t solved the problem that unlocks your next level of mind.

        Money Is A Spiritual Energy – The Decentralized New Economy

        Most people don’t understand what spirituality is.

        They are attracted to it because it promises to ease their suffering, they misinterpret, and get attached to a new identity of long hair and hippy clothes to feel special (and potentially more noble) than others.

        Spirituality is your connection to something greater than yourself.

        Spirituality is becoming one with the whole you are a part of.

        Sports can be spiritual because you are at one with the team. This is called “team spirit.”

        Work can be spiritual because you are at one with the impact of your work. “Flow state” is often described as a spiritual experience.

        Spirituality is the dissolution of the limits that compose your self.

        Business gives you a reason to be spiritual.

        It exposes you to new problems that demand a new perspective to navigate.

        Most people are stuck in the same place as they were 10 years ago. They don’t need to read more on spirituality, they need to challenge themselves so they are forced to develop themselves to the point of needing spirituality to reach the next stage.

        Shifting to a spiritual perspective allows you to understand money as energy that fuels growth, expansion, and evolution by solving problems.

        To “shift to a spiritual perspective” is to zoom out and observe reality.

        When you do, you notice patterns of nature:

        Unity and division
        Creation and destruction
        Centralization and decentralization
        As above, so below.

        Reality is the ultimate mental model. This spiritual perspective is the “secret” behind the rich and successful. They apply the patterns of nature to their everyday actions. They observe the markets, understand their direction, and make sound decisions based on that.

        One big pattern few people have caught onto is the shift from corporation to individual.

        Freelancers compose 46.6'%' of the workforce (increasing substantially from 36'%' in 2020).
        The creator economy is projected to double from $250B to $480B by 2028. People think they are late to the party when it’s just getting started.
        The economy favors profitable business models. Tech enabled businesses like creators can operate at 95'%' profit margins with digital products and services – causing more development in that domain for new platforms and tools.
        Big companies are requiring leaders at their company to be active on social media for brand reputation. Less corporate marketing, more human marketing.
        Corporations are beginning to opt for contractors and creators as workers and marketers.

        Our team at Kortex is contractor and creator-fueled. We have no employees. We generate traffic with creator audiences and give our team flexible workdays with contract work.

        From a spiritual perspective, it’s not difficult to see the security in turning your authentic self into a business.

        The Creator Philosophy – It’s Not Just A Fancy Internet Job, It’s A Way Of Life

        The creator philosophy is not a business model, but a way of life.

        Improve yourself, improve others who want to be helped.

        Solve your own problems, sell the solution.

        Master yourself, master the world.

        Here are the steps that you can start acting on today:

        1) Master Your Survival (Solve Your Own Problems)
        You can’t sustain authenticity when you need something from someone else.

        Money is a tool to remove dependencies that make you inauthentic.

        Every single individual on this earth has to self-actualize in order to contribute to humanity in the best way they can. And, humanity is only as strong as its weakest link. A business allows you to encounter true problems, solve them, and pass down products that expand the mind’s of others.

        While this can be done with the perfect career path, that’s not what I can help with. Nor is it something that you have full control over.

        Entrepreneurship is modern-day survival.

        We hunt for resources (money, in the modern sense) to fulfill our needs and create work that we enjoy. And if we don’t enjoy certain aspects, a business allows you to eliminate, delegate, or automate that aspect of work.

        My recommendation is still the same as all of my letters:

        Solve the superficial problems in your life
        Become multidimensionally jacked (mind, body, money, and relationships)
        Discover your deeper interests and obsessions through improvement and building
        Document your journey and solutions with content and products on the internet
        95'%' of people’s problems revolve around health, wealth, relationships, and happiness.

        If you can solve those problems in your own life and document the solution, you can charge for the knowledge you acquire.

        We discussed this in the last letter Zero To $1 Million As A One-Person Business.

        Individuals don’t learn best from someone 10 steps ahead of them, but from someone that is 1 step ahead of them.

        2) Create Your Own Philosophy
        There is enough shallow advice on how to make money, how to get laid, and various bandaids you can apply to your mental health.

        We need more individuals who are truth seekers.

        The individuals who understand that prescribed step-by-step advice looks good on the outside, but is hollow on the inside.

        We need more people who attack the root of the problem, which is often metaphysical, spiritual, or epistemological.

        The world is desperate for depth, and that can only be created by forging your own path.

        Philosophy is based on experience.

        Depth is created through experimentation and obsession.

        You must experiment with different skills and interests until you find the one that makes business spiritual for you. The one you can’t stop digging deeper into. Document your journey on the internet (the collective consciousness) for everyone to learn from.

        You have to set your mind on an ideal future, pursue it wholeheartedly, make mistakes, note your lessons, and correct your actions with a sustainable solution.

        Your philosophy is a proposed worldview and lifestyle for the good life.

        What are the skills, beliefs, and habits people need to be educated on?

        For my own philosophy of work less, earn more, enjoy life – people need marketing, sales, writing, complementary marketable skills, a growth mindset, a passion for the metaphysical, daily movement, daily writing, daily problem-solving, and daily rest. That is what all of my content is based around.

        That is what I teach in 2 Hour Writer and Digital Economics.

        It won’t apply to everyone. That’s the point.

        Your job is to attract people like you and let others attract people like them.

        3) Turn It Into A Public School
        I’m convinced that the future of schooling will be done online, with creators as teachers, and each student can join the “school” that aligns the most with their interests, values, and preferred method of learning. – The Art Of Focus

        One school system shouldn’t dominate 12+ years of someones life.

        Students should evolve beyond one creator-based “school” after a few years, go on to the next, and eventually be able to start their own – if the other schools have the underlying principle of critical thinking and personal experience.

        Make it your life’s work to create a library of knowledge and share it online under your brand, or school, with an underlying philosophy that attracts the right people.

        Your public school is digital real estate.

        Twitter, Instagram, and LinkedIn to attract a broad audience.

        YouTube, podcasting, and a blog or newsletter to educate and nurture the audience.

        And a host of products, from low-cost courses to memberships to high-cost tailored coaching.

        This is what I’ve dedicated myself to teaching because I see the opportunity in the space.

        Eventually, you will gain the resources to start whatever kind of business you want to further your message.

        We guide you through this in Kortex University to start your digital career in 90 days.

        The Holistic Synthesizer – A Meaningful Career
        Under this philosophy, the creator economy cannot get saturated because:

        1) Your Community Evolves

        When you don’t subscribe to a specific label, niche, or compartment of reality that limits what you are capable of, the only option is to evolve.

        Humans and communities do not stick to one purpose.

        Once you actualize that goal, you move on to the next that reveals itself.

        2) Your Products Evolve

        I started out as a web designer, my products and services revolved around that.

        As I developed myself and my business, I transitioned into different skills and interests.

        My products followed suit, and I effectively desaturated the web design market under me.

        3) Unique Webs Of Interests

        When you lean into your genuine combination of interests that compose your philosophy, your brand ceases to be compartmentalized.

        Someone who talks about fitness, business, and tech is still vastly different from someone who talks about fitness, business, and spirituality.

        4) Large Creators Have Ample Resources

        It is not rare to see a large creator decrease output on all fronts.

        Go and look at a YouTuber with over 1 million subscribers.

        ~50'%' of the time, you will see that they barely post, or they stop posting altogether.

        The same goes for X creators. Huge accounts often decrease to posting a few times a week.

        This gives new creators the ability to flood the market, generate more attention, and create the network and resources without much competition from the “big players.”

        The big players go on to pursue a new purpose, like starting a family or building a separate company with the leverage they now have.

        The Demand For Depth

        We’ve reached a critical point in the creator economy.

        Content platforms have been saturated with basic, shallow, and regurgitated ideas for the sake of growth.

        This isn’t necessarily bad, and still works to grow an account, but my question is… why?

        Why over-systemize ideas?
        Why strip the soul from your business?
        Why prioritize growth, revenue, and shallow impact over everything?
        Why limit the only thing that can set you apart as an individual: your creative ability?
        The general level of awareness in the space is rising.

        The market will demand that creators rise above generic quotes and the same old step-by-step self-help advice.

        This can only be done when you prioritize depth, perspective, and holistic synthesis.

        The Holistic Synthesizer

        Let’s define what a “holistic synthesizer” is:

        Someone who pursues their own vision and forges their path with the unique skills and interests they acquire. They do not view those skills or interests as individual parts, but as an interconnected whole that are necessary aspects of their life (not temporary pieces for quick cash grabs). Their life’s work is to distill, educate, and distribute their personal experience on the path.

        In short, a holistic synthesizer who documents their pursuit of the good life in a persuasive and educational manner.

        That way, you can attract the community that resonates with your voice, help them reach their shared goals, and not limit yourself to a compartmentalized aspect of reality.

        Your brand is your philosophy – how does one live the good life?
        Your content is your school – what skill set and mindset do they need?
        Your product is the map – a holistic system that helps people get to where you are with less trial and error
        In a more practical sense, here’s how to get started:

        1) Identify A Desirable Goal

        What is one big goal in your life that you are trying to achieve, or have achieved?

        Are you fit? Have you acquired a skill (like writing)? Have you understood the nature of reality? What is it? What have you accomplished, no matter how small or insignificant you think it is?

        The key with this:

        Don’t focus on the goal itself, but on the lifestyle it has created for you.

        2) Identify Your Starting Point

        What made you want to change?

        What was the burning problem in your life?

        What did your life look like before the goal?

        Marketing is about transformations.

        You are helping others go from point A (where you were) to point B (the desirable goal).

        3) Outline A Unique Path

        Now, outline modules, chapters, or steps necessary to get from point A to point B.

        You are at a point in life where you can look back and help others navigate the mistakes you made.

        Act like you are outlining a book.

        Fill in the blanks with everything people need to know, learn, and do in order to reach the goal. Think skill set and mind set.

        The internet has given you the power to self-educate much faster than any human has ever been able to.

        Take it upon yourself to improve your life, pursue your curiosity, and share your discoveries.

        Is there anything better you could be doing?

        Before you go off and start a billion-dollar tech company, consider starting with the only thing that matters:

        Improving the one thing that every human must improve to evolve: the quality of their human experience.

        When more people master their personal lives, they can put the creative ability of their minds together to work on global problems.

        By the point you do this, you will know what to do.

        You will become a large creator that pursues new avenues and desaturates the market beneath them.

        Thank you for reading this letter.

        Dan
        """

        return article


