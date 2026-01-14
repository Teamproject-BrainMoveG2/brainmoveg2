from data.database import Database

class ModeRepository:
    @staticmethod
    def get_all_modes(settings):
        sql = "SELECT * FROM spelmodus"
        return Database.get_rows(sql, settings=settings)
    
    @staticmethod
    def get_mode_by_id(settings, mode_id):
        sql = "SELECT * FROM spelmodus WHERE spelmodus_id = %s"
        params = [mode_id]
        return Database.get_one_row(sql, params, settings)