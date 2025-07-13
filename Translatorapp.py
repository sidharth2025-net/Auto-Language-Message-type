import streamlit as st
from googletrans import Translator, LANGUAGES
import asyncio 

def main():
    """
    Main function to run the Streamlit Translator App.
    """
    st.set_page_config(page_title="Online Translator App", page_icon="🌍") 
    st.title("🌐 Translator App with Streamlit") 
    st.markdown("---")
    st.subheader("Enter text to translate:")
    text_input = st.text_area("Type your text here...", height=150, key="text_input_area")

    language_names = sorted(list(LANGUAGES.values()))
    language_code_map = {name: code for code, name in LANGUAGES.items()}

    col1, col2 = st.columns(2)

    with col1:
        src_lang_name = st.selectbox(
            "Select Source Language:",
            language_names,
            index=language_names.index('english'), 
            key="src_lang_select"
        )
    with col2:
        dest_lang_name = st.selectbox(
            "Select Target Language:",
            language_names,
            index=language_names.index('hindi'),
            key="dest_lang_select"
        )

    src_lang_code = language_code_map.get(src_lang_name)
    dest_lang_code = language_code_map.get(dest_lang_name)

    st.markdown("---")

    if st.button("Translate", key="translate_button", help="Click to translate the text"):
        if not text_input.strip(): 
            st.warning("⚠️ Please enter text to translate.")
        else:
            try:
                translator = Translator()
                with st.spinner("Translating..."):
                    try:
                        
                        if src_lang_code is None or dest_lang_code is None:
                            st.error("❌ Invalid language selection. Please choose valid languages.")
                            return

                        result = asyncio.run(translator.translate(text_input, src=src_lang_code, dest=dest_lang_code))
                    except RuntimeError as re:
                        st.error(f"❌ Translation failed due to a runtime error: {re}.")
                        st.warning("This often happens if an asyncio event loop is already running (e.g., by Streamlit).")
                        st.info("Consider restarting the app or checking your `googletrans` version. Using `googletrans==4.0.0-rc1` is often recommended to avoid such issues.")
                        return

              
                st.success("✅ Translated Text:")
                st.write(f"**{result.text}**")
                st.info(f"Detected Source Language: **{LANGUAGES.get(result.src, 'Unknown').capitalize()}**")

            except Exception as e:
                st.error(f"❌ An unexpected error occurred during translation: {e}")
                st.info("Please ensure your internet connection is stable and try again.")
                st.info("Note: The `googletrans` library relies on Google Translate's unofficial API, which can sometimes be unstable.")

if __name__ == "__main__":
    main() 
