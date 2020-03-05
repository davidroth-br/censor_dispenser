# These are the emails you will be censoring. The open() function is opening the text file that the emails are contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithms", "herself", " her"]
negative_words = ["concerned", "behind", "dangerous", "danger", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressed", "concerning", "horrible", "horribly", "questionable"]

def censor_one_word(to_censor, text):
    return text.replace(to_censor, "(*)")

def censor_many_words(to_censor, text):
    for word in to_censor:
        new_text = text.replace(word, "(*)")
        text = new_text
    return new_text

def censor_negatives(negatives, proprietaries, text):
    pre_censored_text = censor_many_words(proprietaries, text)
    new_text = pre_censored_text
    for word in negatives:
        if pre_censored_text.count(word) >= 2:
            new_text = pre_censored_text.replace(word, "(*)")
            pre_censored_text = new_text
    return new_text

def censor_everything(negatives, proprietaries, text):
    

email_one_censored = censor_one_word("learning algorithms", email_one)
print(email_one_censored)

email_two_censored = censor_many_words(proprietary_terms, email_two)
print(email_two_censored)

email_three_censored = censor_negatives(negative_words, proprietary_terms, email_three)
print(email_three_censored)