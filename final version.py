from tkinter import*
from tkinter import messagebox
from pandas import Series,DataFrame
import pandas as pd
import numpy as np
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
import random
from threading import Timer
import time
import speech_recognition as sr


########### main window ###############################################################################################################################################################################################

class Tody:
    def __init__(self,master):

        self.toby_0 = PhotoImage(file='toby+0.png')
        self.toby_1 = PhotoImage(file='toby+1.png')
        self.toby_minus1 = PhotoImage(file='toby-1.png')
        self.toby_psr = PhotoImage(file='toby_psr.png')
        self.toby_minus2 = PhotoImage(file='toby-2.png')
        self.title_label = Label(master,image=self.toby_0,bg = "white" )
        self.title_label.image = self.toby_0
        self.title_label.grid(row =0,columnspan = 20)

        self.comment_label = Label(master, text="Hi my name is Toby! \n Tell me how you are feeling!",height = 5,bg = "#F0F8FF")
        self.comment_label.grid(row=1,columnspan = 20, sticky="ew")

        self.input_bar = Entry(master,width = 15)
        self.input_bar.grid(row =2,column = 0,columnspan = 17, sticky="ew")
        
        mic_img = PhotoImage(file='mic.png')
        self.audiobutton = Button(master,command = self.audio)
        self.audiobutton.image = mic_img
    
        self.audiobutton.config(image=mic_img)
        self.audiobutton.grid(row=2,column =17, sticky="ew" )

        self.enterbutton = Button(master,text ="Send",width = 10,command = self.main)
        self.enterbutton.grid(row=2,column =18,columnspan = 2, sticky="nsew")
        
#######################################################################################################################################################################################################################


############### audio system ##########################################################################################################################################################################################
        
    def audio(self):
        self.input_bar.delete(0, 'end')
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            self.input_bar.insert(END, r.recognize_sphinx(audio))
            print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            self.input_bar.insert(END, "Tody could not understand audio")
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
            
######################################################################################################################################################################################################################


######## processing the inputs ########################################################################################################################################################################################

    def prosser(self,sentences):
                
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
    
        ###################end of scoring####################

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
                print("hi")
                JJ_score += element[0]
                
        fueature_list = [because,you,me,question,fiveWH,length,JJ_score,fscore]
        print(fueature_list)

        return [fueature_list],fscore
        ################### end of Processing ####################

#####################################################################################################################################################################################################################



####### train MLP and give a pridiction on input #####################################################################################################################################################################
    
    def MLpredict(self,x):
        
        df = pd.read_csv("train.csv")

        df_X = df.copy()
        df_Y = df.copy()

        drop_idx = ["Y"]
        df_X = df_X.drop(drop_idx, axis = 1)


        drop_idx = ["because","you","me","question","fiveWH","length","JJ_score","fscore"]
        df_Y = df_Y.drop(drop_idx, axis = 1)

        test_index = x

        #MLPClassifier
        from sklearn.neural_network import MLPClassifier
        my_classifier = MLPClassifier(solver='lbfgs', random_state=0)
        my_classifier.fit(df_X,df_Y.values.ravel())
        # Predict 
        print(my_classifier.predict(test_index))
        return my_classifier.predict(test_index)
    
######################################################################################################################################################################################################################


######## choses the reply based on the pridiction ####################################################################################################################################################################
    
    def MLreply(self,y):
        
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
            self.title_label.config(image = self.toby_1)
            reply = random.choice(_1_)
        elif y == [2]:
            self.title_label.config(image = self.toby_0)
            reply = random.choice(_2_)
        elif y == [-1]:
            self.title_label.config(image = self.toby_minus1)
            reply = random.choice(_neg1_)
        elif y == [-2]:
            self.title_label.config(image = self.toby_minus2)
            reply = random.choice(_neg2_)
        else:
            reply = random.choice(_10_)

        self.comment_label.configure(text = reply)
        return y

######################################################################################################################################################################################################################


############ if the input is simple and can auto reply ###############################################################################################################################################################
    
    def autoreply(self,t):
        auto = 0
        sentence = nltk.word_tokenize(t)
        tag = nltk.pos_tag(sentence)
        listi = []
        count = 0
        for i in tag:
            count += 1
            listi.append([i[0],i[1],count])
        print(listi)
        greating = ["hi","hello","sup","good morning","good evening","good afternoon"]
        for element in listi:
            if element[2] == 1:
                if element[0] in greating:
                    self.title_label.config(image = self.toby_0)
                    self.comment_label.configure(text ="hello")
                    auto = 1
                elif  element[1].startswith("WP"):
                    self.title_label.config(image = self.toby_0)
                    self.comment_label.configure(text ="I am so sorry I don't know the answer to that ")
                    auto = 1

        if t == "how are you?":
            self.title_label.config(image = self.toby_0)
            self.comment_label.configure(text ="I am good thank you and you?")
            auto = 1
        elif t == "no":
            self.title_label.config(image = self.toby_0)
            self.comment_label.configure(text ="Right, anything you want to talk about?")
        elif t == "yes":
            self.comment_label.configure(text ="Right")
        elif (t == "do you like me") or (t == "do you like me ?"):
            self.title_label.config(image = self.toby_0)
            self.comment_label.configure(text ="Of course I do, why wouldn't I ?")
        
        return auto
        
    def simple_reply(self):
        simplereply =  [" Well alright, anything else I can help you? ",
               "Anything you want to talk about?",
               "Right. Anything else I can help you?",
               "What do you want to talk about now?",
               "Anything you want to talk about or anything I can help you?"]
        txt = random.choice(simplereply)
        self.comment_label.configure(text = txt)
        
