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

# Here we build our Markov Chain, pretty cool stuff
# how this works is we take a list of words and a context size k
# and we create a dictionary where each key is a k-word context
# and the value is a list of the next words that follow that context
# so if we have the context "hello world" and the next word is "foo"
# then we would add "foo" to the list of successors for the key "hello world"
# and we do this for every k-word context in the text

def build_markov_chain(words, k):
    chain = defaultdict(list)
    # defaultdict is a dictionary that automatically initializes the value for a key that doesn't exist 
    # as a list, so we don't have to do that manually. this is important because some contexts will not have any successors
    # we iterate over the words and for each k-word context, we add the next word to the list of successors
    for i in range(len(words) - k):
        context = tuple(words[i:i+k])  # This is our k-word context
        successor = words[i+k]        # And this is the next word
        chain[context].append(successor)
    return chain


# Now we generate some text using our Markov Chain
# we start with a given context and then we keep picking a random successor
# until we have generated the desired length of text
# we keep updating the context to the last k words of the sentence as we generate new words
# this way we can keep track of what we've said before and use that to generate the next word
def generate_text(chain, start_context, length):
    # we start with the first k words of the sentence
    sentence = list(start_context)
    # we also keep track of the current context, which is the last k words of the sentence
    current_context = start_context
    
    # we keep generating words until we have the desired length
    for _ in range(length - len(start_context)):
        successors = chain.get(current_context, [])
        if not successors:
            # If we hit a dead end, let's just pick a random context to keep going
            current_context = random.choice(list(chain.keys()))
            continue
        next_word = random.choice(successors)  # Pick a successor, you know, randomly
        sentence.append(next_word) # add the next word to the sentence
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
