from wanikani_loader import WanikaniLoader
from wanikani_word_meaning import WanikaniWordMeaning
import requests


class WanikaniWord:
    data_filename = 'data/wanikani_words.pickle'

    id = None
    url = None
    level = None
    slug = None
    spaced_repetition_system_id = None
    meanings = []

    words = {}

    def __init__(self, word_data):
        self.id = word_data['id']
        self.url = word_data['url']
        self.level = word_data['data']['level']
        self.slug = word_data['data']['slug']
        self.spaced_repetition_system_id = word_data['data']['spaced_repetition_system_id']
        for meaning in word_data['data']['meanings']:
            self.meanings.append(WanikaniWordMeaning(meaning['meaning']))

    @classmethod
    def load(cls, api_key):
        loader = WanikaniLoader()
        data = loader.load_from_file(cls.data_filename)
        if data is None:
            cls.retrieve_words(api_key)
        else:
            cls.words = data

        if cls.words:
            loader.save_to_file(cls.data_filename, cls.words)

    @classmethod
    def retrieve_words(cls, api_key):
        print('Retrieving words via API')
        headers = {'Authorization': f'Bearer {api_key}'}
        query = {'types': 'vocabulary'}
        next_url = 'https://api.wanikani.com/v2/subjects'
        while next_url is not None:
            print(f'Fetching {next_url}')
            response = requests.get(next_url, params=query, headers=headers)
            json = response.json()
            next_url = json['pages']['next_url']
            wk_data = json['data']
            for word_data in wk_data:
                cls.words[word_data['id']] = WanikaniWord(word_data)

    @classmethod
    def get_word(cls, word):
        return next((cls.words[x] for x in cls.words if cls.words[x].slug == word), None)