import os

from dotenv import load_dotenv
from wanikani_assignment import WanikaniAssignment
from wanikani_word import WanikaniWord

class Wanikani:
    load_dotenv()
    api_key = os.getenv('WANIKANI_API_KEY')

    def __init__(self) -> None:
        WanikaniWord.load(self.api_key)
        WanikaniAssignment.load(self.api_key)