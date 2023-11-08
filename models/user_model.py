from .entities.user import User


class UserModel:

    # This method can be used for both login and register
    @classmethod
    def login(cls, db, user):

        # check if username exits
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname FROM user 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                # retrieve selected user
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])

                return user

            return None
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def register(cls, db, user):
        """Creates a new user and returns the id"""
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO user (username, password, used_tokens, email, age, fullname)
            VALUES (%s, %s, %s, %s, %s, %s)"""

            values = (user.username, User.generate_password(user.password), 0, user.email, user.age, user.fullname)
            cursor.execute(sql, values)

            # new user id
            user_id = cursor.lastrowid

            # commit changes
            db.connection.commit()
            cursor.close()
            return user_id
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_tokens(cls, db, user_id, tokens):
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE user SET used_tokens = used_tokens + %s
        WHERE id = %s """
            values = (tokens, user_id)
            cursor.execute(sql, values)

            # commit changes
            db.connection.commit()
            cursor.close()

        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, fullname, used_tokens FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], None, None, row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
