import streamlit as st
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server

# Define a function to get the current session state
def get_session():
    session = get_report_ctx().session
    session_id = session.id
    session_info = Server.get_current()._session_info_by_id.get(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get session info")
    return session, session_id, session_info

# Define your main function
def main():
    session, session_id, session_info = get_session()

    # Define the state of your app
    if 'page' not in session.state:
        session.state.page = 'Data Analysis'

    # Define the different pages of your app
    if session.state.page == 'Data Analysis':
        # Define the contents of the data analysis page
        st.sidebar.title('Navigation')
        option = st.sidebar.selectbox('Select an option', ('Data Analysis', 'Chat Bot'))

        if option == 'Data Analysis':
            st.title('Data Analysis Page')
            st.write('This is the data analysis page of my app.')
            # Add your data analysis and visualization code here
        elif option == 'Chat Bot':
            session.state.page = 'Chat Bot'

    elif session.state.page == 'Chat Bot':
        # Define the contents of the chat bot page
        st.title('Chat Bot Page')
        st.write('This is the chat bot page of my app.')
        # Add your chat bot code here
        st.button('Go back to Data Analysis')
        if st.button('Go back to Data Analysis'):
            session.state.page = 'Data Analysis'

# Call your main function to run the app
if __name__ == '__main__':
    main()
