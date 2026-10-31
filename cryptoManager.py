"""
cryptoManager.py — ECDSA Assessment Integrity

Provides ECDSA digital signature operations for quiz result integrity.
Uses SECP256R1 (P-256) with SHA-256.

The private key signs finalized quiz data at creation time.
The public key verifies that stored quiz data has not been modified.

Security claim:
    ECDSA does not prevent an administrator from modifying MySQL.
    It allows the application to detect that the finalized assessment
    no longer matches the authenticated data.
"""

import os
import json
import base64

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


# Key file paths (stored in data/ directory, gitignored)
KEYS_DIR = os.path.join(os.path.dirname(__file__), "data")
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "private_key.pem")
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "public_key.pem")


def generate_keys():
    """
    Generate a new ECDSA P-256 key pair and save to PEM files.

    Creates:
        data/private_key.pem — private signing key (never in DB, never in Git)
        data/public_key.pem  — public verification key
    """
    os.makedirs(KEYS_DIR, exist_ok=True)

    private_key = ec.generate_private_key(ec.SECP256R1())

    # Save private key (unencrypted for this learning project)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(private_pem)

    # Save public key
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(public_pem)


def load_private_key():
    """Load the ECDSA private key from PEM file."""
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def load_public_key():
    """Load the ECDSA public key from PEM file."""
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def canonicalize_quiz(quiz_id, topic_id, score, total_questions,
                      accuracy, time_taken_seconds, completed_at):
    """
    Build deterministic bytes from quiz fields.

    The same quiz state always produces exactly the same bytes,
    ensuring that verification is consistent.

    Args:
        quiz_id:             int
        topic_id:            int
        score:               int
        total_questions:     int
        accuracy:            Decimal or float or str
        time_taken_seconds:  int or None
        completed_at:        datetime or str

    Returns:
        bytes — deterministic UTF-8 encoded JSON
    """
    # Convert types for deterministic JSON serialization
    # For completed_at: MySQL datetime truncates microseconds,
    # so we format to seconds precision to ensure sign-time
    # and verify-time produce identical bytes.
    if hasattr(completed_at, "strftime"):
        completed_at_str = completed_at.strftime("%Y-%m-%d %H:%M:%S")
    else:
        completed_at_str = str(completed_at)

    payload = {
        "quiz_id": int(quiz_id),
        "topic_id": int(topic_id),
        "score": int(score),
        "total_questions": int(total_questions),
        "accuracy": f"{float(accuracy):.2f}",
        "time_taken_seconds": (
            int(time_taken_seconds)
            if time_taken_seconds is not None
            else None
        ),
        "completed_at": completed_at_str
    }

    # Sorted keys ensure deterministic ordering
    canonical_json = json.dumps(payload, sort_keys=True)
    return canonical_json.encode("utf-8")


def sign_data(data_bytes):
    """
    Sign bytes with the ECDSA private key.

    Args:
        data_bytes: bytes to sign

    Returns:
        str — base64-encoded signature
    """
    private_key = load_private_key()

    signature = private_key.sign(
        data_bytes,
        ec.ECDSA(hashes.SHA256())
    )

    return base64.b64encode(signature).decode("ascii")


def verify_signature(data_bytes, signature_b64):
    """
    Verify an ECDSA signature against data using the public key.

    Args:
        data_bytes:    bytes — the canonical data
        signature_b64: str   — base64-encoded ECDSA signature

    Returns:
        True  if the signature is valid
        False if the data has been modified or the signature is invalid
    """
    public_key = load_public_key()

    try:
        signature = base64.b64decode(signature_b64)
        public_key.verify(
            signature,
            data_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except (InvalidSignature, Exception):
        return False
