import sqlite3

db = sqlite3.connect(r"D:\Claude Code\gas-survey\data\survey.db")
db.execute("DELETE FROM attachments")
db.execute("DELETE FROM iso_documents")
db.execute("DELETE FROM submissions")
db.execute("DELETE FROM sqlite_sequence WHERE name IN ('submissions', 'attachments', 'iso_documents')")
db.commit()
print("db cleared")
