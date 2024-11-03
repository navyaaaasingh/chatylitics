import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import re
import random

st.sidebar.title("Chatalytics_AI")

uploaded_file = st.sidebar.file_uploader("Choose a file")

response = {
    "hello": ["Hello, how can I help you."],
    "hey": ["hey there! how can I assist you?"],
    "howdy": ["howdy! what can I do for you today?"],
    "namaste": ["namaste! how can I be of service?"],
    "i feel sad": ["I am so sorry you are experiencing a setback. I dont know what to say, except that care about you, and I am here for you. If you still feel sad you may contact Mr.Tanish at tanii68@happy.com feel free to share you feelings no one is judging you."],
    "i feel energetic": ["It likely means you are a positive, optimistic, bubbly person whom others find inspiring and comforting to be around. Have a good day and keep up the spirit "],
    "i feel depressed": ["It may be hard to believe right now, but the way you're feeling will change. If you still feel the same way feel free to contact tejas69@omg.hpy.in and feel free to share you feelings no one is judging you."],
    "i feel fabulous": ["It likely means you are a positive, optimistic, bubbly person whom others find inspiring and comforting to be around. Have a good day and keep up the spirit "],
    "ok": ["It was nice talking to you if you need any help I am here , I guess time to say bey now "],
    "i am (.*)": ["Why do you say you feel thastreast way?", "How long have you been feeling like this?"],
    "i'm (.*)": ["Why are you feeling like this?", "How long have you been feeling like this?"],
    "i (.*) you": ["Why do you mean ?", "What makes you think you feel that way?"],
    "i (.*) myself": ["Why do you {} yourself?", "What makes you think you () yourself?"],
    "(.) sorry (.)": ["There's no need to apologize.", "What are you apologizing for?"],
    "(.) friend (.)": ["Tell me more about your friend.", "How do your friends make you feel?"],
    "yes": ["You seem quite sure.", "Ok, but can you elaborate."],
    "no": ["Why not?", "Ok, but can you elaborate a bit?"],
    "(.*) ": ["Please tell me more.", "Let's change focus a bit... tell me about your family.", "Can you elaborate on that ?"],
    "": ["Why do you think that?", "Please tell me more.", "Let's change focus a bit... tell me about your family", "Can you elaborate on that ?"],
    "i'm happy to hear that!": ["that's great to hear! what makes you feel so happy?"],
    "i'm feeling a bit down.": ["i'm sorry to hear that. would you like to talk about what's bothering you?"],
    "can we talk about something else?": ["sure, what would you like to talk about?"],
    "you're a good listener.": "thank you! I'm here to listen whenever you need someone to talk to.",
    "good morning": "good morning! how can I make your day great?",
    "good afternoon": "good afternoon! how can I help you this afternoon?",
    "good evening": "good evening! how can I be of assistance this evening?",
    "how are you?": "I'm doing well, thank you for asking! how are you feeling today?",
    "I'm angry": "it's completely understandable to feel angry sometimes. would you like to talk about what's making you angry?",
    "I'm confused": "that's okay, sometimes things can be confusing. what can I do to help clarify things for you?",
    "I'm bored": "I understand feeling bored. would you like to hear a joke or play a game?",
    "I'm lonely": "feeling lonely can be tough. would you like to talk about it, or perhaps I can recommend some activities to help you connect with others?",
    "thank you": "you're welcome! I'm glad I could help.",
    "you're doing a great job": "thank you! I appreciate the kind words.",
    "goodbye": "goodbye! it was nice talking to you. take care!",
}


def match_response(input_text, response):
    lower_text = input_text.lower()
    for pattern, response_list in response.items():
        match = re.search(pattern, lower_text, re.IGNORECASE)
        if match:
            chosen_response = random.choice(response_list)
            return chosen_response

    return "That's interesting. Can you tell me more?"


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # timeline

        # monthly timeline
        st.title("Monthly Timeline of Chats")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Messages')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline of Chats")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Messages')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            ax.set_xlabel('Day')
            ax.set_ylabel('Number of Messages per day')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            ax.set_xlabel('Month')
            ax.set_ylabel('Number of Messages per Month')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Heat Map
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.bar(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)

else:
    st.write("Please upload a file to get started.")


st.title("Chatalytics_AI Psychotherapist Chatbot")

user_input = st.text_input("You:", "")
if user_input:
    response = match_response(user_input, response)
    st.write("Chatalytics_AI: ", response)
