"""ORM models for summarizer app."""
from tortoise import fields, models


class TextSummary(models.Model):
    """Summary for a web page."""
    id = fields.IntField(pk=True)  # noqa: VNE003
    url = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.url
