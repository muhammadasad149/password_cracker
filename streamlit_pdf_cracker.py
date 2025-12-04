#!/usr/bin/env python3
# streamlit_pdf_cracker.py
# Streamlit web interface for PDF Password Cracker

import streamlit as st
import pikepdf
import time
import io
from datetime import datetime
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="PDF Password Cracker",
    page_icon="🔓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 2px solid #28a745;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 2px solid #17a2b8;
        color: #0c5460;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        color: #856404;
        margin: 1rem 0;
    }
    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cracking_complete' not in st.session_state:
    st.session_state.cracking_complete = False
if 'found_password' not in st.session_state:
    st.session_state.found_password = None
if 'cracking_stats' not in st.session_state:
    st.session_state.cracking_stats = {}

def crack_pdf_password(pdf_file, wordlist_content, max_attempts=10000, progress_callback=None):
    """
    PDF password cracker with progress tracking
    """
    try:
        # Create temporary PDF file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
            tmp_pdf.write(pdf_file.read())
            tmp_pdf_path = tmp_pdf.name
        
        # Parse wordlist
        passwords = [line.strip() for line in wordlist_content.decode('utf-8', errors='ignore').split('\n') if line.strip()]
        
        total = len(passwords)
        if total == 0:
            return None, {"error": "Wordlist is empty"}
        
        attempts = 0
        start_time = time.time()
        
        for idx, password in enumerate(passwords):
            if attempts >= max_attempts:
                break
            
            attempts += 1
            
            # Update progress
            if progress_callback and attempts % 10 == 0:
                elapsed = time.time() - start_time
                rate = attempts / elapsed if elapsed > 0 else 0
                progress_callback(idx, total, attempts, rate)
            
            try:
                with pikepdf.open(tmp_pdf_path, password=password) as pdf:
                    end_time = time.time()
                    elapsed = end_time - start_time
                    
                    stats = {
                        'password': password,
                        'attempts': attempts,
                        'time': elapsed,
                        'speed': attempts / elapsed if elapsed > 0 else 0,
                        'pages': len(pdf.pages),
                        'encrypted': pdf.is_encrypted
                    }
                    
                    # Clean up
                    os.unlink(tmp_pdf_path)
                    return password, stats
                    
            except pikepdf.PasswordError:
                pass
            except Exception as e:
                error_str = str(e).lower()
                if "password" not in error_str and "incorrect password" not in error_str:
                    if attempts % 1000 == 0:
                        st.warning(f"Error at attempt {attempts}: {str(e)[:100]}")
        
        # Clean up
        os.unlink(tmp_pdf_path)
        
        end_time = time.time()
        elapsed = end_time - start_time
        stats = {
            'password': None,
            'attempts': attempts,
            'time': elapsed,
            'speed': attempts / elapsed if elapsed > 0 else 0
        }
        return None, stats
        
    except Exception as e:
        return None, {"error": str(e)}

def create_sample_wordlist():
    """Generate sample wordlist"""
    common_passwords = [
        "password", "123456", "12345678", "1234", "qwerty",
        "12345", "dragon", "baseball", "football", "letmein",
        "monkey", "abc123", "111111", "mustang", "access",
        "shadow", "master", "michael", "superman", "696969",
        "123123", "admin", "welcome", "password123", "123456789",
        "sunshine", "iloveyou", "trustno1", "admin123", "letmein123"
    ]
    
    # Add year patterns
    for year in range(2000, 2026):
        common_passwords.extend([str(year), f"pass{year}", f"admin{year}"])
    
    # Add numeric patterns
    for i in range(10000):
        common_passwords.append(str(i))
    
    # Create variations
    wordlist = []
    for pw in common_passwords:
        wordlist.extend([pw, f"{pw}!", f"{pw}@", f"{pw}#", f"{pw}$", f"{pw}123"])
    
    return "\n".join(wordlist)

