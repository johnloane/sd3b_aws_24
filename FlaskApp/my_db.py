from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.String(21), nullable=False)
    token = db.Column(db.String(255))
    login = db.Column(db.Integer)
    read_access = db.Column(db.Integer)
    write_access = db.Column(db.Integer)

    def __init__(self, name, user_id, token, login, read_access, write_access):
        self.name = name
        self.user_id = user_id
        self.token = token
        self.login = login
        self.read_access = read_access
        self.write_access = write_access


def delete_all():
    try:
        db.session.query(User).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def get_user_row_if_exists(user_id):
    get_user_row = User.query.filter_by(user_id = user_id).first()
    if get_user_row is not None:
        return get_user_row
    else:
        print("That user does not exist")
        return False
    

def add_user_and_login(name, user_id):
    row = get_user_row_if_exists(user_id)
    if row is not False:
        row.login = 1
        db.session.commit()
    else:
        new_user = User(name, user_id, None, 1, 0, 0)
        db.session.add(new_user)
        db.session.commit()


def user_logout(user_id):
    row = get_user_row_if_exists(user_id)
    if row is not False:
        row.login = 0
        db.session.commit()


def add_token(user_id, token):
    row = get_user_row_if_exists(user_id)
    if row is not False:
        row.token = token
        db.session.commit()


def get_token(user_id):
    row = get_user_row_if_exists(user_id)
    if row is not False:
        return row.token
    else:
        print("User with id: " + user_id + " doesn't exist")


def view_all():
    rows = User.query.all()
    print_results(rows)


def print_results(rows):
    for row in rows:
        print(f"{row.id} | {row.name} | {row.user_id} | {row.token} | {row.login} | {row.read_access} | {row.write_access}")
        

def get_all_logged_in_users():
    rows = User.query.filter_by(login=1).all()
    user_records = {"users" : []}
    for row in rows:
        if row.read_access == 1:
            read = "checked"
        else:
            read = "unchecked"
        if row.write_access == 1:
            write = "checked"
        else:
            write = "unchecked"
        user_records["users"].append([row.name, row.user_id, read, write])
    return user_records

def add_user_permission(user_id, read, write):
    row = get_user_row_if_exists(user_id)
    if row is not False:
        if read == "true":
            row.read_access = 1
        else:
            row.read_access = 0
        if write == "true":
            row.write_access = 1
        else:
            row.write_acccess = 0
        db.session.commit()






    


        
