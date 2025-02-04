from database.vector_store import VectorStore
from services.synthesizer import Synthesizer

# Initialize VectorStore
vec = VectorStore()

def process_question(relevant_question):
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
        final_string = "No matches found."
    
    response = Synthesizer.generate_response(question=relevant_question, context=final_string)
    generated_response = "".join(chunk.choices[0].delta.content or "" for chunk in response)
    print(generated_response)
    return final_string, generated_response
