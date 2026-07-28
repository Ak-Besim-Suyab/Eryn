import sqlite3
conn = sqlite3.connect(r'c:\Eryn\generic.db')
cur = conn.cursor()
cur.execute("PRAGMA table_info('Statistic')")
print(cur.fetchall())
conn.close()
