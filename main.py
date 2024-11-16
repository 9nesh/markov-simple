from collections import defaultdict
import random
import string

# Let's load some text from a specified file
def load_text(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: Can't find the file at {file_path}")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

# Now, we need to build a Markov Chain based on k-word contexts
def build_markov_chain(words, k):
    chain = defaultdict(list)
    for i in range(len(words) - k):
        context = tuple(words[i:i+k])  # This is our k-word context
        successor = words[i+k]        # This is the next word that follows
        chain[context].append(successor)
    return chain

# Next, we generate text using the Markov Chain we've built
def generate_text(chain, start_context, length):
    sentence = list(start_context)
    current_context = start_context
    
    for _ in range(length - len(start_context)):
        successors = chain.get(current_context, [])
        if not successors:
            break  # Stop if there are no successors
        next_word = random.choice(successors)  # Randomly pick a successor
        sentence.append(next_word)
        current_context = tuple(sentence[-len(current_context):])  # Update the context
    
    return " ".join(sentence)

# Main execution starts here
if __name__ == "__main__":
    # Specify the path to the text file we want to use
    file_path = "./seinfeld-script.txt"  # Make sure to update this with the correct path
    text = load_text(file_path)
    
    # Preprocess the text: remove newlines, punctuation, and convert to lowercase
    words = text.replace('\n', ' ').translate(str.maketrans('', '', string.punctuation)).lower().split()

    # Ask the user for the context size and the number of words to generate
    k = int(input("Enter the context size (k): "))
    num_words = int(input("Enter the number of words to generate: "))

    if k >= len(words):
        print(f"Error: Context size k={k} is too large for the text provided.")
        exit()

    # Build the Markov Chain from the words
    markov_chain = build_markov_chain(words, k)

    # Select a random starting context for text generation
    start_index = random.randint(0, len(words) - k)
    start_context = tuple(words[start_index:start_index + k])

    # Generate the text based on the Markov Chain
    generated_text = generate_text(markov_chain, start_context, num_words)
    print(generated_text)
