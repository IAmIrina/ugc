
REPORT = """
    {database} ({record_count} records)
    Read threads: {read_threads}
    Write threads: {write_threads}
    ----------------------------------------------------------------------------
    | Read all movies watched by user          | {user_movies} |
    | Read 10 last watched movies by user      | {last_user_movies} |
    | Read 10 the most popular movies          | {popular} |
    | Read last watched movies                 | {last_watched}|
    ----------------------------------------------------------------------------
    | Write record                             | {write_time}|
    ----------------------------------------------------------------------------

    """
