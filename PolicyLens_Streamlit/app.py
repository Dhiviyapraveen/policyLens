import streamlit as st
from utils.prompt import build_prompt
from utils.llm_client import explain_text
from PyPDF2 import PdfReader
from fpdf import FPDF
import io
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title='PolicyLens', layout='wide')
st.markdown('<h1 style="color:#4B5563">PolicyLens</h1>', unsafe_allow_html=True)
st.sidebar.header('Settings')

# Sidebar controls
tone = st.sidebar.selectbox('Tone', ['Professional', 'Simple', 'Kid-Friendly'])
length = st.sidebar.selectbox('Output Length', ['Short', 'Medium', 'Detailed'])
highlight = st.sidebar.checkbox('Highlight key clauses', value=True)
upload = st.sidebar.file_uploader('Upload PDF or TXT', type=['pdf','txt'])
st.sidebar.markdown('---')
st.sidebar.write('Tip: Set GEMINI_API_KEY to enable remote LLM calls.')

# Main UI
col1, col2 = st.columns([2,1])
with col1:
    st.subheader('Policy input')
    policy_text = st.text_area('Paste policy text here or upload a file', height=300)
    if upload is not None and upload.type == 'application/pdf':
        try:
            reader = PdfReader(upload)
            pages = [p.extract_text() or '' for p in reader.pages]
            policy_text = '\n'.join(pages)
            st.success('PDF loaded — text extracted.')
        except Exception as e:
            st.error('Could not read PDF: ' + str(e))
    elif upload is not None and upload.type.startswith('text'):
        try:
            policy_text = upload.read().decode('utf-8')
            st.success('Text file loaded.')
        except Exception as e:
            st.error('Could not read file: ' + str(e))

    if st.button('Explain policy'):
        if not policy_text.strip():
            st.warning('Please paste or upload policy text.')
        else:
            with st.spinner('Generating explanation...'):
                prompt = build_prompt(policy_text, tone, length)
                result = explain_text(prompt)
                st.session_state['last_result'] = result
                st.session_state['last_policy'] = policy_text
                st.success('Explanation generated. Scroll right to see results.')

with col2:
    st.subheader('Actions')
    if 'last_result' in st.session_state:
        if st.button('Download Explanation as TXT'):
            b = st.session_state['last_result'].encode('utf-8')
            st.download_button('Download TXT', data=b, file_name='explanation.txt', mime='text/plain')
        if st.button('Export as PDF'):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, 'PolicyLens Explanation', ln=True)
            pdf.set_font('Arial', '', 11)
            text = st.session_state['last_result']
            # split into chunks
            for line in text.split('\n'):
                pdf.multi_cell(0, 6, line)
            pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
            st.download_button('Download PDF', data=pdf_out, file_name='explanation.pdf', mime='application/pdf')

# Results area (full width)
st.markdown('---')
st.subheader('Explanation Output')
if 'last_result' in st.session_state:
    st.markdown('**Summary / Explanation**')
    st.write(st.session_state['last_result'])
else:
    st.info('No explanation yet. Paste a policy and click "Explain policy".')
