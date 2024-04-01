import streamlit as st
import preprocess, helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set page title and favicon
st.set_page_config(page_title="Whatsapp Chat Analyzer", page_icon=":speech_balloon:")

# Custom CSS styling
st.markdown(
    """
    <style>
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }

    /* Page title */
    .css-2trqyj {
        font-size: 36px;
        font-weight: bold;
        color: #333333;
        margin-bottom: 20px;
    }

    /* Section headings */
    .css-1rx1e5e {
        font-size: 24px;
        font-weight: bold;
        color: #333333;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* Button */
    .css-18olvmw {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .css-18olvmw:hover {
        background-color: #45a049;
    }

    /* Warning message */
    .warning {
        background-color: #ffcc00;
        color: #333333;
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
    }

    /* Horizontal rule */
    .hr {
        border: none;
        height: 2px;
        background-color: #dddddd;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar title and file uploader
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

# Main content
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocess.preprocess(data)

    if df is not None:
        st.write(df)

        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

        if selected_user is not None:
            if st.sidebar.button("Show Analysis"):
                # Fetch statistics
                num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

                # Display top statistics
                st.markdown("<p class='css-1rx1e5e'>Top Statistics</p>", unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f"<p>Total Messages</p><p>{num_messages}</p>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<p>Total Words</p><p>{words}</p>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<p>Media Shared</p><p>{num_media_messages}</p>", unsafe_allow_html=True)
                with col4:
                    st.markdown(f"<p>Links Shared</p><p>{num_links}</p>", unsafe_allow_html=True)

                # Add horizontal rule for separation
                st.markdown("<hr class='hr'>", unsafe_allow_html=True)

                # Monthly timeline
                st.markdown("<p class='css-1rx1e5e'>Monthly Timeline</p>", unsafe_allow_html=True)
                timeline = helper.monthly_timeline(selected_user, df)
                fig, ax = plt.subplots(figsize=(20, 8))
                ax.plot(timeline['time'], timeline['message'], color='green')
                plt.xticks(rotation='vertical')
                plt.tight_layout(pad=3)
                st.pyplot(fig, clear_figure=True)

                # Daily timeline
                st.markdown("<p class='css-1rx1e5e'>Daily Timeline</p>", unsafe_allow_html=True)
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
                plt.xticks(rotation='vertical')
                col1, col2 = st.columns(2)
                with col1:
                    st.pyplot(fig)

                # Activity map
                st.markdown("<p class='css-1rx1e5e'>Activity Map</p>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("<p>Most busy day</p>", unsafe_allow_html=True)
                    busy_day = helper.week_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_day.index, busy_day.values, color='purple')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.markdown("<p>Most busy month</p>", unsafe_allow_html=True)
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index, busy_month.values, color='orange')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                # Add horizontal rule for separation
                st.markdown("<hr class='hr'>", unsafe_allow_html=True)

                # Wordcloud
                st.markdown("<p class='css-1rx1e5e'>Wordcloud</p>", unsafe_allow_html=True)
                df_wc = helper.create_wordcloud(selected_user, df)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)

                # Add horizontal rule for separation
                st.markdown("<hr class='hr'>", unsafe_allow_html=True)

            else:
                st.warning("Please click the 'Show Analysis' button.")
        else:
            st.warning("Please select a user for analysis.")
    else:
        st.warning("Error during data preprocessing. Please check your input file.")
