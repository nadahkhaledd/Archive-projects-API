

class Asset:
    id: int
    name: str

    def fromJson(self, id: int, name: str) -> None:
        self.id = id
        self.name = name



class Department:
    id: int
    name: str
    asset: Asset

    def fromJson(self, id: int, name: str, asset: Asset) -> None:
        self.id = id
        self.name = name
        self.asset = asset


class Project:
    id: int
    name: str
    department: Department

    def fromJson(self, id: int, name: str, department: Department) -> None:
        self.id = id
        self.name = name
        self.department = department
