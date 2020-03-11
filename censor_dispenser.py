# These are the emails you will be censoring. The open() function is opening the text file that the emails are
# contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithms", "her", "herself"]
negative_words = ["concerned", "behind", "danger", "dangerous", "danger", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressed", "concerning", "horrible", "horribly", "questionable"]
punctuation = [".", ",", "?", "!", ":", ";"]

censored = "*"


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


def prepare_punctuation(censor, word, length):
    censored_word = ""
    for punct in punctuation:
        if punct == word[-1:]:
            word_without_punct = word[:-1]
            if censor == word_without_punct:
                censored_word = (censored * (length - 1)) + punct
                break
        else:
            if censor == word:
                censored_word = censored * length
    return censored_word


def compare_words(censor, word, lengths):
    censored_words = []
    if censor in word.lower():
        for length in lengths:
            censored_word = prepare_punctuation(censor, word.lower(), length)
            if censored_word != "":
                censored_words.append(censored_word)
    return censored_words


def censor_negatives(negatives, proprietaries, text):
    pre_censored_text = censor(proprietaries, text, "simple")
    new_text = pre_censored_text
    for word in negatives:
        if pre_censored_text.count(word) >= 2:
            new_text = pre_censored_text.replace(word, censored * len(word))
            pre_censored_text = new_text
    return new_text


def censor(list_of_words_to_censor, text, method):
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

                censored_words = compare_words(word_to_censor, formated_word, word_lengths)
                if censored_words:
                    if method == "simple" or method == "full":
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


#print(email_one)
print(censor(["learning algorithms"], email_one, "simple"))

#print(email_two)
print(censor(proprietary_terms, email_two, "simple"))

#print(email_three)
#print(censor_negatives(negative_words, proprietary_terms, email_three))

#print(email_four)
print(censor(negative_words + proprietary_terms, email_four, "full"))
