import json
from datetime import datetime
from sqlalchemy import Column, Date, String, func
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.dialects.postgresql as postgresql
from fixerapp import db


class CurrencyInformation(db.Model):
    __tablename__ = 'currency_information'
    base_currency = Column(String(3), nullable=False, primary_key=True)
    changes = Column(postgresql.JSONB, nullable=False)
    change_date = Column(Date, nullable=False)
    retrieved_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, primary_key=True)
    created_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    @classmethod
    def latest_rates(cls, base, date = datetime.now().date()):
        return cls.query.order_by(
            cls.retrieved_at.desc()
        ).filter_by(
            base_currency = base,
            change_date = date
        ).first()

    def __repr__(self):
        return f'<{self.base_currency}> <date>{self.change_date}'

    def to_json(self):
        return json.dumps(
            {
                'base_currency': self.base_currency,
                'changes': self.changes,
                'change_date': self.change_date.strftime('%Y-%m-%d'),
                'retrieved_at': int(self.retrieved_at.timestamp()),
                'created_at': int(self.created_at.timestamp())
            }
        )

