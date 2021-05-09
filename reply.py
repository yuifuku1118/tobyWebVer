import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn

import random

############ if the input is simple and can auto reply ###############################################################################################################################################################

def autoreply(t):
    auto = 0
    res = ""
    sentence = nltk.word_tokenize(t)
    tag = nltk.pos_tag(sentence)
    listi = []
    count = 0
    for i in tag:
        count += 1
        listi.append([i[0],i[1],count])
    greating = ["hi","hello","sup","good morning","good evening","good afternoon"]
    for element in listi:
        if element[2] == 1:
            if element[0] in greating:
                res = "hello"
                auto = 1
            elif  element[1].startswith("WP"):
                res = "I am so sorry I don't know the answer to that "
                auto = 1

    if t == "how are you?":
        res = "I am good thank you and you?"
        auto = 1
    elif t == "no":
        res = "Right, anything you want to talk about?"
    elif t == "yes":
        res = "Right"
    elif (t == "do you like me") or (t == "do you like me ?"):
        res = "Of course I do, why wouldn't I ?"

    return auto, res


######## choses the reply based on the pridiction ####################################################################################################################################################################

def MLreply(y):
    
    reply = ""
    _1_ = ["That’s great! Tell me more about your day!",
            "Good to hear that. Tell me more about it!",
            "Nice! Anything happened to you recently?",
            "Okay nice! Is there anything you want to talk about?",
            "Anything happened in your day?"]
    
    _2_ =  ["That is great! Anything you want to talk about?",
            "That is awesome. Anything you want to talk about?.",
            "Great! Anything you want to talk about?",
            "Wonderful! Anything you want to talk about?",
            "You must be happy. Anything you want to talk about?"]
    
    _neg1_ = ["Oh:( why is that?",
            "Ummmmm why is that?",
            "Oh, that is unfortunate why is that?",
            "Oh no what happened?",
            "Oh no do you wanna tell me more about it?",
            "Oh no tell me more about it:("]

    _neg2_ = ["Oh, that is unfortunate. ",
            "I feel sorry for you.",
            "I am sorry to hear that.",
            "Well it is better than nothing.",
            "Oh no:("]
    
    _10_ = ["Me?",
            "Lets talk something about you how was your day?,",
            "I don’t really matter it is about you.",
            "Hahaha me?",
            "Me? We are talking about you, how was your day?"]


    if y == [1]:
        reply = random.choice(_1_)
    elif y == [2]:
        reply = random.choice(_2_)
    elif y == [-1]:
        reply = random.choice(_neg1_)
    elif y == [-2]:
        reply = random.choice(_neg2_)
    else:
        reply = random.choice(_10_)
    return y, reply


######## choses the simple reply ####################################################################################################################################################################

def simple_reply():
    simplereply =  [" Well alright, anything else I can help you? ",
            "Anything you want to talk about?",
            "Right. Anything else I can help you?",
            "What do you want to talk about now?",
            "Anything you want to talk about or anything I can help you?"]
    txt = random.choice(simplereply)
    return txt
    
def caretext():
    
    caretxt = [" Well you know I’m here and I care. Love you!”",
                "Unfortunately, there’s no way around sadness, but through it. I’m here and will be whenever you need me.",
                "life isn’t fair sometimes. I’m here and I care.",
                "Well I beleve that the problems do not last forever, everything will be fine!",
                "It is ok tho I am with you"]
    
    txt = random.choice(caretxt)
    return txt                
