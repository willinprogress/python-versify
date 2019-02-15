import util
from model.Testament import Testament


class Version:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.testaments = []

    def get_testaments(self):
        t = []
        url = util.Dbt.Dbt.get_api_url("/library/volume", {"language_family_code": util.Dbt.Dbt.language, "media": "text"})
        testaments = util.Dbt.Dbt.get_request(url)
        for testament in testaments:
            if self.name != testament["version_code"]:
                continue
            t.append(Testament(testament['volume_name'],
                          testament['dam_id'],
                          testament['collection_code'],
                          self))
        return t