import psycopg2
import environs

env = environs.Env()
env.read_env()

try:
    connection = psycopg2.connect(user = env('POSTGRES_USER'),
                                  password = env('POSTGRES_PASSWORD'),
                                  host = env('POSTGRES_SERVER'),
                                  port = env('POSTGRES_PORT'),
                                  database = env('DBNAME'))
    print(connection)

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

except psycopg2.Error as error :
    print("Error while connecting to PostgreSQL")
    print(error)
finally:
    #closing database connection.
    print('done')
