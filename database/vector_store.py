import logging
import time
from typing import Any, List, Tuple, Union

import torch
import pandas as pd
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
from config.settings import get_settings
from pinecone import Pinecone

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")
host = os.getenv("PINECONE_HOST")
pc = Pinecone(api_key=api_key)



class VectorStore:
    def __init__(self):
        self.settings = get_settings()
        self.index = pc.Index(host=host) 
        self.tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-base')
        self.model = AutoModel.from_pretrained('intfloat/multilingual-e5-base')

    def average_pool(self, last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

    def get_embedding(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        input_text = f"query: {text}"
        batch_dict = self.tokenizer(input_text, max_length=512, padding=True, truncation=True, return_tensors='pt')

        start_time = time.time()
        with torch.no_grad():
            outputs = self.model(**batch_dict)
            embeddings = self.average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])

        normalized_embeddings = F.normalize(embeddings, p=2, dim=1)
        elapsed_time = time.time() - start_time
        return normalized_embeddings.squeeze().tolist()


    def upsert(self, df: pd.DataFrame) -> None:
        ids = df['id'].tolist()
        embeddings = df['embedding'].tolist()
        metadata = df['metadata'].tolist()
        data = [{"id": id_, "values": embedding, "metadata": meta} for id_, embedding, meta in zip(ids, embeddings, metadata)]
        
        self.index.upsert(data)
        print(f'Inserted {len(df)} rows')

    def search(self, query_text: str, limit: int = 5, metadata_filter: Union[dict, List[dict]] = None, return_dataframe: bool = False) -> Union[List[Tuple[Any, ...]], pd.DataFrame]:
        query_embedding = self.get_embedding(query_text)

        start_time = time.time()

        search_args = {
            "top_k": limit,
            "include_metadata": True
        }

        if metadata_filter:
            search_args["filter"] = metadata_filter

        results = self.index.query(vector=query_embedding, **search_args)

        elapsed_time = time.time() - start_time
        logging.info(f"Vector search completed in {elapsed_time:.3f} seconds")

        if return_dataframe:
            return self._create_dataframe_from_results(results)
        else:
            return results

    def _create_dataframe_from_results(self, results) -> pd.DataFrame:
        data = []
        for match in results['matches']:
            data.append({
                'id': match['id'],
                'score': match['score'],
                'metadata': match.get('metadata', {})
            })
        return pd.DataFrame(data)


    def _create_dataframe_from_results(
        self,
        results: List[Tuple[Any, ...]],
    ) -> pd.DataFrame:
        """
        Create a pandas DataFrame from the search results.

        Args:
            results: A list of tuples containing the search results.

        Returns:
            A pandas DataFrame containing the formatted search results.
        """
        # Convert results to DataFrame
        df = pd.DataFrame(
            results, columns=["id", "metadata", "content", "embedding", "distance"]
        )

        # Expand metadata column
        df = pd.concat(
            [df.drop(["metadata"], axis=1), df["metadata"].apply(pd.Series)], axis=1
        )

        # Convert id to string for better readability
        df["id"] = df["id"].astype(str)

        return df
