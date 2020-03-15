import mysql.connector
 
conn = mysql.connector.connect(host="localhost", port="3308",
                               user="test_python", password="Kkj4VC1YJOn5NeOk", 
                               database="test_python")
cursor = conn.cursor()
cursor.execute("""SELECT * FROM player""")
myresult = cursor.fetchall()
print(myresult)


def createPlayer(username):
    sqlInsert = "Insert into Player(username) values (" + username.capitalize() + ");"
    cursor.execute(sqlInsert)

def setWinner(idPlayer1, idPlayer2):
    sqlInsert = "Insert into PartyHistoric(IdLoser, IdWinner) values (" + idPlayer1 + "," + idPlayer2 + ");"
    cursor.execute(sqlInsert)

def getPlayerByUsername(username):
    sqlSelect = "SELECT id FROM player WHERE username = 'Kevin'"
    print(sqlSelect)
    cursor.execute(sqlSelect)
    result = cursor.fetchall()
    return result
test = getPlayerByUsername("Kevin")
print(test)
print(type(test))

conn.close()
