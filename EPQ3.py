import os
import sys
import pygame
import time

import speech_recognition
from gtts import gTTS

class Bot:
    def __init__(self):

        """this dictionary stores the key pair values for the first
           required phrase component of a command (pair) from a
           piece of dialogue (key) usually the start of a sentence"""
        
        first_term_store = {"search":"search_",
                            "open":"open_",
                            "find":"search_",
                            "look":"search_",
                            "is":"question_",
                            "what is":"query_",
                            "what's":"query_",
                            "activate":"activate",
                            "deactivate":"deactivate",
                            "say":"say_",
                            "tell":"tell_"}
        
        """this dictionary stores the key pair values for the middle
           required phrase component of a command (pair) from a
           piece of dialogue (key) this is usually a concrete noun"""
        
        mid_term_store = {"file":"file",
               "document":"file",
               "website":"website",
               "time":"time",
               "weather":"weather",
               "date":"date",
               "hello":"hello",
               "joke":"joke"}

        """this dictionary stores the key pair values for the extension terms
           of which are optional in a sentence, the pair value is not required
           hence a blank string."""
        
        extra_grammar_store = {"called":"",
                               "named":"",
                               "the":"",
                               "a":""}

        """this dictionary binds the previous three together as members of one object"""
        
        self.phrase_store = [first_term_store,
                             mid_term_store,
                             extra_grammar_store]
        
        self.run = False
        self.listen()   

    def speech(self,output_dialogue: str) -> None:

        """this functions takes in a string and plays an audio file
           of a text-to-speech conversion of the contents"""
        
        text_to_speech = gTTS(output_dialogue)
        try:
            file_name = 'playback.mp3'
            text_to_speech.save(file_name)
        except:
            file_name = 'alt_playback.mp3'
            text_to_speech.save(file_name)
            pass

        pygame.mixer.init()
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    def comprehend(self,sentence: str) -> None:

        """this functions takes in a string and breaks down the components into either query_item
           content or keys to the phrase_store dictionary; used for converting the contents of the
           sentence into parts of the function(to be called)'s name"""
        
        function_name = ""
        phrase_counter = 0
        sentence_fault = False
        query_item = []

        print(sentence)
        print(phrase_counter)
        for word in sentence.split():
            for item in self.phrase_store:
                for key,pair in item.items():

                    """phrase_counter shall be used to check wherever there is an appropriate mid_term_store
                       and first_term_store value e.g.: search, file"""
                    if phrase_counter != 2 and key == word and word not in self.phrase_store[2]:
                        phrase_counter+=1
                        function_name+=pair
                        
                        
            if phrase_counter == 2 and word not in self.phrase_store[2]:
                print(word)
                query_item.append(word)
                

              
                    
                #if key in self.phrase_store[2] and phrase_counter != 2:  
                 #   phrase_counter-=1
            print(phrase_counter) 
        sentence_fault = False
            #if phrase_counter >= 2 and item not in self.phrase_store[2]:
             #   print("yes")
              #  query_item += item
        phrase_counter = 0
                        
        print(function_name)
        print(query_item)
        if len(query_item) != 0:
            query_item.remove(query_item[0])
            query_item = "".join(query_item)

        """These if statements determine wherever the bot has been activated or not based on
           the 'activate'/'deactivate command nad self.run variable or if another command
           has been run after activation"""
        
        if function_name == "activate":
            self.speech("activated")
            self.run = True
        elif function_name == "deactivate":
            self.speech("deactivated")
            self.run = False
        elif self.run != True:
            self.listen()
        else:
            self.speech("sentence recognised")

            """Try and except statement used to check wherever a command exists or not"""
            
            print(query_item)
            try:
                print(f"self.{function_name}({query_item})")
                exec(f"self.{function_name}('{query_item}')")
            except:
                pass
            
    def listen(self):

        """this function handles audio input and converts the values to string and then
           executes the self.comprehend function with the string as a parameter"""
        
        while True:
            recog = speech_recognition.Recognizer()
            with speech_recognition.Microphone() as source:
                audio = recog.listen(source)
                try:
                    command = recog.recognize_google(audio)
                except:
                    command = ""
                    pass
                print("YES")
                print(command)
                self.comprehend(command)
                
    def say_hello(self,_) -> None:
        self.speech("Hello everyone")

    def tell_joke(self,_) -> None:
        self.speech("Why did the functions stop calling each other?")
        time.sleep(3)
        self.speech("Because they had constant arguments.")
        
        
test_bot = Bot()

