class User:
    def __init__(self, id=None, username="", password="", email="",
                 real_name="", is_admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.real_name = real_name
        self.is_admin = is_admin

    def __str__(self):
        return "User: username={}, {}".format(
            self.username,
            "admin" if self.is_admin else "not admin"
        )

    def __repr__(self):
        return "{}: username={}, password={}, email={}{}".format(
            self.__class__,
            self.username,
            self.password,
            self.email,
            "admin" if self.is_admin else "not admin"
        )


if __name__ == "__main__":
    user = User("Masha", "Pupkin")
    print(user)
