import streamlit as st
import os
from PIL import Image
import importlib
from dotenv import load_dotenv

# Import application modules
from modules.auth import login, signup
from modules.artist import profile, management
from modules.music import upload, player, discovery
from modules.payments import crypto
from modules.ui import components, styles, pages

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="BeatDrop - Independent Artist Platform",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize application state
def initialize_session_state():
    """Initialize session state variables"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'is_artist' not in st.session_state:
        st.session_state.is_artist = False
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'

# Apply custom styling
def apply_styling():
    """Apply custom styling to the application"""
    # Get custom CSS based on dark/light mode
    custom_css = styles.get_css(dark_mode=st.session_state.dark_mode)
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Apply custom font and icon imports
    st.markdown(styles.get_font_imports(), unsafe_allow_html=True)

# Navigation component
def render_navigation():
    """Render the main navigation bar"""
    return components.navigation_bar(
        is_logged_in=st.session_state.user_id is not None,
        is_artist=st.session_state.is_artist,
    )

# Main application router
def route_to_page():
    """Route to the appropriate page based on session state"""
    current_page = st.session_state.current_page
    
    # Authentication pages
    if current_page == 'login':
        login.render_login_page()
    elif current_page == 'signup':
        signup.render_signup_page()
    
    # Home/discovery pages
    elif current_page == 'home':
        pages.render_home_page()
    elif current_page == 'discover':
        discovery.render_discovery_page()
    elif current_page == 'trending':
        discovery.render_trending_page()
    elif current_page == 'playlists':
        discovery.render_playlists_page()
    
    # Artist pages
    elif current_page == 'artist_profile':
        profile.render_artist_profile(st.session_state.profile_user_id)
    elif current_page == 'my_profile':
        profile.render_artist_profile(st.session_state.user_id)
    elif current_page == 'edit_profile':
        management.render_edit_profile_page()
    
    # Music management
    elif current_page == 'upload':
        upload.render_upload_page()
    elif current_page == 'my_music':
        management.render_my_music_page()
    
    # Payment pages
    elif current_page == 'payments':
        crypto.render_payment_page()
    
    # Default - render 404 page
    else:
        pages.render_404_page()

# Main application
def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Apply custom styling
    apply_styling()
    
    # Render sidebar
    with st.sidebar:
        components.render_sidebar()
    
    # Render top navigation
    nav_col1, nav_col2 = st.columns([3, 7])
    with nav_col1:
        components.render_logo()
    with nav_col2:
        render_navigation()
    
    # Render current music player if track is playing
    if 'current_track' in st.session_state and st.session_state.current_track:
        player.render_persistent_player()
    
    # Main content area - route to appropriate page
    with st.container():
        route_to_page()
    
    # Render footer
    components.render_footer()

if __name__ == "__main__":
    main()
