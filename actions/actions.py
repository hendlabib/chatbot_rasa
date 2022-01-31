# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []



def country_db():
    
    URL = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries"
    r = requests.get(URL).json()
        
    db = []    
    for value in r['body']:
        
        
        value = value.lower()
        db.append(value)   

    """LIST of supported COUNTRIES"""
    return db
    

class ActionFormCapital(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        
        return "form_info_capital"
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
       """ A list of required slots that the form has to fill"""
       return ["country"]
             
    def slot_mappings(self) -> Dict[Text,Union[Dict,List[Dict]]]:
        """ A dictionary to map required slots to 
        - an extracted entity 
        - intent: value pairs
        - a whole message 
        or list of them ,where a first match will be picked"""
        return { "country": [self.from_entity(eninty="country", intent = "capital")]}
      
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do 
        after all required slots are filled"""
      
        dispatcher.utter_message("utter_submit",tracker,country=tracker.get_slot('country'))

        return [] 

    
    
    def validate_capital (self,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Dict[Text, Any]:
      
        url_capital = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCapital"
        
        value = tracker.get_slot("country")
        """Validate Country value."""
        if value.lower() in self.country_db(): 
            """if the user enter lower case""" 
            country = {"country": value.capitalize()}  
            capital = requests.post(url_capital, json=country).json()   
            capital = capital['body']['capital']
            dispatcher.utter_message(template="utter_capital")
            
            return {"country": country,
                    "capital":capital}
        else:
            dispatcher.utter_message(template="utter_wrong_value")
            # valida+tion failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"country": None}    
            

        
class ActionFormPopulation(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        
        return "form_info_population"
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
       """ A list of required slots that the form has to fill"""
       return ["country"]
             
    def slot_mappings(self) -> Dict[Text,Union[Dict,List[Dict]]]:
        """ A dictionary to map required slots to 
        - an extracted entity 
        - intent: value pairs
        - a whole message 
        or list of them ,where a first match will be picked"""
        return { "country": [self.from_entity(eninty="country", intent = "population")]}
      
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do 
        after all required slots are filled"""
      
        dispatcher.utter_message("utter_submit",tracker,country=tracker.get_slot('country'))

        return [] 

              
    def validate_population (self,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Dict[Text, Any]:
      
        url_population = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getPopulation"
        
        value = tracker.get_slot("country")
        if value.lower() in self.country_db(): 
            """if the user enter lower case""" 
            country = {"country": value.capitalize()}  
            population = requests.post(url_population, json=country).json()   
            population = population['body']['population']
            dispatcher.utter_message(template="utter_population")
            
            return {"country": country,"population":population}
        else:
            dispatcher.utter_message(template="utter_wrong_value")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"country": None} 