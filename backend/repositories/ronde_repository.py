from data.database import Database


class RondeRepository:
    @staticmethod
    def create_ronde(settings, sessie_id, ronde_nummer, reactietijd_ms, potje_id, uitkomst):
        sql = "INSERT INTO spelronde (spelsessie_id, ronde_nummer, reactietijd_ms, potje_id, uitkomst) VALUES (%s, %s, %s, %s, %s)"
        params = [sessie_id, ronde_nummer, reactietijd_ms, potje_id, uitkomst]
        return Database.execute_sql(sql, params, settings)
    
    @staticmethod
    def get_ronde_by_id(settings, ronde_id):
        sql = "SELECT * FROM spelronde WHERE id = %s"
        params = [ronde_id]
        return Database.get_one_row(sql, params, settings)