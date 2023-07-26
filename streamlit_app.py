import streamlit as st

# Define the layout of the data analysis page
def data_analysis_page():
    st.title('Data Analysis Page')
    st.write('This is the data analysis page of my app.')
    # Add your data analysis and visualization code here

# Define the layout of the chat bot page
def chat_bot_page():
    st.title('Chat Bot Page')
    st.write('This is the chat bot page of my app.')
    # Add your chat bot code here
    if st.button('Go back to Data Analysis'):
        st.session_state.page = 'Data Analysis'

# Define your main function
def main():
    # Define the state of your app
    if 'page' not in st.session_state:
        st.session_state.page = 'Data Analysis'

    # Define the contents of the sidebar
    st.sidebar.title('Navigation')
    option = st.sidebar.selectbox('Select an option', ('Data Analysis', 'Chat Bot'))

    # Define the different pages of your app
    if option == 'Data Analysis':
        st.session_state.page = 'Data Analysis'
        data_analysis_page()
    elif option == 'Chat Bot':
        st.session_state.page = 'Chat Bot'
        chat_bot_page()

# Call your main function to run the app
if __name__ == '__main__':
    main()
