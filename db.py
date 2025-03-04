import mysql.connector
import json
import os

class Database:
    def __init__(self):
        self.read_conn = mysql.connector.connect(
            host="ich-db.edu.itcareerhub.de",
            user="ich1",
            password="password",
            database="sakila"
        )
        self.read_cursor = self.read_conn.cursor(dictionary=True)

        self.write_conn = mysql.connector.connect(
            host="ich-edit.edu.itcareerhub.de",
            user="ich1",
            password="ich1_password_ilovedbs",
            database="ich_edit"
        )
        self.write_cursor = self.write_conn.cursor(dictionary=True)

    def search_by_keyword(self, keyword):
        cache = self.load_cache()
        if keyword in cache:
            return cache[keyword]

        query = """
        SELECT film_id, title, description, release_year 
        FROM film 
        WHERE title LIKE %s OR description LIKE %s 
        LIMIT 10;
        """
        self.read_cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        results = self.read_cursor.fetchall()

        self.save_cache(keyword, results)
        return results

    def search_by_genre_year(self, genre, year):
        cache_key = f"{genre}_{year}"
        cache = self.load_cache()
        if cache_key in cache:
            return cache[cache_key]

        query = """
        SELECT f.film_id, f.title, f.release_year, c.name AS genre 
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE c.name = %s AND f.release_year = %s
        LIMIT 10;
        """
        self.read_cursor.execute(query, (genre, year))
        results = self.read_cursor.fetchall()

        self.save_cache(cache_key, results)
        return results

    def save_query(self, query_text):
        query = """
        INSERT INTO queries_search_movies (query_text) 
        VALUES (%s);
        """
        self.write_cursor.execute(query, (query_text,))
        self.write_conn.commit()

    def get_popular_queries(self):
        query = """
        SELECT query_text, COUNT(*) AS search_count 
        FROM queries_search_movies 
        GROUP BY query_text 
        ORDER BY search_count DESC 
        LIMIT 10;
        """

        self.write_cursor.execute(query)
        return self.write_cursor.fetchall()

    def save_cache(self, key, value):
        cache = self.load_cache()
        cache[key] = value
        with open("cache.json", "w") as f:
            json.dump(cache, f)

    def load_cache(self):
        if os.path.exists("cache.json"):
            with open("cache.json", "r") as f:
                return json.load(f)
        return {}

    def close(self):
        self.read_cursor.close()
        self.read_conn.close()
        self.write_cursor.close()
        self.write_conn.close()
