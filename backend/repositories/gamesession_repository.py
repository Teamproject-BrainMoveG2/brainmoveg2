from data.database import Database

class GameSessionRepository:
    @staticmethod
    def create_session(settings, username, mode_id, difficulty_id, started_on):
        sql = "INSERT INTO spelsessie (username, spelmodus_id, moeilijkheid_id, gestart_op) VALUES (%s, %s, %s, %s)"
        params = [username, mode_id, difficulty_id, started_on]
        return Database.execute_sql(sql, params=params, settings=settings)
    
    @staticmethod
    def end_session(settings, session_id, ended_on, score):
        sql = "UPDATE spelsessie SET geëindigd_op = %s, score = %s WHERE spelsessie_id = %s"
        params = [ended_on, score, session_id]
        return Database.execute_sql(sql, params=params, settings=settings)
    
    @staticmethod
    def get_top_scores(settings, mode_id, limit=10):
        sql = "SELECT username, score, RANK() OVER (ORDER BY score DESC) AS rank FROM spelsessie WHERE spelmodus_id = %s ORDER BY score DESC LIMIT %s"
        params = [mode_id, limit]
        return Database.get_rows(sql, params=params, settings=settings)
    
    @staticmethod
    def get_player_rank(settings, session_id):
        sql = "WITH ranked_sessions AS (SELECT spelsessie_id, username, score, RANK() OVER (ORDER BY score DESC) AS rank FROM spelsessie) SELECT spelsessie_id, username, score, rank FROM ranked_sessions WHERE spelsessie_id = %s;"
        params = [session_id]
        return Database.get_one_row(sql, params=params, settings=settings)
    
    @staticmethod
    def get_sessions_today(settings):
        sql = "SELECT spelsessie.spelsessie_id, username, moeilijkheid.naam, score, AVG(spelronde.reactietijd_ms) AS avg_reactietijd_ms, SUM(CASE WHEN spelronde.uitkomst = 'goed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS accuracy_percent FROM spelsessie INNER JOIN moeilijkheid ON spelsessie.moeilijkheid_id = moeilijkheid.moeilijkheid_id INNER JOIN spelronde ON spelsessie.spelsessie_id = spelronde.spelsessie_id WHERE DATE(spelsessie.gestart_op) = CURRENT_DATE GROUP BY spelsessie.spelsessie_id, username, moeilijkheid.naam, score"
        return Database.get_rows(sql, settings=settings)
    
    @staticmethod
    def get_sessions_thisweek(settings):
        sql = "SELECT spelsessie.spelsessie_id, username, moeilijkheid.naam, score, AVG(spelronde.reactietijd_ms) AS avg_reactietijd_ms, SUM(CASE WHEN spelronde.uitkomst = 'goed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS accuracy_percent FROM spelsessie INNER JOIN moeilijkheid ON spelsessie.moeilijkheid_id = moeilijkheid.moeilijkheid_id INNER JOIN spelronde ON spelsessie.spelsessie_id = spelronde.spelsessie_id WHERE DATE(spelsessie.gestart_op) >= DATE_SUB(CURRENT_DATE, INTERVAL 6 DAY) AND DATE(spelsessie.gestart_op) <= CURRENT_DATE GROUP BY spelsessie.spelsessie_id, username, moeilijkheid.naam, score"
        return Database.get_rows(sql, settings=settings)
    
    
    @staticmethod
    def get_sessions_thismonth(settings):
        sql = "SELECT spelsessie.spelsessie_id, username, moeilijkheid.naam, score, AVG(spelronde.reactietijd_ms) AS avg_reactietijd_ms, SUM(CASE WHEN spelronde.uitkomst = 'goed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS accuracy_percent FROM spelsessie INNER JOIN moeilijkheid ON spelsessie.moeilijkheid_id = moeilijkheid.moeilijkheid_id INNER JOIN spelronde ON spelsessie.spelsessie_id = spelronde.spelsessie_id WHERE DATE(spelsessie.gestart_op) >= DATE_FORMAT(CURRENT_DATE, '%Y-%m-01') AND DATE(spelsessie.gestart_op) <= CURRENT_DATE GROUP BY spelsessie.spelsessie_id, username, moeilijkheid.naam, score"
        return Database.get_rows(sql, settings=settings)
    
    @staticmethod
    def get_sessions_alltime(settings):
        sql = "SELECT spelsessie.spelsessie_id, username, moeilijkheid.naam, score, AVG(spelronde.reactietijd_ms) AS avg_reactietijd_ms, SUM(CASE WHEN spelronde.uitkomst = 'goed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS accuracy_percent FROM spelsessie INNER JOIN moeilijkheid ON spelsessie.moeilijkheid_id = moeilijkheid.moeilijkheid_id INNER JOIN spelronde ON spelsessie.spelsessie_id = spelronde.spelsessie_id GROUP BY spelsessie.spelsessie_id, username, moeilijkheid.naam, score"
        return Database.get_rows(sql, settings=settings)