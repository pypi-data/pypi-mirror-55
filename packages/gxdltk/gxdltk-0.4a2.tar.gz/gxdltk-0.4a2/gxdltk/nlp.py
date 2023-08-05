import re
def word_extraction(sentence):
    # ignore = ['a', "the", "is"]
    words = re.sub("[^\w]", " ", sentence).split()
    # cleaned_text = [w.lower() for w in words if w not in ignore]
    cleaned_text = [w.lower() for w in words]
    return cleaned_text