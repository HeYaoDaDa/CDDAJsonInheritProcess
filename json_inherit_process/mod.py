class mod:
    def __init__(self, jsondata: dict, path: str) -> None:
        self.id: str = jsondata["id"]
        self.name: str = jsondata["name"]
        self.path: list[str] = [path]
        self.dependencies: list[str] = []
        if "dependencies" in jsondata:
            json_depe = jsondata["dependencies"]
            self.dependencies = json_depe if type(
                json_depe) is list else [json_depe]
        self.processed_json_object_map: dict = {}

    def __str__(self) -> str:
        return f"(\n  id:{self.id}\n  name:{self.name}\n  path:{self.path}\n  dependencies:{self.dependencies}\n)"
