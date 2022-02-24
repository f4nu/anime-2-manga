import pickle


class WanikaniLoader:
    def load_from_file(self, data_filename):
        try:
            with open(data_filename, 'rb') as handle:
                return pickle.load(handle)
        except:
            return None

    def save_to_file(self, data_filename, data):
        with open(data_filename, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)