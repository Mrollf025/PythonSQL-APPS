import psycopg2
import pandas as p

class SQL:
    def __init__(self):
        pass

    def connect(self):
        return psycopg2.connect(
            dbname="GAMES",
            user="postgres",
            password="7354",
            host="localhost",
            port="5432"
        )

    def list_consoles(self):
        try:
            conn = self.connect()
            cur= conn.cursor()

            cur.execute("""
                SELECT c.console_id, c.console_name, c.release_year, co.company_name
                FROM consoles c
                JOIN company co ON c.company_id = co.company_id
                ORDER BY c.console_name ASC
            """)
            consoles = cur.fetchall()
            print("\n--- Console List ---")
            for console in consoles:
                print(f"[{console[0]}] {console[1]} ({console[2]}) - {console[3]}")

            cur.close()
            conn.close()
            return consoles
        except Exception as e:
            print("Error:", e)
            return[]

    def list_genres(self):
        try:
            conn = self.connect()
            cur= conn.cursor()

            cur.execute("""
                SELECT * FROM genres ORDER BY genre_name ASC
            """)
            genres = cur.fetchall()
            print("\n--- Genres ---")
            for genre in genres:
                print(f"[{genre[0]}] {genre[1]}")

            cur.close()
            conn.close()
            return genres
        except Exception as e:
            print("Error:", e)
            return [] 

    def list_company(self):
        try:
            conn = self.connect()
            cur= conn.cursor()

            cur.execute("""
                SELECT * FROM company ORDER BY company_name ASC
            """)
            company = cur.fetchall()
            print("\n--- Company ---")
            for comp in company:
                print(f"[{comp[0]}] {comp[1]} {comp[2]}")

            cur.close()
            conn.close()
            return company
        
        except Exception as e:
            print("Error:", e)
            return []


    def list_region(self):
        try:
            conn = self.connect()
            cur= conn.cursor()

            cur.execute("""
                SELECT * FROM region ORDER BY region_name ASC
            """)
            region = cur.fetchall()
            print("\n--- Region ---")
            for reg in region:
                print(f"[{reg[0]}] {reg[1]} {reg[2]}")

            cur.close()
            conn.close()
            return region
        except Exception as e:
            print("Error:", e)
            return []

    def list_games(self):
        try:
            conn = self.connect()
            cur= conn.cursor()

            cur.execute("""
                SELECT * FROM games
            """)
            games = cur.fetchall()
            print("\n--- Games ---")
            for game in games:
                print(
                    f"[{game[0]}] {game[1]} {game[2]} {game[3]} {game[4]} "
                    f"{game[5]} {game[6]} {game[7]} {game[8]}"
                     )

            cur.close()
            conn.close()
            return games
        
        except Exception as e:
            print("Error:", e)
            return []
        

    def insert_game(self, title, genre_id, console_id, publisher_id, region_id, year, played):
        try:
            conn = self.connect()
            cur = conn.cursor()
        
            query=("""
                    INSERT INTO public.games(
	                name, played, genre_id, console_id, 
                    publisher_id, year_published, region_id)
	                VALUES (%s, %s, %s, %s, %s, %s,%s);
                    """)
            params = (title, played, genre_id, console_id, publisher_id, year, region_id)
            cur.execute(query, params)
            conn.commit()
            cur.close()
            conn.close()
            print("Game Inserted Successfully")

        except Exception as e:
            print("Error inserting game:",e)
            pass


    # Run the function
if __name__ == "__main__":
    app = SQL()
    app.list_games()