from .. import db

class User(db.Model):
    userid       = db.Column(db.String(32), unique=True,  nullable=False, primary_key=True)
    lib_username = db.Column(db.String(64), unique=False, nullable=False)
    lib_password = db.Column(db.String(64), unique=False, nullable=False)

    def __repr__(self):
        return f"<User ${self.userid}>"
