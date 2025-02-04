from database.vector_store import VectorStore
from services.synthesizer import Synthesizer

vec = VectorStore()

# --------------------------------------------------------------
# clinical question
# --------------------------------------------------------------

relevant_question = "چند وقته گلوم خشکه و تنگیه نفس دارم اگر دود سیگار وارد ریم بشه به شدت سرف میکنم"
results = vec.search(relevant_question, limit=4)
if 'matches' in results:
    concatenated_strings = [
        match['metadata']['contents']
        .replace("Question:", "سوال بیمار:")
        .replace("Answer:", "جواب دکتر:").strip()
        for match in results['matches']
    ]
    
    final_string = "\n\n".join(concatenated_strings)
else:
    print("No matches found.")

response = Synthesizer.generate_response(question=relevant_question, context=final_string)
for chunk in response:
    print(chunk.choices[0].delta.content or "", end="")


