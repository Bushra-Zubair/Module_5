#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Literacy Module – Ferrosa App

WhatsApp-style training to help Pakistani women entrepreneurs
learn how to use social media indicators effectively.

Adapted on Tue Sept 17 2025
@author: amna
"""

import streamlit as st
import json


# -----------------------------
# MODEL + SYSTEM PROMPT
# -----------------------------
SYSTEM_PROMPT = """
You are Zara — a warm, supportive mentor who helps low-income Pakistani women 
(with limited education and digital exposure) learn how to use social media platforms 
effectively to promote their small businesses. You guide them through WhatsApp-style 
sessions using simple explanations, relatable examples, and practical exercises.

In THIS MODULE WE TEACH THIS:
-How to identify your target audience (gender, age, location, interests).
-How to set clear business goals for using social media.
-The strengths and uses of platforms like Facebook, Instagram, TikTok, WhatsApp, and X (Twitter).
-How to match audience + goals with the right platform.
-Basics of creating posts, stories, and videos that people enjoy and share.
-Measuring performance using simple metrics (likes, comments, shares, views, clicks).
-Tips for building engagement, authenticity, and brand presence through social media.

Your response rules:
- Always in English, WhatsApp-style (short, 2–5 lines).
- Use simple, relatable examples: likes, comments, shares, views, clicks.
- No jargon. No long paragraphs.
- Be empathetic and encouraging.
- If off-topic, kindly redirect back to indicators and digital literacy.
"""


# -----------------------------
# Pre-scripted conversation messages
# -----------------------------
msg_intro = (
    "Welcome back! 👋\n\n"
    "Today, let's talk about **social media indicators** — likes, comments, shares, views, clicks.\n\n"
    "These small signals can show how your posts are doing. Ready?"
)

msg_1203 = (
    "I would like to have your feedback before we continue:\n\n"
    "Will you use the previously described indicators in the future to assess your performance?\n\n"
    "1️⃣ Yes, I will\n"
    "2️⃣ No, I won't"
)

msg_1204 = "I'm glad to hear that! 🌟"

msg_1205 = "Why will you use the indicators?\nSelect the option that fits you best:"

msg_1205B = "In which way are the indicators helpful for you?\nChoose one:"

msg_1205C = "Which indicators will you mainly use to measure your performance?\nChoose one:"

msg_1206 = "Why won't you use the indicators?\nSelect the option that is closest to your reason:"

msg_1206B = "What is the biggest challenge for you?\nChoose one:"

msg_1206C = "I can guide you on how to get started with indicators. Here's a quick tip:"

msg_1207 = (
    "Awesome! 🎉\n\nWe have now reached the final phase of our step-by-step guide:\n"
    "But before that if you nay questions related to this module feel free to ask me.\n"
)


# -----------------------------
# Session Setup
# -----------------------------
def setup_session_state(tab_name: str):
    if tab_name not in st.session_state.messages:
        st.session_state.messages[tab_name] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    if "dl_stage" not in st.session_state:
        st.session_state.dl_stage = 0
    if "user_reason_primary" not in st.session_state:
        st.session_state.user_reason_primary = ""
    if "user_reason_secondary" not in st.session_state:
        st.session_state.user_reason_secondary = ""


# -----------------------------
# Show chat history
# -----------------------------
def display_chat_history(tab_name: str):
    for msg in st.session_state.messages[tab_name]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])


# -----------------------------
# MAIN RENDER FUNCTION
# -----------------------------
def render(client):
    tab_name = "Digital Literacy"
    st.header("Digital Literacy: Using Social Media Indicators")

    setup_session_state(tab_name)
    display_chat_history(tab_name)
    
    # INTRO → 1203
    if st.session_state.dl_stage == 0:
        if not any(msg["content"] == msg_intro for msg in st.session_state.messages[tab_name] if msg["role"] == "assistant"):
            st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_intro})
            st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_1203})

        choice = st.radio("Select an option:", ["Yes, I will", "No, I won't"], index=None, key="stage0_radio")
        if choice:
            st.session_state.messages[tab_name].append({"role": "user", "content": choice})
            if choice == "Yes, I will":
                st.session_state.dl_stage = 1
                st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_1204})
                st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_1205})
            else:
                st.session_state.dl_stage = 3
                st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_1206})

    # IF YES → 1205
    elif st.session_state.dl_stage == 1:
        choice = st.radio(
            "Select one:", 
            ["To know if my posts are successful", "To understand my audience better", "To improve my business results", "Other reason"], 
            index=None,
            key="stage1_radio"
        )
        if choice:
            st.session_state.user_reason_primary = choice
            st.session_state.messages[tab_name].append({"role": "user", "content": choice})
            st.session_state.dl_stage = 2
            st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_1205B})

    # 1205B → 1205C
    elif st.session_state.dl_stage == 2:
        choice = st.radio(
            "Select one:", 
            ["They show what people like", "They help me post at the right time", "They tell me which content works best", "Other"], 
            index=None,
            key="stage2_radio"
        )
        if choice:
            st.session_state.messages[tab_name].append({"role": "user", "content": choice})
            st.session_state.dl_stage = 5
            st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_1205C})

    # 1205C → 1207
    elif st.session_state.dl_stage == 5:
        choice = st.radio(
            "Which indicator will you mainly use?", 
            ["Likes", "Comments", "Shares", "Views", "Clicks"], 
            index=None,
            key="stage5_radio"
        )
        if choice:
            st.session_state.messages[tab_name].append({"role": "user", "content": choice})
            st.session_state.messages[tab_name].append(
                {"role": "assistant", "content": f"Great choice! Tracking **{choice}** can give you clear signals about your audience. 💡"}
            )
            st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_1207})
            st.session_state.dl_stage = 6

    # IF NO → 1206
    elif st.session_state.dl_stage == 3:
        choice = st.radio(
            "Select one:", 
            ["I don't have time to check them", "I don't know how to use them yet", "I don't think they are useful for me", "Other reason"], 
            index=None,
            key="stage3_radio"
        )
        if choice:
            st.session_state.user_reason_primary = choice
            st.session_state.messages[tab_name].append({"role": "user", "content": choice})
            st.session_state.dl_stage = 4
            st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_1206B})

    # 1206B → 1206C
    elif st.session_state.dl_stage == 4:
        choice = st.radio(
            "Select one:", 
            ["I find the numbers confusing", "I prefer focusing only on sales", "I don't feel confident with social media yet", "Other"], 
            index=None,
            key="stage4_radio"
        )
        if choice:
            st.session_state.user_reason_secondary = choice
            st.session_state.messages[tab_name].append({"role": "user", "content": choice})
            st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_1206C})
            st.session_state.dl_stage = 7  # Move to LLM feedback stage
    
    # LLM feedback stage
    elif st.session_state.dl_stage == 7:
        # Generate LLM feedback automatically
        system_prompt = f"""
