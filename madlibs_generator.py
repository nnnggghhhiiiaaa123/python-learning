with open("story.txt", "r") as f:
    story = f.read()

words = set()
start_of_word = -1

target_start = "<"
target_end = ">"

# Find placeholders like <noun>, <verb>, etc.
for i, char in enumerate(story):
    if char == target_start:
        start_of_word = i
    elif char == target_end and start_of_word != -1:
        word = story[start_of_word: i + 1]
        words.add(word)   # FIXED
        start_of_word = -1

answers = {}

# Ask user to fill in placeholders
for word in words:
    answer = input(f"Enter a word for {word}: ")
    answers[word] = answer

# Replace placeholders with answers
for word in words:
    story = story.replace(word, answers[word])  # FIXED

print("\nHere’s your story:\n")
print(story)
