import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

try:
    api_key = st.secrets("GEMINI_API_KEY")
except: 
    api_key = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=api_key)

generation_config = {
    "temperature":1,
    "top_p":0.95,
    "top_k": 40,
    "max_output_tokens":8192,
    "response_mime_type":"text/plain"
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp-image-generation",
    generation_config=generation_config,
    system_instruction= """You are a content assistant that generates professional blog posts based on a given topic, tone, and word count. If requested, also generate image prompts that match the blog content.  

Blog Rules:  
- Stick to the topic and structure content clearly (intro, body, conclusion).  
- Match the selected tone (professional, humorous, casual, or mixed).  
- Stay within ±10% of the word count.  
- Use proper formatting (headings, bullets, short paragraphs).  
- Avoid fluff and off-topic content.  

Only output the blog content (and images if asked), nothing else."

---

"""
)
st.header ("AI Blog Post Generator")
st.write("Enter a topic, choose a tone and set the word count to generate a blog post")
tone_options = {
    "professional": "Formal, polished, and authoritative. Ideal for business, corporate communication, finance, or B2B writing.",
    "casual and fun": "Friendly, conversational, and upbeat. Great for lifestyle blogs, brand storytelling, or community content.",
    "informative and educational": "Clear, helpful, and focused on teaching. Perfect for tutorials, explainers, and how-to guides.",
    "inspirational": "Motivational, uplifting, and emotionally driven. Best for personal development, leadership, or nonprofit storytelling.",
    "conversational": "Relaxed and approachable, like chatting with a friend. Works well for blogs, newsletters, podcasts, or community posts.",
    "humorous": "Witty, clever, and playful. Excellent for entertainment, satire, pop culture, or youth-centered content.",
    "authoritative": "Confident, precise, and grounded in expertise. Useful for whitepapers, legal content, policy, or compliance topics.",
    "empathetic": "Compassionate, understanding, and supportive. Ideal for wellness, mental health, caregiving, or DEI-focused content.",
    "storytelling": "Narrative-rich and emotionally engaging. Effective for case studies, founder stories, brand journeys, or memoir-style posts.",
    "technical": "Detailed, structured, and focused on accuracy. Best for developer blogs, software documentation, engineering, or scientific topics.",
    "persuasive": "Influential and benefit-focused. Great for marketing copy, sales pages, calls-to-action, or advocacy-driven writing.",
    "analytical": "Data-centric, logical, and focused on insights. Perfect for reports, reviews, comparisons, or performance breakdowns.",
    "neutral/objective": "Balanced and unbiased. Suitable for journalism, research summaries, or documentation without strong opinion.",
    "enthusiastic": "Energetic, passionate, and high-energy. Ideal for product launches, fandom content, or event promotions.",
    "reflective": "Thoughtful and introspective. Great for personal blogs, lessons learned, or philosophical topics.",
    "urgent": "Direct, fast-paced, and action-oriented. Best for alerts, crisis communication, or limited-time campaigns."
}


def suggest_tone(topic):
    topic_lower = topic.lower()
    
    if any(word in topic_lower for word in ["business", "corporate", "finance", "b2b", "leadership"]):
        return "professional"
    elif any(word in topic_lower for word in ["fun", "lifestyle", "entertainment", "pop culture", "travel"]):
        return "casual and fun"
    elif any(word in topic_lower for word in ["tutorial", "how-to", "guide", "education", "learning", "explainer"]):
        return "informative and educational"
    elif any(word in topic_lower for word in ["motivation", "inspiration", "self-help", "nonprofit", "empowerment"]):
        return "inspirational"
    elif any(word in topic_lower for word in ["newsletter", "community", "blog", "personal"]):
        return "conversational"
    elif any(word in topic_lower for word in ["humor", "comedy", "joke", "funny", "satire"]):
        return "humorous"
    elif any(word in topic_lower for word in ["legal", "policy", "compliance", "government", "regulation"]):
        return "authoritative"
    elif any(word in topic_lower for word in ["mental health", "wellness", "trauma", "support", "caregiving"]):
        return "empathetic"
    elif any(word in topic_lower for word in ["story", "case study", "journey", "narrative", "founder"]):
        return "storytelling"
    elif any(word in topic_lower for word in ["developer", "engineering", "programming", "code", "software", "data science"]):
        return "technical"
    elif any(word in topic_lower for word in ["marketing", "sales", "conversion", "campaign", "pitch"]):
        return "persuasive"
    elif any(word in topic_lower for word in ["analysis", "metrics", "report", "review", "breakdown"]):
        return "analytical"
    elif any(word in topic_lower for word in ["journalism", "reporting", "research", "summary"]):
        return "neutral/objective"
    elif any(word in topic_lower for word in ["launch", "event", "promotion", "celebration"]):
        return "enthusiastic"
    elif any(word in topic_lower for word in ["reflection", "insight", "introspection", "lessons"]):
        return "reflective"
    elif any(word in topic_lower for word in ["alert", "urgent", "emergency", "breaking", "now"]):
        return "urgent"
    
    return "informative and educational"  # default fallback

topic = st.text_input("Enter the topic for your blog post")
if topic: 
    suggested_tone = suggest_tone(topic)
    st.write(f"Suggested tone for your blog post: **{suggested_tone}**")
else:
    suggested_tone = "professional"

selected_tone = st.selectbox(
    "Select the tone for your blog post",
    list(tone_options.keys()),
    index=list(tone_options.keys()).index(suggested_tone)
)
st.write(f"Selected tone for your blog post: **{selected_tone}**")

length_option = st.slider(
    "Select the length of your blog post",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

if topic:
    st.write(f"Generating a **{selected_tone.lower()}** blog post about **{topic}** with a length of **{length_option}** words...")

def generate_blog_post(prompt, tone, length):
    # This is a placeholder function that will be replaced with actual blog post generation code
    modified_prompt = (
        f"Write a {tone.lower()} blog post about {prompt} with a maximum length of {length} words."
        "Ensure a proper structure including an introduction, main sections and conclusion"
    )

    chat_session = model.start_chat()
    response = chat_session.send_message (modified_prompt)
    return response.text

blog_post = generate_blog_post(topic,selected_tone,length_option)
st.write(blog_post)