def test_pdf_password(pdf_file, password):
    """Test if password works"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
            tmp_pdf.write(pdf_file.read())
            tmp_pdf_path = tmp_pdf.name
        
        with pikepdf.open(tmp_pdf_path, password=password) as pdf:
            result = {
                'success': True,
                'pages': len(pdf.pages),
                'encrypted': pdf.is_encrypted
            }
            os.unlink(tmp_pdf_path)
            return result
    except pikepdf.PasswordError:
        os.unlink(tmp_pdf_path)
        return {'success': False, 'error': 'Invalid password'}
    except Exception as e:
        if os.path.exists(tmp_pdf_path):
            os.unlink(tmp_pdf_path)
        return {'success': False, 'error': str(e)}

# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">🔓 PDF Password Cracker</h1>', unsafe_allow_html=True)
    
    # Warning
    st.markdown("""
    <div class="warning-box">
        <h3>⚠️ Legal Notice</h3>
        <p>This tool is for <strong>educational purposes only</strong>. Only use it on PDFs you own or have permission to access.</p>
        <p>Unauthorized access to protected files may be illegal in your jurisdiction.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("ℹ️ Information")
    st.sidebar.info(f"""
    **Version:** 2.1  
    **pikepdf Version:** {pikepdf.__version__}  
    **Status:** Ready
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Features")
    st.sidebar.markdown("""
    - 🔐 Password cracking
    - 📝 Custom wordlists
    - 🧪 Password testing
    - 📈 Real-time progress
    - 💾 Result download
    """)
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["🔓 Crack Password", "📝 Create Wordlist", "🧪 Test Password"])
    
    # Tab 1: Crack Password
    with tab1:
        st.header("Crack PDF Password")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            pdf_file = st.file_uploader("Upload PDF File", type=['pdf'], key='crack_pdf')
        
        with col2:
            max_attempts = st.number_input(
                "Max Attempts", 
                min_value=100, 
                max_value=1000000, 
                value=10000, 
                step=1000,
                help="Maximum number of passwords to try (0 for unlimited)"
            )
        
        wordlist_file = st.file_uploader("Upload Wordlist", type=['txt'], key='wordlist')
        
        col3, col4 = st.columns(2)
        with col3:
            use_sample = st.checkbox("Use sample wordlist (if no wordlist uploaded)")
        with col4:
            if st.button("ℹ️ About Sample Wordlist"):
                st.info("Sample wordlist contains ~60,000 common passwords including numeric patterns, dates, and common words with variations.")
        
        if st.button("🚀 Start Cracking", type="primary", use_container_width=True):
            if not pdf_file:
                st.error("Please upload a PDF file!")
            elif not wordlist_file and not use_sample:
                st.error("Please upload a wordlist or check 'Use sample wordlist'")
            else:
                # Reset session state
                st.session_state.cracking_complete = False
                st.session_state.found_password = None
                
                # Get wordlist content
                if wordlist_file:
                    wordlist_content = wordlist_file.read()
                else:
                    wordlist_content = create_sample_wordlist().encode('utf-8')
                
                # Progress containers
                progress_bar = st.progress(0)
                status_text = st.empty()
                stats_container = st.empty()
                
                def update_progress(idx, total, attempts, rate):
                    progress = idx / total
                    progress_bar.progress(progress)
                    status_text.text(f"Progress: {idx}/{total} ({progress*100:.1f}%) | Speed: {rate:.1f} passwords/sec")
                
                # Start cracking
                with st.spinner('Cracking password...'):
                    password, stats = crack_pdf_password(
                        pdf_file, 
                        wordlist_content, 
                        max_attempts,
                        update_progress
                    )
                
                st.session_state.cracking_complete = True
                st.session_state.found_password = password
                st.session_state.cracking_stats = stats
                
                # Clear progress
                progress_bar.empty()
                status_text.empty()
        
        # Show results
        if st.session_state.cracking_complete:
            if st.session_state.found_password:
                st.markdown(f"""
                <div class="success-box">
                    <h2>✅ PASSWORD FOUND!</h2>
                    <h3>Password: <code>{st.session_state.found_password}</code></h3>
                </div>
                """, unsafe_allow_html=True)
                
                stats = st.session_state.cracking_stats
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Attempts", stats.get('attempts', 'N/A'))
                col2.metric("Time", f"{stats.get('time', 0):.2f}s")
                col3.metric("Speed", f"{stats.get('speed', 0):.1f}/s")
                col4.metric("Pages", stats.get('pages', 'N/A'))
                
                # Download button
                result_text = f"PDF Password Found\n{'='*50}\nPassword: {st.session_state.found_password}\nAttempts: {stats.get('attempts', 'N/A')}\nTime: {stats.get('time', 0):.2f} seconds\nSpeed: {stats.get('speed', 0):.1f} passwords/sec\nPages: {stats.get('pages', 'N/A')}\n"
                st.download_button(
                    "💾 Download Result",
                    result_text,
                    file_name="password_found.txt",
                    mime="text/plain"
                )
            else:
                st.markdown("""
                <div class="error-box">
                    <h2>❌ PASSWORD NOT FOUND</h2>
                    <p>The password was not found in the provided wordlist.</p>
                </div>
                """, unsafe_allow_html=True)
                
                if 'error' in st.session_state.cracking_stats:
                    st.error(f"Error: {st.session_state.cracking_stats['error']}")
                else:
                    stats = st.session_state.cracking_stats
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Attempts", stats.get('attempts', 'N/A'))
                    col2.metric("Time", f"{stats.get('time', 0):.2f}s")
                    col3.metric("Speed", f"{stats.get('speed', 0):.1f}/s")
                    
                    st.markdown("""
                    <div class="info-box">
                        <h4>💡 Suggestions:</h4>
                        <ul>
                            <li>Use a larger wordlist (like rockyou.txt)</li>
                            <li>Try different password patterns</li>
                            <li>Check if PDF uses owner password instead of user password</li>
                            <li>Some PDFs use strong encryption that can't be brute-forced</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Tab 2: Create Wordlist
    with tab2:
        st.header("Create Custom Wordlist")
        
        st.info("Generate a sample wordlist with common passwords and patterns")
        
        col1, col2 = st.columns(2)
        with col1:
            include_years = st.checkbox("Include years (2000-2025)", value=True)
            include_numeric = st.checkbox("Include numeric patterns (0-9999)", value=True)
        with col2:
            include_variations = st.checkbox("Include variations (!@#$)", value=True)
            include_common = st.checkbox("Include common passwords", value=True)
        
        if st.button("🔨 Generate Wordlist", use_container_width=True):
            with st.spinner("Generating wordlist..."):
                wordlist = create_sample_wordlist()
                
            st.success(f"✅ Wordlist generated with {len(wordlist.split())} passwords")
            
            # Preview
            st.subheader("Preview (first 50 lines)")
            preview = "\n".join(wordlist.split('\n')[:50])
            st.code(preview, language="text")
            
            # Download
            st.download_button(
                "💾 Download Wordlist",
                wordlist,
                file_name="sample_wordlist.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    # Tab 3: Test Password
    with tab3:
        st.header("Test PDF Password")
        
        st.info("Verify if a password works on your PDF")
        
        test_pdf = st.file_uploader("Upload PDF File", type=['pdf'], key='test_pdf')
        test_password = st.text_input("Enter Password to Test", type="password")
        
        if st.button("🧪 Test Password", use_container_width=True):
            if not test_pdf:
                st.error("Please upload a PDF file!")
            elif not test_password:
                st.error("Please enter a password!")
            else:
                with st.spinner("Testing password..."):
                    result = test_pdf_password(test_pdf, test_password)
                
                if result['success']:
                    st.markdown(f"""
                    <div class="success-box">
                        <h3>✅ Password is CORRECT!</h3>
                        <p><strong>Pages:</strong> {result['pages']}</p>
                        <p><strong>Encrypted:</strong> {result['encrypted']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        <h3>❌ Password is INCORRECT</h3>
                        <p>{result.get('error', 'Invalid password')}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Made with ❤️ using Streamlit | For Educational Purposes Only</p>
        <p>pikepdf v{} | Python PDF Processing</p>
    </div>
    """.format(pikepdf.__version__), unsafe_allow_html=True)

if __name__ == "__main__":
    main()