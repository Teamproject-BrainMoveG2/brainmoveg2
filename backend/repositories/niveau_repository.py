from data.database import Database

class NiveauRepository:
    @staticmethod
    def get_niveau_by_id(settings, id):
        sql = "SELECT name FROM niveaus WHERE niveau_id = %s"
        params = [id]
        return Database.get_one_row(sql, params, settings=settings)
    