import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Page configuration
st.set_page_config(
    page_title="Text Summarization App",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with baby pink premium theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #ffeef8 0%, #fff0f5 50%, #ffeef8 100%);
    }
    
    /* Header styling */
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: -0.01em;
        color: #d63384;
        text-shadow: 2px 2px 4px rgba(214, 51, 132, 0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #c2185b;
        font-size: 1.15rem;
        margin-bottom: 3rem;
        font-weight: 300;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
    }
    
    /* Summary text area - no box, clean display */
    .summary-text {
        background: transparent;
        padding: 1.5rem 0;
        line-height: 2;
        font-size: 1.1rem;
        color: #2d1b3d;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
    }
    
    /* Stats boxes with premium pink theme */
    .stats-box {
        background: linear-gradient(135deg, #fff5f9 0%, #ffeef8 100%);
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(214, 51, 132, 0.08);
        border: 1px solid rgba(214, 51, 132, 0.15);
    }
    
    /* Input section */
    .input-section {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(214, 51, 132, 0.12);
        border: 1px solid rgba(214, 51, 132, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Premium button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff6b9d 0%, #d63384 100%);
        color: white;
        font-weight: 600;
        font-size: 1.15rem;
        padding: 1rem 2.5rem;
        border-radius: 12px;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(214, 51, 132, 0.25);
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(214, 51, 132, 0.35);
        background: linear-gradient(135deg, #ff7ba8 0%, #e6399f 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #fff5f9 0%, #ffeef8 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff5f9 0%, #ffeef8 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    /* Headers */
    h2, h3 {
        color: #d63384;
        font-weight: 600;
        font-family: 'Playfair Display', serif;
    }
    
    /* Text area styling */
    .stTextArea>div>div>textarea {
        border-radius: 12px;
        border: 2px solid rgba(214, 51, 132, 0.2);
        background: rgba(255, 255, 255, 0.95);
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #d63384;
        box-shadow: 0 0 0 4px rgba(214, 51, 132, 0.1);
        outline: none;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #d63384;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        color: #c2185b;
        font-weight: 500;
    }
    
    /* Slider styling */
    .stSlider>div>div>div {
        background: linear-gradient(90deg, #ff6b9d 0%, #d63384 100%);
    }
    
    .stSlider>div>div>div>div {
        background: #d63384;
    }
    
    /* Radio button styling */
    .stRadio>div>label {
        color: #2d1b3d;
        font-weight: 500;
    }
    
    /* Info box */
    .stInfo {
        background: linear-gradient(135deg, #fff5f9 0%, #ffeef8 100%);
        border-left: 4px solid #d63384;
        border-radius: 8px;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #fff5f9 0%, #ffeef8 100%);
        color: #d63384;
        border: 2px solid #d63384;
        font-weight: 600;
    }
    
    .stDownloadButton>button:hover {
        background: #d63384;
        color: white;
    }
    
    /* Progress bar */
    .stProgress>div>div>div {
        background: linear-gradient(90deg, #ff6b9d 0%, #d63384 100%);
    }
    
    /* Remove default Streamlit elements styling */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* File uploader */
    .stFileUploader>div>div>div {
        border: 2px dashed rgba(214, 51, 132, 0.3);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.5);
    }
    
    .stFileUploader>div>div>div:hover {
        border-color: #d63384;
        background: rgba(255, 255, 255, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_stopwords():
    """Cache stopwords for faster access"""
    return set(stopwords.words('english'))

@st.cache_data
def extractive_summarize(text, num_sentences=3):
    """
    Highly optimized extractive summarization using sentence scoring
    """
    # Early return for short texts
    if not text or not text.strip():
        return ""
    
    # Clean and tokenize text
    sentences = sent_tokenize(text)
    
    if len(sentences) <= num_sentences:
        return text
    
    # Get cached stopwords
    stop_words = get_stopwords()
    
    # Pre-process words once - optimized
    text_lower = text.lower()
    words = word_tokenize(text_lower)
    words = [word for word in words if word.isalnum() and word not in stop_words and len(word) > 1]
    
    if not words:
        return text
    
    # Calculate word frequencies efficiently
    word_freq = Counter(words)
    max_freq = max(word_freq.values())
    
    # Normalize frequencies in one pass
    word_freq_normalized = {word: freq / max_freq for word, freq in word_freq.items()}
    
    # Score sentences efficiently with pre-tokenized words
    sentence_scores = []
    for idx, sentence in enumerate(sentences):
        sentence_lower = sentence.lower()
        sentence_words = [w for w in word_tokenize(sentence_lower) 
                         if w.isalnum() and w not in stop_words and len(w) > 1]
        if sentence_words:
            score = sum(word_freq_normalized.get(word, 0) for word in sentence_words)
            # Normalize by sentence length to avoid bias toward long sentences
            score = score / len(sentence_words) if sentence_words else 0
            sentence_scores.append((idx, sentence, score))
    
    if not sentence_scores:
        return text
    
    # Get top sentences and maintain original order
    top_sentences = sorted(sentence_scores, key=lambda x: x[2], reverse=True)[:num_sentences]
    top_sentences = sorted(top_sentences, key=lambda x: x[0])
    
    return ' '.join([sent for _, sent, _ in top_sentences])

@st.cache_data
def calculate_stats(text):
    """Calculate text statistics - cached for performance"""
    if not text:
        return {
            'characters': 0,
            'words': 0,
            'sentences': 0,
            'paragraphs': 0
        }
    
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    
    return {
        'characters': len(text),
        'characters_no_spaces': len(text.replace(' ', '')),
        'words': len([w for w in words if w.isalnum()]),
        'sentences': len(sentences),
        'paragraphs': len(paragraphs) if paragraphs else 1
    }

def main():
    st.markdown('<h1 class="main-header">Text Summarization</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Transform long texts into concise, meaningful summaries</p>', unsafe_allow_html=True)
    
    # Sidebar for settings
    with st.sidebar:
        st.markdown("### Settings")
        st.markdown("---")
        
        num_sentences = st.slider(
            "Number of sentences in summary",
            min_value=1,
            max_value=10,
            value=3,
            help="Select how many sentences to include in the summary"
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        This app uses extractive summarization to identify and select the most important sentences from your text.
        
        **Features:**
        - Fast and efficient processing
        - Preserves original wording
        - Maintains sentence order
        - Works with any text length
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("### Input Text")
        input_method = st.radio(
            "Input method",
            ["Type/Paste Text", "Upload File"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        text_input = ""
        
        if input_method == "Type/Paste Text":
            text_input = st.text_area(
                "Enter or paste your text here:",
                height=450,
                placeholder="Type or paste your text here...",
                help="Enter the text you want to summarize",
                label_visibility="visible"
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload a text file",
                type=['txt', 'md'],
                help="Upload a .txt or .md file"
            )
            if uploaded_file is not None:
                text_input = uploaded_file.read().decode('utf-8')
                st.text_area("File content:", text_input, height=350, key="file_content")
        
        if text_input:
            original_stats = calculate_stats(text_input)
            st.markdown('<div class="stats-box">', unsafe_allow_html=True)
            st.markdown("**Original Text Statistics**")
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Characters", f"{original_stats['characters']:,}")
            with col_stat2:
                st.metric("Words", f"{original_stats['words']:,}")
            with col_stat3:
                st.metric("Sentences", f"{original_stats['sentences']:,}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("Generate Summary", type="primary", use_container_width=True):
            if not text_input.strip():
                st.error("Please enter some text to summarize!")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("Processing your text...")
                    progress_bar.progress(30)
                    
                    status_text.text("Analyzing sentences...")
                    progress_bar.progress(60)
                    
                    summary = extractive_summarize(text_input, num_sentences=num_sentences)
                    
                    progress_bar.progress(100)
                    status_text.text("Complete!")
                    
                    # Display summary without box/header
                    st.markdown('<div class="summary-text">', unsafe_allow_html=True)
                    st.markdown(summary)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Summary statistics
                    summary_stats = calculate_stats(summary)
                    compression_ratio = (1 - summary_stats['words'] / original_stats['words']) * 100 if original_stats['words'] > 0 else 0
                    
                    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                    st.markdown("**Summary Statistics**")
                    
                    col_sum1, col_sum2, col_sum3 = st.columns(3)
                    with col_sum1:
                        st.metric("Characters", f"{summary_stats['characters']:,}")
                    with col_sum2:
                        st.metric("Words", f"{summary_stats['words']:,}")
                    with col_sum3:
                        st.metric("Sentences", f"{summary_stats['sentences']:,}")
                    
                    st.metric("Compression Ratio", f"{compression_ratio:.1f}% reduction")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download button
                    st.download_button(
                        label="Download Summary",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Please check your input text and try again.")
        else:
            st.info("Enter text in the left panel and click 'Generate Summary' to get started!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #c2185b; padding: 2rem; font-family: Inter, sans-serif; font-weight: 300;'>"
        "Built with Python and Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
