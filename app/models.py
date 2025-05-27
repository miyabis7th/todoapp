import datetime
import uuid

class Todo:
    def __init__(self, title, description='', completed=False, image_url=None, id=None, created_at=None):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.completed = completed
        self.image_url = image_url
        self.created_at = created_at or datetime.datetime.now()

    @staticmethod
    def from_dict(source):
        """Create a Todo from a Firestore document."""
        todo = Todo(
            title=source['title'],
            description=source.get('description', ''),
            completed=source.get('completed', False),
            image_url=source.get('image_url'),
            id=source.get('id'),
            created_at=source.get('created_at')
        )
        return todo

    def to_dict(self):
        """Return a dictionary representation of the Todo."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'image_url': self.image_url,
            'created_at': self.created_at
        }