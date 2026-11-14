
from sql_generator import generate_sql
from sql_validator import validate_sql

question = "What is the total revenue?"

print("Question:", question)

sql = generate_sql(question)

print("\nGenerated SQL:")
print(sql)

try:
    validate_sql(sql)
    print("\nSQL VALIDATION SUCCESSFUL!")

except ValueError as error:
    print("\nSQL VALIDATION FAILED:")
    print(error)
