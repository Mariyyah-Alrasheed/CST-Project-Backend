from datetime import date
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="StopRequestsDatabase",
    user="postgres",
    password="Ma_ria111",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# قائمة IDs المسموح بها
employee_ids = [
    1, 2, 7, 9, 10, 11, 12, 13, 14, 15,
    16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
    26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
    36, 37, 38
]

# ربطهم بمزودي الخدمة (نفترض أن لدينا فقط 3 مزودي خدمة: 1، 2، 3)
data = []
providers = [ 2, 3,4,5,6,7]
provider_index = 0

for emp_id in employee_ids:
    provider_id = providers[provider_index % len(providers)]
    data.append((emp_id, provider_id, date.today()))
    provider_index += 1

# تنفيذ الإدخال
query = """
INSERT INTO employee_service_provider (employee_id, provider_id, assigned_at)
VALUES (%s, %s, %s)
"""

cur.executemany(query, data)
conn.commit()

print("✅ تم إدخال بيانات الربط بنجاح.")
cur.close()
conn.close()