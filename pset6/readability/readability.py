from cs50 import get_string
import re


def main():
    # Prompts user for text
    text = get_string("Text: ")

    # Compute num of letters, words and sentences
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Avg num of letter per 100 words rounded to 2 decimal places
    letter_avg = round(float(letters) / words * 10000, 2) / 100

    # Avg num of sentences per 100 words rounded to 2 decimal places
    sentence_avg = round(float(sentences) / words * 10000, 2) / 100

    # Compute the Coleman-Liau index
    index = round(0.0588 * letter_avg - 0.296 * sentence_avg - 15.8)

    # Checks before Grade 1 condition
    if index < 1:
        print("Before Grade 1")
    # Checks Grade 16+ condition
    elif index >= 16:
        print("Grade 16+")
    # If all special cond. fails, print Grade X
    else:
        print(f"Grade {index}")


def count_letters(text):
    # Initiliaze num of letter
    letters = 0

    # Loop through each char
    for c in text:
        if c.isalpha() == True:
            letters += 1

    return letters


def count_words(text):
    # Initialize num of words
    words = 0

    # Loop through each word
    for word in text.split():
        words += 1

    return words


def count_sentences(text):
    # Initialize num of sentences
    sentences = 0

    # Define regex wanted
    regex = r'([A-z])[^.?!]*'

    # Loop through each sentence as predefined by regex
    for sentence in re.findall(regex, text):
        sentences += 1

    return sentences


# Run main
if __name__ == "__main__":
    main()