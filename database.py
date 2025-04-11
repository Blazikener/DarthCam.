import MySQLdb
def get_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="idk@6332",
        db="sisthack"
    )
