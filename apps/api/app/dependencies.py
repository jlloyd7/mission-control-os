"""Request context (dev-auth stub).

P0 resolves a single dev org + user. # TODO(P1): real auth (JWT/Clerk/etc.).
"""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models
from .config import get_settings
from .db import get_db

settings = get_settings()


@dataclass
class RequestContext:
    db: Session
    org: models.Organization
    user: models.User

    @property
    def org_id(self) -> str:
        return self.org.id

    @property
    def user_id(self) -> str:
        return self.user.id


def get_context(db: Session = Depends(get_db)) -> RequestContext:
    org = db.scalar(select(models.Organization).filter_by(slug="mission-control-dev"))
    if org is None:
        org = models.Organization(name=settings.dev_org_name, slug="mission-control-dev")
        db.add(org)
        db.flush()
    user = db.scalar(select(models.User).filter_by(email=settings.dev_user_email))
    if user is None:
        user = models.User(
            organization_id=org.id,
            email=settings.dev_user_email,
            display_name="George Dev",
            role="owner",
        )
        db.add(user)
        db.flush()
    db.commit()
    return RequestContext(db=db, org=org, user=user)
