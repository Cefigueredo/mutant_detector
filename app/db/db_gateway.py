import json
import os

FILE_PATH = "app/db/sequences.json"


class DBGateway:
    def read_detections(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as file:
                return json.load(file)
        else:
            os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

        return {"sequences": []}

    def write_detections(self, detections):
        with open(FILE_PATH, "w") as file:
            json.dump(detections, file, indent=4)

    def read_sequences(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as file:
                data = json.load(file)
                return data.get("sequences", [])
        return []

    def write_sequences(self, sequences):
        data = self.read_detections()
        data["sequences"] += [sequences]
        self.write_detections(data)
