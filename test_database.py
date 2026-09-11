from database import execute_query

execute_query(
    "INSERT INTO subjects (name) VALUES (%s)",
    ("Test Subject",)
)

print("Query executed successfully!")