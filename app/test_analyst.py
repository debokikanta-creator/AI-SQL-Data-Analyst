
from data_analyst import analyze_question

question = "What is the total revenue?"

try:
    sql, results = analyze_question(question)

    print("\n" + "=" * 50)
    print("AI SQL DATA ANALYST RESULTS")
    print("=" * 50)

    print("\nQuestion:")
    print(question)

    print("\nSQL Query:")
    print(sql)

    print("\nActual Database Results:")
    print(results.to_string(index=False))

    print("\nNumber of rows:", len(results))

except Exception as error:
    print("\nERROR:")
    print(type(error).__name__, str(error))
