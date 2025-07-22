from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from datetime import datetime

class Base(SQLModel):
    item_id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        unique=True,
    )
    item_created: datetime = Field(default_factory=datetime.now)
    item_modified: datetime = Field(default_factory=datetime.now)

    def create(self):
        """Initializes ItemBase default fields when a new item is created."""
        self.item_created = datetime.now()
        self.item_modified = datetime.now()

    def update(self):
        """Updates ItemBase default fields when an item is modified."""
        self.item_modified = datetime.now()