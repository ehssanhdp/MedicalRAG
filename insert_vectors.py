from datetime import datetime
import pandas as pd
from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time



# Initialize VectorStore
vec = VectorStore()

# Read the data
df = pd.read_json(
    "", 
    orient="records",
    lines=True
)

# Prepare data for insertion
def prepare_record(row):
    question = row["questionBody"]
    answer = row["answers"][0]["answer"] if row["answers"] else "No answer provided"
    print(question)
    print(answer)
    content = f"Question: {question}\nAnswer: {answer}"

    embedding = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "category": row["category"],
                "contents": content,
                "age": row["age"],
                "sex": row["sex"],
            },
            "embedding": embedding,
        }
    )

records_df = df.apply(prepare_record, axis=1)
vec.upsert(records_df)