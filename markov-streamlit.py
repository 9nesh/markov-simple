import streamlit as st
from collections import defaultdict, Counter
import random
import string
import pandas as pd
import time
import matplotlib.pyplot as plt


# This function cleans up the text a bit
def preprocess_text(text, remove_punctuation=True, convert_lowercase=True):
    if remove_punctuation:
        text = text.translate(str.maketrans('', '', string.punctuation))
    if convert_lowercase:
        text = text.lower()
    return text.replace('\n', ' ').split()

# Here we build our Markov Chain, pretty cool stuff
def build_markov_chain(words, k):
    chain = defaultdict(list)
    for i in range(len(words) - k):
        context = tuple(words[i:i+k])  # This is our k-word context
        successor = words[i+k]        # And this is the next word
        chain[context].append(successor)
    return chain

# Now we generate some text using our Markov Chain
def generate_text(chain, start_context, length):
    sentence = list(start_context)
    current_context = start_context
    
    for _ in range(length - len(start_context)):
        successors = chain.get(current_context, [])
        if not successors:
            # If we hit a dead end, let's just pick a random context to keep going
            current_context = random.choice(list(chain.keys()))
            continue
        next_word = random.choice(successors)  # Pick a successor, you know, randomly
        sentence.append(next_word)
        current_context = tuple(sentence[-len(current_context):])  # Update the context
    
    return " ".join(sentence)

# Here comes the main part of our Streamlit app
def main():
    st.title("Enhanced Markov Chain Text Generator")
    
    # A little help section on the sidebar
    st.sidebar.title("Help")
    st.sidebar.info("""
    - **Context Size (k):** How many words we use to predict the next one.
    - **Number of Words:** Total words we want to generate.
    - **Starting Context:** You can give some starting words if you want.
    - **Random Seed:** Set a seed for making randomness repeatable.
    """)

    # Time to upload a file
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    
    if uploaded_file:
        # Load and clean up the text
        text = uploaded_file.read().decode("utf-8")
        remove_punctuation = st.checkbox("Remove punctuation?", value=True)
        convert_lowercase = st.checkbox("Convert text to lowercase?", value=True)
        words = preprocess_text(text, remove_punctuation, convert_lowercase)
        
        st.write("### Uploaded Text Sample")
        st.text(" ".join(words[:100]))  # Just show a little bit of the text
        
        # Some debugging info for us
        st.write("### Debug Info")
        st.write(f"Total words in text: {len(words)}")

        # Let's visualize how often words show up
        if st.checkbox("Show word frequency chart?"):
            word_counts = Counter(words)
            freq_df = pd.DataFrame(word_counts.items(), columns=["Word", "Count"]).sort_values(by="Count", ascending=False).head(20)
            fig, ax = plt.subplots()
            freq_df.set_index("Word").plot(kind="bar", ax=ax)
            st.pyplot(fig)

        # Get the context size (k) from the user
        k = st.number_input("Enter the context size (k):", min_value=1, max_value=50, value=3, step=1)

        # Check if the text is long enough for the context size
        if len(words) <= k:
            st.error(f"The text is too short for context size k={k}. Try reducing k or uploading a larger text file.")
            return
        
        # Ask how many words to generate
        num_words = st.number_input("Enter the number of words to generate:", min_value=1, max_value=500, value=100, step=10)
        
        # Set a random seed if the user wants
        seed = st.slider("Set random seed (0 for random):", min_value=0, max_value=1000, value=0)
        if seed != 0:
            random.seed(seed)
        
        # Let the user choose a starting context
        if st.checkbox("Choose a starting context?"):
            start_context_input = st.text_input(f"Enter {k} starting words (separate by spaces):")
            start_context = tuple(start_context_input.lower().split()[:k])
            if len(start_context) < k:
                st.error(f"The starting context must contain at least {k} words.")
                return
        else:
            start_index = random.randint(0, len(words) - k)
            start_context = tuple(words[start_index:start_index + k])
        
        # Decide if we want to generate text word by word or all at once
        if st.checkbox("Generate text dynamically (word by word)?"):
            if st.button("Generate Text Dynamically"):
                markov_chain = build_markov_chain(words, k)
                generated_text = generate_text(markov_chain, start_context, num_words)
                
                # Use a placeholder to show the text as we generate it
                placeholder = st.empty()
                current_text = ""  # Keep track of the text as we go
                for word in generated_text.split():
                    current_text += word + " "  # Add the new word to what we have
                    placeholder.text(current_text.strip())  # Update the display
                    time.sleep(0.1)  # A little delay for effect

        else:
            if st.button("Generate Text"):
                # Build the Markov Chain
                markov_chain = build_markov_chain(words, k)
                
                # Generate the text
                generated_text = generate_text(markov_chain, start_context, num_words)
                
                if len(generated_text.split()) < num_words:
                    st.warning("Not enough data to generate the requested number of words. Try reducing k or increasing text size.")
                
                st.write("### Generated Text")
                st.markdown(f"**{generated_text}**")
                
                # Option to download the generated text
                st.download_button("Download Generated Text", generated_text, "generated_text.txt", "text/plain")

if __name__ == "__main__":
    main()
