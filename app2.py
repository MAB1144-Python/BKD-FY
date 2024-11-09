import psycopg2



if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="postgres", user="user", password="Mab880821", host="127.0.0.1", port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""
        DO $$ DECLARE
        r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
            END LOOP;
        END $$;
    """)

    cur.close()
    conn.close()
