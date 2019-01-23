from value_models.user import User
from datetime import datetime


class Status:
    def __init__(self, text="", user=None, photo_source=None):
        self.text = text
        self.user = user
        self.photo_source = photo_source
        self.time_created = datetime.now()

    def __str__(self):
        return 'Status of {} user with text: {}'.format(self.user, self.text)

    def __repr__(self):
        return "{}: text={}, user={}, {}".format(
            self.__class__,
            self.text,
            str(self.user),
            "with photo" if self.photo_source else "without photo"
        )


if __name__ == "__main__":
    some_user = User(username="test", password="test_pass")
    status = Status(user=some_user, text="Some text")
    print(status)
