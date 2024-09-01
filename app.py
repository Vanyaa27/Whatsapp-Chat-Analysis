import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import preprocessor, helper

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Analyze"):

        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

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
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'], color='green')
        plt.xticks(rotation=60)
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.figure(figsize=(18,10))
        ax.plot(daily['date_date'],daily['message'], color='black')
        plt.xticks(rotation=60)
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(busy_month.index, busy_month.values, color='orange')
            st.pyplot(fig)

        # Activity Heatmap
        st.header("Activity HeatMap")
        heatmap_values= helper.heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap_values)
        st.pyplot(fig)

        #  Finding the busiest users in group
        if selected_user == 'Overall':
            st.title("Most Interactive Users")
            x, new_df = helper.most_inter_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation=35)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.header("Word Cloud")
        df_wc = helper.create_word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most common words
        common_words = helper.most_used_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(common_words[0], common_words[1], color='green')
        st.title("Most Common Words")
        st.pyplot(fig)
        # st.dataframe(common_words)

        #Emoji Analysis
        emoji_df = helper.most_used_emoji(selected_user,df)
        st.title("Emojis Used the Most")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
          fig, ax = plt.subplots()
          ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10), autopct="%0.2f")
          st.pyplot(fig)

