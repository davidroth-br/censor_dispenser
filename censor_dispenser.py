# These are the emails you will be censoring. The open() function is opening the text file that the emails are
# contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithms", "her",
                     "herself"]
negative_words = ["concerned", "behind", "danger", "dangerous", "danger", "alarming", "alarmed", "out of control",
                  "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed",
                  "distressed", "concerning", "horrible", "horribly", "questionable"]
punctuation = [".", ",", "?", "!", ":", ";", "(", ")"]
censored = "*"
double_words = []


def prepare_text(text):
    broken_down_text = []
    split_lines = text.split("\n")
    for line in split_lines:
        broken_down_text.append(line.split())
    return broken_down_text


def reformat_text(prepared_text):
    lines = []
    for line in prepared_text:
        lines.append(" ".join(line))
    return "\n".join(lines)


def prepare_punctuation(censor_this, word, length):
    censored_word = ""
    for punct in punctuation:
        if punct in word:
            word_without_punct = word.strip(punct)
            if censor_this == word_without_punct:
                if punct != "(":
                    censored_word = (censored * (length - 1)) + punct
                else:
                    censored_word = punct + (censored * (length - 1))
                break
        else:
            if censor_this == word:
                censored_word = censored * length
    return censored_word


def compare_words(censor_this, word, lengths, method, text):
    censored_words = []
    compare_word = word.lower()
    if censor_this in compare_word:
        if method == "double":
            for punct in punctuation:
                compare_word = compare_word.strip(punct)
            number_of_occurences = text.count(compare_word) + text.count(compare_word.upper()) + text.count(compare_word.title())
            if compare_word in negative_words:
                if number_of_occurences < 2 and compare_word not in double_words:
                    return censored_words
                else:
                    if compare_word not in double_words:
                        double_words.append(compare_word)
        ind = 0
        for length in lengths:
            ind += 1
            if ind == len(lengths):
                censored_word = prepare_punctuation(censor_this, word.lower(), length)
            else:
                censored_word = prepare_punctuation(censor_this, compare_word, length)
            if censored_word != "":
                censored_words.append(censored_word)
        return censored_words


def censor(list_of_words_to_censor, text, method):
    if method != "simple" and method != "double" and method != "full":
        return "Method must be 'simple', 'double' or 'full'"
    text_list = prepare_text(text)
    for line_number in range(len(text_list)):
        for word_number in range(len(text_list[line_number])):
            for word_to_censor in list_of_words_to_censor:
                number_of_words = len(word_to_censor.split())

                word_to_check = ""
                word_lengths = []
                for i in range(number_of_words):
                    try:
                        word_to_check += text_list[line_number][word_number + i] + " "
                        word_lengths.append(len(text_list[line_number][word_number + i]))
                    except:
                        break
                formated_word = word_to_check.strip()

                censored_words = compare_words(word_to_censor, formated_word, word_lengths, method, text)
                if censored_words:
                    for i in range(len(censored_words)):
                        text_list[line_number][word_number + i] = censored_words[i]
                        last_index = i
                    if method == "full":
                        word_before = word_number - 1
                        word_after = word_number + last_index + 1
                        text_list[line_number][word_before] = prepare_punctuation(text_list[line_number][word_before], text_list[line_number][word_before], len(text_list[line_number][word_before]))
                        try:
                            text_list[line_number][word_after] = prepare_punctuation(text_list[line_number][word_after], text_list[line_number][word_after], len(text_list[line_number][word_after]))
                        except:
                            pass
    return reformat_text(text_list)


print(censor(["learning algorithms"], email_one, "simple"))

print(censor(proprietary_terms, email_two, "simple"))

print(censor(negative_words + proprietary_terms, email_three, "double"))

print(censor(negative_words + proprietary_terms, email_four, "full"))
