


class AvatarFrame:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.id: str = data.get("id")
        self.icon: str = data.get("icon")
        self.resource: str = data.get("resource")
        self.name: str = data.get("name")
        self.status: int = data.get("status")
        self.version: int = data.get("version")
        self.restrictionType: int = data.get("restrictionType")