######################################################################################################################################################################################################################                
                
    def caretext(self):
        
        caretxt = [" Well you know I’m here and I care. Love you!”",
                   "Unfortunately, there’s no way around sadness, but through it. I’m here and will be whenever you need me.",
                   "life isn’t fair sometimes. I’m here and I care.",
                   "Well I beleve that the problems do not last forever, everything will be fine!",
                   "It is ok tho I am with you"]
        
        txt = random.choice(caretxt)
        self.comment_label.configure(text = txt)


###################### psr ############################################################################################################################################################################################
        
    def ask_if_psr(self):
        self.comment_label.configure(text = "To refresh your mind, \n would you like to play a game of paper scissors rock?")
        time.sleep(3)
        self.answer = messagebox.askquestion("paper scissors rock?","So would you like to play?")

    def setuo_psr(self):
        if self.answer == "yes":
            self.title_label.config(image = self.toby_psr)
            self.mini_window = Toplevel(window)
            self.mini_window.geometry("+%d+%d" % (1100,350))
            self.players_point = 0
            self.comp_point = 0

            title_label = Label(self.mini_window, text = "pps" )
            title_label.grid(row =0,columnspan = 3)

            self.comp_label = Label(self.mini_window, text="Ok Lets play !, whoever gets 3 points first wins! \n Choose your hand!",height = 5,bg = "#F0F8FF")
            self.comp_label.grid(row=1,columnspan = 3, sticky="ew")

            self.p_button = Button(self.mini_window,text ="paper",width = 10,command = lambda: self.psr_play("paper"))
            self.p_button.grid(row=2,column =0, sticky="ew")

            self.s_button = Button(self.mini_window,text ="scissors",width = 10,command = lambda: self.psr_play("scissors"))
            self.s_button.grid(row=2,column =1, sticky="ew")
            
            self.r_button = Button(self.mini_window,text ="rock",width = 10,command = lambda: self.psr_play("rock"))
            self.r_button.grid(row=2,column =2, sticky="ew")
        else:
            self.comment_label.configure(text = "Anything else I can help you?")
            
    def psr_play(self,hand):
         
        r = ""
        player = hand
        if self.comp_point == 2:
            if player == "rock":
                self.comp_label.configure(text = "Tody: Scissors")
            elif player == "paper":
                self.comp_label.configure(text = "Tody: Rock")
            else:
                self.comp_label.configure(text = "Tody: Paper")
            r = "win"

        else:
            t = ["rock", "paper", "scissors"]
            comp = random.choice(t)
            self.comp_label.configure(text = "Tody;{}".format(comp))
            if player == comp:
                r = "tie"
            elif player == "rock":
                if comp == "paper":
                    r = "lose"
                else:
                    r = "win"
            elif player == "paper":
                if comp == "scissors":
                    r = "lose"
                else:
                    r = "win"
            elif player == "scissors":
                if comp == "rock":
                    r = "lose"
                else:
                    r = "win"
        process = Timer(2, self.psr_prosess,args=(r,))
        process.start()

        
    def psr_prosess(self,result):
        win = Timer(2, self.psr_win,args=())
        
        if (self.players_point < 2) and (result == "win"):
            self.players_point += 1
            self.comp_label.configure(text = "You got 1 point! \n choose your next hand!")
        elif (self.players_point == 2) and (result == "win"):
            self.comp_label.configure(text = "You got three points you won. You are too good")
            win.start()
        elif result == "lose":
            self.comp_point += 1
            self.comp_label.configure(text = "You lost 1 point:( \n choose your next hand!")
        elif result == "tie":
            self.comp_label.configure(text = "Tie!  \n choose your next hand!")

    def psr_win(self):
        self.again = messagebox.askquestion("paper scissors rock?","Play again?")
        again = Timer(2, self.again_or_not_process,args=())
        again.start()
        

    def again_or_not_process(self):
        if self.again == "yes":
            self.players_point = 0
            self.comp_point = 0
            self.comp_label.configure(text = "Ok lets play again!  \n choose your hand!")
        else:
            self.mini_window.destroy()
            self.how_was_thegame()
            
    def how_was_thegame(self):
        self.comment_label.configure(text = "How are you feeling now?")

#######################################################################################################################################################################################################################


################## main function ######################################################################################################################################################################################
        
    def main(self):
        caretext = Timer(3.0, self.caretext,args=())
        ask_psr = Timer(8.0, self.ask_if_psr,args=())
        psr = Timer(15.0, self.setuo_psr,args=())

        
        score = 0
        text = self.input_bar.get()
        text = text.lower()
        z = self.autoreply(text)
        if z != 1:
            x = self.prosser(text)
            score += x[1]
            if x[1] != 0:           
                y = self.MLpredict(x[0])
                i = self.MLreply(y)
                if i == [-2]:
                    caretext.start()
                    ask_psr.start()
                    psr.start()
                    
                
                        
            else:
                self.title_label.config(image = self.toby_0)
                self.simple_reply()
        self.input_bar.delete(0, 'end')                
        print(score)

#######################################################################################################################################################################################################################

window = Tk()
my_gui = Tody(window)
window.title("tody")
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel()) 
window.mainloop()


