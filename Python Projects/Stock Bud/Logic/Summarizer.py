# summarizer.py
#YOU NEED AN OPENAI API KEY FOR THIS TO WORK
# This script uses OpenAI's GPT-3.5 Turbo model to analyze news articles and generate insights.
import os
import openai
from openai import OpenAI
from transformers import pipeline
from Logic import NewsExtractor

class NewsInsights:
    def __init__(
        self,
        openai_api_key=None,
        summary_model="sshleifer/distilbart-cnn-12-6",
        insight_model="google/flan-t5-large",
        chat_model="gpt-3.5-turbo"
    ):
        key = openai_api_key 
        # or os.getenv("OPENAI_API_KEY")
        
        if key:
            self.client = OpenAI(api_key=key)
        else:
            self.client = None

        self.summarizer = pipeline(
            "summarization", model=summary_model, tokenizer=summary_model, device="cpu"
        )
        self.insighter = pipeline(
            "text2text-generation", model=insight_model, tokenizer=insight_model, device="cpu"
        )
        self.chat_model = chat_model

    def summarize(self, text, max_length=60, min_length=25):
        if not text:
            return ""
        out = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return out[0]["summary_text"]

    def _analyze_with_openai(self, text, max_tokens=500):
        prompt = (
            "You are a seasoned financial analyst. Read the news article below and produce a Markdown report\n"
            "with sections: ## Summary, ## Economic Impact, ## Affected Stocks & Industries, ## Historical Context\n\n"
            f"Article:\n\"\"\"\n{text}\n\"\"\""
        )
        resp = self.client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": "You are a helpful financial analyst."},
                {"role": "user",   "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()

    def analyze_economy(self, text):
        # Try OpenAI first, then fallback on local HF if quota/rate‑limit is hit
        if self.client:
            try:
                return self._analyze_with_openai(text)
            except openai.RateLimitError:
                print("⚠️ OpenAI rate‑limit or quota error – falling back to local insights.")
        # Local Hugging Face fallback
        prompt = (
            "Read the following news article and produce a report in Markdown with these sections:\n"
            "## Summary\nA one‑sentence summary(Break down techincal terms down).\n\n"
            "## Economic Impact\nHow this will affect the broader economy.(Talk about stock increases, give numbers)\n\n"
            "## Affected Stocks & Industries\nWhich stocks or sectors will move.\n\n"
            "## Historical Context\nRelevant past events or trends.\n\n"
            f"Article:\n\"\"\"\n{text}\n\"\"\""
        )
        out = self.insighter(prompt, max_length=256, do_sample=False)
        return out[0]["generated_text"]

if __name__ == "__main__":
    print("\n" + "="*80 + "\n")
    extractor = NewsExtractor()
    article = extractor.extractNews("https://www.cnn.com/2025/04/16/investing/us-stock-market/index.html")
    insights = NewsInsights()
    print(insights.analyze_economy(article.data))
    print("\n" + "="*80 + "\n")
    # for news in articles:
    #     print(f"# {news.get_title()}\n")
    #     print(insights.analyze_economy(news.data))
    #     print("\n" + "="*80 + "\n")
#`pip install huggingface_hub[hf_xet]` or `pip install hf_xet`