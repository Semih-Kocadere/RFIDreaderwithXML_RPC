from xmlrpc.server import SimpleXMLRPCServer
import psycopg2

def is_person_exists(rfid_id,current_date_time):
    connection = psycopg2.connect(dbname='employee',
        user='',
        password='1234',
        host='',
        port=''
    )
    cursor = connection.cursor()
    #Execute a SQL query
    cursor.execute("SELECT * FROM rfid_data WHERE rfid_id = %s", (rfid_id,))
    #Fetch the row of the query result
    result = cursor.fetchone()

    cursor.close()
    connection.close()
    if result:
        name = result[1] # Assume name is in the 2.column
        return name
    else:
        return "Unknown RFID ID"

#Listens the port 8000
server = SimpleXMLRPCServer(("0.0.0.0", 8000))
#This method is used to register a function that can be called remotely via XML-RPC.
server.register_function(is_person_exists, "is_person_exists")

# Run the server
server.serve_forever()
