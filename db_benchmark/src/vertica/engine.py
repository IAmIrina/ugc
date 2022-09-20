import vertica_python

connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}


with vertica_python.connect(**connection_info) as connection:  # 1
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE  IF NOT EXISTS views (
        event_time TIMESTAMP NOT NULL,
        user_id UUID NOT NULL,
        movie_id VARCHAR(256) NOT NULL,
        viewed_frame INTEGER NOT NULL
    );
    """)

    cursor.execute("""INSERT INTO views (event_time, user_id, movie_id, viewed_frame) VALUES (
        TO_TIMESTAMP(1546300800),
        '61f0c404-5cb3-11e7-907b-a6006ad3dba0',
        'tt0120338',
        1611902873
    );
    """)

    cursor.execute("""
        SELECT * FROM views;
    """)
    for row in cursor.iterate():
        print(row)
