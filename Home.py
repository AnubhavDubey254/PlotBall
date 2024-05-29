import streamlit as st

st.set_page_config(
    page_title="Plotball",
    page_icon="🧩",
)
st.title('HOME')


#Introduction
st.subheader("Introduction")
st.write('''PlotBall is an open source streamlist-based data visualization app that leverages publicly available data from StatsBomb to display various data plots.
         Currently, the app supports Pass and Shot maps, offering users insightful visual representations of this data.
         In the future, I plan to expand its capabilities by adding many more types of data graphs.

Your feedback is crucial for improving PlotBall.
If you encounter any bugs or have suggestions for new features, please don't hesitate to get in touch.
You can reach out anytime through the Contact Us page on the app, or you can visit the GitHub repository to contribute directly to the project.

By collaborating, we can make PlotBall a more powerful and user-friendly tool for data visualization.
Whether you're a data enthusiast or a sports analyst, your input will help shape the future of PlotBall.
Thank you for your support and interest in this project. ''')

st.page_link("pages/1_Data_Plots.py",label = "Check Out Plots",icon = "📊")


