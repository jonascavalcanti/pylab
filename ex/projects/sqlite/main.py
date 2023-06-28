from services.db import SQLite


sql = SQLite("./hodor.db")
conn = sql.get_connection()

m = {
    "id": 2211596,
    "google_workspace_name": "tribe-people",
    "github_id": 1000,
    "github_slug": "tribe-people",
    "github_name": "tribe-people"
    }

print(m["id"])

sql.insert(conn, "groups", m)

