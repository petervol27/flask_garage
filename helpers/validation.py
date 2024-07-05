def capitalize_desc(car_desc):
    split_desc = car_desc.split()
    capitalized_words = []
    for word in split_desc:
        capitalized_words.append(word.capitalize())
    return " ".join(capitalized_words)
