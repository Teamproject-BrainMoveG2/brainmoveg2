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
        # Corrected for older MySQL: Use subquery instead of RANK()
        sql = "SELECT username, score, (SELECT COUNT(*) + 1 FROM spelsessie s2 WHERE s2.spelmodus_id = s1.spelmodus_id AND s2.score > s1.score) AS `rank` FROM spelsessie s1 WHERE spelmodus_id = %s ORDER BY score DESC LIMIT %s"
        params = [mode_id, limit]
        return Database.get_rows(sql, params=params, settings=settings)
    
    @staticmethod
    def get_player_rank(settings, session_id, mode_id):
        # Corrected for older MySQL: Use subquery instead of CTE and RANK()
        sql = "SELECT spelsessie_id, username, score, (SELECT COUNT(*) + 1 FROM spelsessie s2 WHERE s2.spelmodus_id = s1.spelmodus_id AND s2.score > s1.score) AS `rank` FROM spelsessie s1 WHERE spelsessie_id = %s AND spelmodus_id = %s"
        params = [session_id, mode_id]
        return Database.get_one_row(sql, params=params, settings=settings)
    
    @staticmethod
    def get_sessions_today(settings):
        sql = "SELECT spelsessie.spelsessie_id, username, spelsessie.spelmodus_id, moeilijkheid.naam, score, CAST(AVG(spelronde.reactietijd_ms) AS DECIMAL(10,2)) AS avg_reactietijd_ms, ROUND(SUM(CASE WHEN spelronde.uitkomst = 'goed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS accuracy_percent FROM spelsessie LEFT JOIN moeilijkheid ON spelsessie.moeilijkheid_id = moeilijkheid.moeilijkheid_id INNER JOIN spelronde ON spelsessie.spelsessie_id = spelronde.spelsessie_id WHERE DATE(spelsessie.gestart_op) = CURRENT_DATE GROUP BY spelsessie.spelsessie_id, username, spelsessie.spelmodus_id, moeilijkheid.naam, score"
        return Database.get_rows(sql, settings=settings)
    
    @staticmethod
    def get_sessions_thisweek(settings):
        sql = "SELECT spelsessie.spelsessie_id, username, spelsessie.spelmodus_id, moeilijkheid.naam, score, AVG(spelronde.reactietijd_ms) AS avg_reactietijd_ms, SUM(CASE WHEN spelronde.uitkomst = 'goed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS accuracy_percent FROM spelsessie LEFT JOIN moeilijkheid ON spelsessie.moeilijkheid_id = moeilijkheid.moeilijkheid_id INNER JOIN spelronde ON spelsessie.spelsessie_id = spelronde.spelsessie_id WHERE DATE(spelsessie.gestart_op) >= DATE_SUB(CURRENT_DATE, INTERVAL 6 DAY) AND DATE(spelsessie.gestart_op) <= CURRENT_DATE GROUP BY spelsessie.spelsessie_id, username, spelsessie.spelmodus_id, moeilijkheid.naam, score"
        return Database.get_rows(sql, settings=settings)
    
    
    @staticmethod
    def get_sessions_thismonth(settings):
        sql = "SELECT spelsessie.spelsessie_id, username, spelsessie.spelmodus_id, moeilijkheid.naam, score, AVG(spelronde.reactietijd_ms) AS avg_reactietijd_ms, SUM(CASE WHEN spelronde.uitkomst = 'goed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS accuracy_percent FROM spelsessie LEFT JOIN moeilijkheid ON spelsessie.moeilijkheid_id = moeilijkheid.moeilijkheid_id INNER JOIN spelronde ON spelsessie.spelsessie_id = spelronde.spelsessie_id WHERE DATE(spelsessie.gestart_op) >= DATE_FORMAT(CURRENT_DATE, '%Y-%m-01') AND DATE(spelsessie.gestart_op) <= CURRENT_DATE GROUP BY spelsessie.spelsessie_id, username, spelsessie.spelmodus_id, moeilijkheid.naam, score"
        return Database.get_rows(sql, settings=settings)
    
    @staticmethod
    def get_sessions_alltime(settings):
        sql = "SELECT spelsessie.spelsessie_id, username, spelsessie.spelmodus_id, moeilijkheid.naam, score, AVG(spelronde.reactietijd_ms) AS avg_reactietijd_ms, SUM(CASE WHEN spelronde.uitkomst = 'goed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS accuracy_percent FROM spelsessie LEFT JOIN moeilijkheid ON spelsessie.moeilijkheid_id = moeilijkheid.moeilijkheid_id INNER JOIN spelronde ON spelsessie.spelsessie_id = spelronde.spelsessie_id GROUP BY spelsessie.spelsessie_id, username, spelsessie.spelmodus_id, moeilijkheid.naam, score"
        return Database.get_rows(sql, settings=settings)
    
    @staticmethod
    def get_sessions_in_date_range(settings, start_date, end_date):
        sql = "SELECT spelsessie.spelsessie_id, username, spelsessie.spelmodus_id, moeilijkheid.naam, score, AVG(spelronde.reactietijd_ms) AS avg_reactietijd_ms, SUM(CASE WHEN spelronde.uitkomst = 'goed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS accuracy_percent, gestart_op as datum FROM spelsessie INNER JOIN moeilijkheid ON spelsessie.moeilijkheid_id = moeilijkheid.moeilijkheid_id INNER JOIN spelronde ON spelsessie.spelsessie_id = spelronde.spelsessie_id WHERE DATE(spelsessie.gestart_op) BETWEEN %s AND %s GROUP BY spelsessie.spelsessie_id, username, spelsessie.spelmodus_id, moeilijkheid.naam, score"
        params = [start_date, end_date]
        return Database.get_rows(sql, params=params, settings=settings)