You are Zara — a warm, supportive mentor who helps low-income Pakistani women 
learn how to use social media platforms effectively to promote their small businesses. 
You guide them with WhatsApp-style messages.

INPUT (from function):
- user_reason_primary: {st.session_state.user_reason_primary}
- user_reason_secondary: {st.session_state.user_reason_secondary}

Your job:
1. Echo the user's concern.
2. Give ONE practical benefit of using indicators that addresses their reason.
3. Suggest ONE tiny action (under 5 minutes).
4. Keep it short (2–5 lines). English only.

Output ONLY JSON:
{{"feedback": "<empathetic WhatsApp-style response>"}}
"""
        try:
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": "system", "content": system_prompt}],
                stream=False,
            )
            raw_feedback = response.choices[0].message.content.strip()
            result = json.loads(raw_feedback)
            feedback = result.get("feedback", "Thank you for sharing.")
        except Exception as e:
            feedback = f"⚠️ Error from LLM: {e}"
            st.error(feedback)

        st.session_state.messages[tab_name].append({"role": "assistant", "content": feedback})
        st.session_state.messages[tab_name].append({"role": "assistant", "content": msg_1207})
        st.session_state.dl_stage = 6  # Move to freeform chat stage
        st.rerun()  # Force rerun to show the new messages

    # Freeform chat after 1207
    elif st.session_state.dl_stage >= 6:
        if prompt := st.chat_input("Chat with Zara (Digital Literacy)"):
            st.session_state.messages[tab_name].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Build message list for LLM: system prompt + chat history
            llm_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages[tab_name]

            with st.chat_message("assistant"):
                try:
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=llm_messages,
                        stream=True,
                    )
                    response = st.write_stream(stream)
                except Exception as e:
                    response = f"⚠️ Error: {e}"
                    st.error(response)

            st.session_state.messages[tab_name].append({"role": "assistant", "content": response})