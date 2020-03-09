# These are the emails you will be censoring. The open() function is opening the text file that the emails are contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithms", "her", "herself"]
negative_words = ["concerned", "behind", "danger", "dangerous", "danger", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressed", "concerning", "horrible", "horribly", "questionable"]
punctuation = ["", ".", ",", "?", "!", ":", ";", "'s"]

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

def compare_words(word_to_censor, word_in_text):
    for punct in punctuation:
        if word_to_censor in word_in_text:
            test_word = word_to_censor + punct
            if test_word == word_in_text.lower():
                return True, punct
    return False, punct

def censor_negatives(negatives, proprietaries, text):
    pre_censored_text = censor_many_words(proprietaries, text)
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
                if " " in word_to_censor and (word_number + 1) < len(text_list[line_number]):
                    need_to_censor, punct = compare_words(word_to_censor, text_list[line_number][word_number] + " " + text_list[line_number][word_number + 1])
                    two_words = True
                else:
                    need_to_censor, punct = compare_words(word_to_censor, text_list[line_number][word_number])
                    two_words = False
                if need_to_censor:
                    if method == "full":
                        text_list[line_number][word_number - 1] = censored * len(text_list[line_number][word_number - 1])
                        if punct == "'s" or punct == "'d":
                            text_list[line_number][word_number] = censored * len(text_list[line_number][word_number])
                        else:
                            text_list[line_number][word_number] = censored * (len(text_list[line_number][word_number]) - len(punct)) + punct
                        try:
                            text_list[line_number][word_number + 1] = censored * len(text_list[line_number][word_number + 1])
                        except:
                            pass
                    elif method == "simple":
                        if punct == "'s" or punct == "'d":
                            text_list[line_number][word_number] = censored * len(text_list[line_number][word_number])
                            if two_words:
                                text_list[line_number][word_number + 1] = censored * len(
                                    text_list[line_number][word_number + 1])
                        else:
                            if two_words:
                                text_list[line_number][word_number] = censored * len(text_list[line_number][word_number])
                                text_list[line_number][word_number + 1] = censored * (len(
                                    text_list[line_number][word_number + 1]) - len(punct)) + punct
                            else:
                                text_list[line_number][word_number] = censored * (len(text_list[line_number][word_number]) - len(punct)) + punct
    return reformat_text(text_list)

#print(email_one)
#print(censor(["learning algorithms"], email_one, "simple"))

#print(email_two)
#print(censor(proprietary_terms, email_two, "simple"))

#print(email_three)
#print(censor_negatives(negative_words, proprietary_terms, email_three))

#print(email_four)
#print(censor(negative_words + proprietary_terms, email_four, "full"))
