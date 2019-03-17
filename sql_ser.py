import pyodbc


conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=server_name;"
                        "Database=db_name;"
                        "uid=User")

cursor = conn.cursor()
sql = "SELECT * FROM rainfall.dbo.details;"
cursor.execute(sql)