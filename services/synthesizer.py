from typing import List
import pandas as pd
from services.llm_factory import LLMFactory



class Synthesizer:
    """Synthesizes a response based on a question and the retrieved context."""
    
    SYSTEM_PROMPT = """تو به سوالات بیماران پاسخ می‌دهی. به موارد زیر توجه کن و به سوال کاربر پاسخ بده:
1. با توجه به سوالی که کاربر پرسیده، سوالات و جواب‌های مشابه برای تو فراهم می‌شود که باید با توجه به آن‌ها پاسخ بدهی.
2. از جواب دادن به سوالاتی که نامربوط به پزشکی یا بهداشت هستند، اجتناب کن و پاسخ نده.
3. اگر سوالات و جواب‌های مشابهی که در اختیارت قرار می‌گیرد به سوال کاربر نامربوط بود، پاسخ نده و بگو که این موضوع از توانایی‌های من خارج است.
4. اگر سوال بیمار ربطی به سوال و جواب های پیدا شده نداشت اون رو در جریان قرار بده و بگو که اطلاعات مشابهی پیدا شد یا اطلاعات مشابه کمی پیدا شد
5. اگر کسی در مورد هویتت ازت سوال پرسید با اینکه اطلاعات مشابهی دریافت نکردی به او پاسخ بده، تو یه دستیار سوالات بالینی هستی که به مردم کمک میکنی"""

    @staticmethod
    def generate_response(question: str, context: str) -> any:
        """
        Generates a synthesized response based on the question and context.

        Args:
            question (str): The user's question.
            context (pd.DataFrame): The relevant context retrieved from the knowledge base.

        Returns:
            SynthesizedResponse: A Pydantic model with the thought process and final answer.
        """

        messages = [
    {"role": "system", "content": Synthesizer.SYSTEM_PROMPT},
    {
        "role": "user",
        "content": (
            f"سوال کاربر:\n{question}\n\n"
            f"اطلاعات زیر شامل سوالات و پاسخ‌های مرتبط است. "
            f"از این اطلاعات برای ارائه یک پاسخ جدید و جامع به سوال استفاده کنید. "
            f"پاسخ شما نباید به صورت مستقیم از متن کپی شود، بلکه باید بر اساس تحلیل اطلاعات باشد:\n\n"
            f"{context}"
        )
    }
]
        llm_factory = LLMFactory() 
        return llm_factory.create_completion(
            messages=messages,
            stream=False
        )

    @staticmethod
    def dataframe_to_json(
        context: pd.DataFrame,
        columns_to_keep: List[str],
    ) -> str:
        """
        Convert the context DataFrame to a JSON string.

        Args:
            context (pd.DataFrame): The context DataFrame.
            columns_to_keep (List[str]): The columns to include in the output.

        Returns:
            str: A JSON string representation of the selected columns.
        """
        return context[columns_to_keep].to_json(orient="records", indent=2)
