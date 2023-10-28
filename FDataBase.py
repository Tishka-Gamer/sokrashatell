import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


# connect = sqlite3.connect("database.db")
# cursor = connect.cursor()


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getUser(self):
        sql = '''SELECT * FROM user'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Ошибка чтения бд')
        return []

    def addUser(self, login, hpsw):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM user WHERE login LIKE "{login}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь существует')
                return False
            self.__cur.execute('INSERT INTO user VALUES(NULL, ?, ?)', (login, hpsw))
            self.__db.commit()
        except sqlite3.Error as e:
            print('руки крюки')
            return False
        return True

    def SingIn(self, login, hpsw):
        # try:
        res = self.__cur.execute('SELECT * FROM "user" WHERE login = ?', (login,)).fetchone()
        print(res)
        if res is None:
            return False
        else:
            if check_password_hash(res['password'], hpsw):
                return True

    # except sqlite3.Error as e:
    #     print('руки крюки')
    #     return False

    def searchLink(self, sokr):
        self.__cur.execute(f'SELECT * FROM link WHERE psev = "{sokr}"')
        return self.__cur.fetchone()

    def searchLinnk(self, sokr):
        print(sokr)
        self.__cur.execute(f'SELECT * FROM link WHERE psev LIKE"%{sokr}%"')
        return self.__cur.fetchone()

    def SearchUser(self, login):
        self.__cur.execute(f'SELECT * FROM "user" WHERE login = "{login}"')
        return self.__cur.fetchone()[0]

    def addLink(self, link, sokr, type, id):
        if self.searchLink(sokr) == None:
            print(link, sokr, type, id)
            self.__cur.execute('INSERT INTO "link" VALUES(NULL, ?, ?, ?, ?, ?)', (link, sokr, type, 0, id))
            self.__db.commit()
            return True
        else:
            return False

    def userLinks(self, user):
        self.__cur.execute(f'SELECT * FROM link WHERE id_user = "{user}"')
        return self.__cur.fetchall()

    def serLink(self, id):
        self.__cur.execute(f'SELECT * FROM link WHERE id = "{id}"')
        return self.__cur.fetchone()

    def delLink(self, id):
        self.__cur.execute(f'DELETE FROM link WHERE id = "{id}"')
        self.__db.commit()

    def updat(self, id, psev, type):
        if self.searchLinnk(psev) == None:
            self.__cur.execute(f'UPDATE link SET psev = ?, type = ? WHERE id = ?', (psev, type, id))
            self.__db.commit()
        else:
            'ошибка'

    def updateCount(self, id):
        self.__cur.execute(f'UPDATE link SET count = count + 1 WHERE id = ?', (id,))
        self.__db.commit()
    # def sear
