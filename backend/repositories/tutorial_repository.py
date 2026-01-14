from data.database import Database

class TutorialRepository:
    @staticmethod
    def get_rondes_by_mode_id(settings, mode_id):
        sql = "SELECT * FROM spelmodus_handleiding_stappen WHERE spelmodus_id = %s"
        params = [mode_id]
        return Database.get_rows(sql, params, settings)