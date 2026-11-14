
from schema_inspector import get_database_schema

print("=" * 45)
print("AUTOMATIC DATABASE SCHEMA DETECTION")
print("=" * 45)

schema = get_database_schema()

print(schema)

print("\nSCHEMA DETECTION SUCCESSFUL!")
