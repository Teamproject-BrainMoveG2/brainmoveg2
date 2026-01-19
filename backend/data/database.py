from mysql import connector
import os

class Database:

    # 1. Opening Connection
    @staticmethod
    def __open_connection(settings):
        try:
            db = connector.connect(
                            host=settings.host,
                            user=settings.dbuser,
                            password=settings.password,
                            database=settings.database,
                            autocommit=False
                        ) 
            if "AttributeError" in (str(type(db))):
                raise Exception("\033[0m Incorrect Database Connection Values\033[0m")
            cursor = db.cursor(dictionary=True, buffered=True)  # lazy loaded
            return db, cursor
        except connector.Error as err:
            if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("\033[0mError: Authentication failed when connecting to database\033[0m")
            elif err.errno == connector.errorcode.ER_BAD_DB_ERROR:
                print("\033[0mError: Database not found\033[0m")
            else:
                print(err)
            return

    # 2. Executes READS
    @staticmethod
    def get_rows(sqlQuery, params=None, settings=None):
        result = None
        db, cursor = Database.__open_connection(settings)
        try:
            cursor.execute(sqlQuery, params)
            result = cursor.fetchall()
            cursor.close()
            if result is None:
                print(ValueError(f"\033[0mResults are non-existent.[DB Error]\033[0m"))
            db.close()
        except Exception as error:
            print(error)
            result = None
        finally:
            return result

    @staticmethod
    def get_one_row(sqlQuery, params=None, settings=None):
        db, cursor = Database.__open_connection(settings)
        try:
            cursor.execute(sqlQuery, params)
            result = cursor.fetchone()
            cursor.close()
            if result is None:
                raise ValueError("\033[0mResults are non-existent.[DB Error]\033[0m")
        except Exception as error:
            print(error)
            result = None
        finally:
            db.close()
            return result

    # 3. Executes INSERT, UPDATE, DELETE with PARAMETERS
    @staticmethod
    def execute_sql(sqlQuery, params=None, settings=None):
        result = None
        db, cursor = Database.__open_connection(settings)
        try:
            cursor.execute(sqlQuery, params)
            db.commit()
            # confirmation of create (int or 0)
            result = cursor.lastrowid
            # confirmation of update, delete (array)
            # result = result if result != 0 else params  # Extra control needed!!
            if result != 0:  # is an insert, return the lastrowid.
                result = result
            else:  # is an update or a delete
                if cursor.rowcount == -1:  # There is an error in the SQL
                    raise Exception("\033[0mError in SQL\033[0m")
                elif (
                    cursor.rowcount == 0
                ):  # Nothing was changed, where clause does not match or no change in data
                    result = 0
                elif result == "undefined":
                    raise Exception("\033[0mSQL error\033[0m")
                else:
                    result = cursor.rowcount
        except connector.Error as error:
            db.rollback()
            result = None
            print(f"\033[0mError: Data not saved.{error.msg}\033[0m")
        finally:
            cursor.close()
            db.close()
            return result
