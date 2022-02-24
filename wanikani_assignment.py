import requests

from wanikani_loader import WanikaniLoader


class WanikaniAssignment:
    data_filename = 'data/wanikani_assignments.pickle'
    
    id = None
    subject_id = None
    subject_type = None
    srs_stage = None

    assignments = {}

    def __init__(self, assignment_data):
        self.id = assignment_data['id']
        self.subject_id = assignment_data['data']['subject_id']
        self.subject_type = assignment_data['data']['subject_type']
        self.srs_stage = assignment_data['data']['srs_stage']

    @classmethod
    def load(cls, api_key):
        loader = WanikaniLoader()
        data = loader.load_from_file(cls.data_filename)
        if data is None:
            cls.retrieve_assignments(api_key)
        else:
            cls.assignments = data

        if cls.assignments:
            loader.save_to_file(cls.data_filename, cls.assignments)

    @classmethod
    def retrieve_assignments(cls, api_key):
        print('Retrieving assignments via API')
        headers = {'Authorization': f'Bearer {api_key}'}
        query = {'subject_types': 'vocabulary'}
        next_url = 'https://api.wanikani.com/v2/assignments'
        while next_url is not None:
            print(f'Fetching {next_url}')
            response = requests.get(next_url, params=query, headers=headers)
            json = response.json()
            next_url = json['pages']['next_url']
            wk_data = json['data']
            for assignment_data in wk_data:
                cls.assignments[assignment_data['data']['subject_id']] = WanikaniAssignment(assignment_data)

    @classmethod
    def get_assignment(cls, subject_id):
        return cls.assignments.get(subject_id)