"""Module for extracting info from a web page and text summarization."""
import nltk
from newspaper import Article

from app.models import TextSummary


async def generate_summary(summary_id: int, url: str) -> None:
    """Parse a web page and retrieve a summary about it's content."""
    article = Article(url)
    article.download()
    article.parse()

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    finally:
        article.nlp()

    summary = article.summary
    await TextSummary.filter(id=summary_id).update(summary=summary)
