import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn

def pre_process(sentences):
            
    empha = ["absolutely","completely","extremely","highly","really","so","too","totally",
                "very","utterly","fucking","super"]
    no = ["not","n't"]
    past_be_verb = ["was","were"]
    be_verb = ["am","is","are"]
    no_mean = ["want","mum","dad","family","i","everyday"]
    should_be_neg = ["punch","kill","ignore","sad","mad","bully","mom","busy"]
    should_be_pos = ["cool"]

    sentence = nltk.word_tokenize(sentences)
    ###############　pre-processing　##################

    ##cheack if any of the cancel out or not is happening##
    c = 0 #place me
    cancel_out = False
    _not_ = True
    for i in sentence:
        c += 1 #place of word +1
        if i in no: #if the word is in no list
            if c < len(sentence): #if not is not at the end of the sentence
                if sentence[c] in empha: #if word after word[i] is in empha list
                    cancel_out = True
            else:
                _not_ = False 
    tag = nltk.pos_tag(sentence)
    wnl = nltk.WordNetLemmatizer()
    #print(wnl)

    listp = [] # list of word in [word,speech tag, word place, cheaker]
    count = 0
    #generating the listp
    for i in tag:
        count += 1
        listp.append([i[0],i[1],count,0])
    # print(listp)

    #Changing the counter value in listp if any of not or emphasizing#
    counter = 0
    for i in listp:
        #if any of empasizing word is before this word
        if counter == 1:
            i[3] += 1
            counter -= 1
        #if any of "not" is before this word
        elif counter == -1:
            i[3] -= 1
            counter += 1
        #if any of empasizing word is this word
        if i[0] in empha:
            counter += 1
        #if any of "not" is this word
        elif i[0] in no:
            counter -= 1

    ###############　pre-processing　##################

    #################### scoreing #########################

    score_list=[] #list of [score,word,speechtag,wordplacement]
    score_list2=[]# list of all the scores
    JJ_score = 0 # score of adjectives
    past = False
    c = 0
    for t in listp:
        c +=1
        newtag=''
        present_form = WordNetLemmatizer().lemmatize(t[0],'v') #present form (netural form) of the word
        #print(present_form)
        if t[0] in past_be_verb: #if the word is the past be verb(e.g was, were)
            past = True
            score_list.append([0.0,t[0],t[1],c])
        elif (t[0] in no) or (t[0] in empha): #if word is in either of empha list or not list
            score_list.append([0.0,t[0],t[1],c])
        else:
            lemmatized=wnl.lemmatize(t[0])
            if t[1].startswith('NN'): #If noun 
                newtag='n'
            elif t[1].startswith('JJ'): #If adjective
                newtag='a'
            elif t[1].startswith('V'): #If verb
                if t[0] not in be_verb:  #If it is b
                    newtag='v'
                else:
                    nettag = ""
            elif t[1].startswith('R'): # If adverb
                newtag='r'
            else: #If not any of them
                newtag=''     
            if(newtag!=''):    
                synsets = list(swn.senti_synsets(lemmatized, newtag))
                #print(synsets)
                #Getting average of all possible sentiments     
                score=0
                JJ_score = 0
                if(len(synsets)>0): #If the word have more than 1 meaning 
                    for syn in synsets:
                        score+=syn.pos_score()-syn.neg_score() #calculate the total score
                    if cancel_out == True: #if cancel out is happening 
                        if t[1] == "JJ":
                            score = score/2*-1
                    else:                            
                        if t[3] == 1: #If any of the empha word is before this word
                            score = score*2
                        elif t[3] == -1: #if not is before the word
                            if _not_ == False: #if not cancel out 
                                score -= 0.2 #if not is not at the end of the sentence
                            else:
                                score = score*-1

                    if past == True: #if it is about past 
                        if t[1] == "JJ":
                            score = score/2
                    if present_form in no_mean: #if the word should have not neg/pos
                        score = score*0
                    elif present_form in should_be_neg: #if the word should be negative
                        #print("yes")
                        score -= 0.5
                    elif present_form in should_be_pos: #if the word should be positive
                        score += 0.5
                
                    score_list2.append(score/len(synsets))
                    score_list.append([score/len(synsets),t[0],t[1],c])
                    
                else: #If the word does not have more than 1 meaning
                    if present_form in should_be_neg: #if the word should be negative
                        score_list.append([-0.5,t[0],t[1],c])
                        score_list2.append(-0.5)
                    elif present_form in should_be_pos: #if the word should be positive
                        score_list.append([0.5,t[0],t[1],c])
                        score_list2.append(0.5)                        
                    else: 
                        score_list.append([0.0,t[0],t[1],c])
            else:#if not any of (adjective,noun,verb)
                score_list.append([0.0,t[0],t[1],c])
                
    #if it is about the user          
    about_me = 0
    for word in score_list:
        if (about_me == 1) and (word[1] == "me"): #If the word is me and word before is verb and has a negative meaning 
            word_place_of_V_if_aboutme = word_place_of_me+1
            if word_place_of_V_if_aboutme == word[3]:
                score_list2.append(-0.2)
            else:
                about_me = 0
        if (word[2].startswith('V')) and (word[0] <0): #If the word is verb and has a negative meaning 
            about_me = 1
            word_place_of_me = word[3]
    print(score_list)
    fscore = sum(score_list2)

    return fscore, sentence, listp, score_list, JJ_score, score_list

    ###################end of scoring####################



def processing(fscore, sentence, listp, score_list, JJ_score):
    ################### Processing ####################
    length = len(sentence)
    youlist = ["you","You","Your","your"]
    melist = ["i","me","my"]
    because = 0
    you = 0
    me = 0
    question = 0
    fiveWH = 0
    for word in listp:
        if word[1] == "IN":
            if word[0] == "because":
                because += 1
        elif word[1].startswith("PR"):
            if word[0] in youlist:
            
                you += 1
            elif word[0] in melist:
                
                me += 1
        elif word[1] == ".":
            if word[0] == "?":
                question += 1
        elif word[1].startswith("WP"):
            fiveWH += 1

    for element in  score_list:
        if element[2] == "JJ":
            JJ_score += element[0]
            
    fueature_list = [because,you,me,question,fiveWH,length,JJ_score,fscore]
    print(fueature_list)

    return [fueature_list],fscore
