import json


class JsonPresenter(object):

    def show(self, str_json):
        return json.dumps(str_json, indent=4, sort_keys=True)
