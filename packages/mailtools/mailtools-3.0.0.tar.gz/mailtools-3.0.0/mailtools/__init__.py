"""
mailtools package.

Exports all symbols from ``mailtools.mailer``.
"""
__version__ = "3.0.0"

__all__ = (
    "CopyMessages",
    "Mailer",
    "RedirectMessages",
    "SMTPMailer",
    "SMTPTransport",
    "TestMailer",
    "ThreadedMailer",
)

from mailtools.mailer import (
    CopyMessages,
    Mailer,
    RedirectMessages,
    SMTPMailer,
    SMTPTransport,
)
from mailtools.threadedmailer import ThreadedMailer
