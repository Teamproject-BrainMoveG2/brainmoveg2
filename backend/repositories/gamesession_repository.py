from data.database import Database

class GameSessionRepository:
    @staticmethod
    def create_session(settings, username, mode_id, difficulty_id, started_on):
        sql = "INSERT INTO spelsessie (gebruikersnaam, spelmodus_id, moeilijkheid_id, gestart_op) VALUES (%s, %s, %s, %s)"
        params = [username, mode_id, difficulty_id, started_on]
        return Database.execute_sql(sql, params=params, settings=settings)
    
    @staticmethod
    def end_session(settings, session_id, ended_on, score):
        sql = "UPDATE spelsessie SET geëindigd_op = %s, score = %s WHERE id = %s"
        params = [ended_on, score, session_id]
        return Database.execute_sql(sql, params=params, settings=settings)
    
    @staticmethod
    def get_top_scores(settings, limit=10):
        sql = "SELECT gebruikersnaam, score, RANK() OVER (ORDER BY score DESC) AS rank FROM spelsessie ORDER BY score DESC LIMIT %s"
        params = [limit]
        return Database.get_rows(sql, params=params, settings=settings)
    
    @staticmethod
    def get_player_rank(settings, session_id):
        sql = "SELECT RANK() OVER (ORDER BY score DESC) AS rank FROM spelsessie WHERE id = %s"
        params = [session_id]
        return Database.get_one_row(sql, params=params, settings=settings)