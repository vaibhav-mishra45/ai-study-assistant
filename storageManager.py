import json
from database import execute_query, fetch_all, fetch_one
from rich import print
from rich.table import Table

def get_subject_by_name(name):
    query = """
        SELECT id, name
        FROM subjects
        WHERE LOWER(name) = LOWER(%s)
    """

    subjects = fetch_all(query, (name,))
    return subjects[0] if subjects else None

def get_subjects():
    query = """
        SELECT id, name
        FROM subjects
        ORDER BY id
    """
    return fetch_all(query)


def save_subject(name):
    query = """
        INSERT INTO subjects (name)
        VALUES (%s)
    """
    execute_query(query, (name,))


def delete_subject(name):
    query = """
        DELETE FROM subjects
        WHERE name = %s
    """
    execute_query(query, (name,))


def rename(old_name, new_name):
    subject = fetch_all(
        """
        SELECT id, name
        FROM subjects
        WHERE LOWER(name) = LOWER(%s)
        """,
        (old_name,)
    )

    if not subject:
        return False

    existing = fetch_all(
        """
        SELECT id
        FROM subjects
        WHERE LOWER(name) = LOWER(%s)
        """,
        (new_name,)
    )

    if existing:
        return False

    execute_query(
        """
        UPDATE subjects
        SET name = %s
        WHERE id = %s
        """,
        (new_name, subject[0]["id"])
    )

    return True

def get_topic_by_name(subject_id, name):
    query = """
        SELECT id, subject_id, name
        FROM topics
        WHERE subject_id = %s
          AND LOWER(name) = LOWER(%s)
    """

    topics = fetch_all(query, (subject_id, name))
    return topics[0] if topics else None

def get_topics(subject_id):
    query = """
        SELECT id, name
        FROM topics
        WHERE subject_id = %s
        ORDER BY id
    """

    return fetch_all(query, (subject_id,))


def save_topic(subject_id, name):
    query = """
        INSERT INTO topics (subject_id, name)
        VALUES (%s, %s)
    """

    execute_query(query, (subject_id, name))


def delete_topic(topic_id):
    query = """
        DELETE FROM topics
        WHERE id = %s
    """

    execute_query(query, (topic_id,))


def rename_topic(subject_id, old_topic_name, new_topic_name):
    topic = fetch_all(
        """
        SELECT id, name
        FROM topics
        WHERE subject_id = %s
          AND LOWER(name) = LOWER(%s)
        """,
        (subject_id, old_topic_name)
    )

    if not topic:
        return False

    existing = fetch_all(
        """
        SELECT id
        FROM topics
        WHERE subject_id = %s
          AND LOWER(name) = LOWER(%s)
        """,
        (subject_id, new_topic_name)
    )

    if existing:
        return False

    execute_query(
        """
        UPDATE topics
        SET name = %s
        WHERE id = %s
        """,
        (new_topic_name, topic[0]["id"])
    )

    return True


def save_note(topic_id, content):
    query = """
        INSERT INTO notes (topic_id, content)
        VALUES (%s, %s)
    """

    execute_query(query, (topic_id, content))


def update_note(topic_id, content):
    query = """
        UPDATE notes
        SET content = %s
        WHERE topic_id = %s
    """

    execute_query(query, (content, topic_id))

def delete_note(topic_id):
    query = """
        DELETE FROM notes
        WHERE topic_id = %s
    """

    execute_query(query, (topic_id,))


def get_note(topic_id):
    query = """
        SELECT id, topic_id, content
        FROM notes
        WHERE topic_id = %s
    """

    notes = fetch_all(query, (topic_id,))

    return notes[0] if notes else None

def save_study_session(topic_id, start_time, end_time, duration_minutes):
    query = """
        INSERT INTO study_sessions
        (topic_id, start_time, end_time, duration_minutes)
        VALUES (%s, %s, %s, %s)
    """
    execute_query(
        query,
        (topic_id, start_time, end_time, duration_minutes)
    )

def save_quiz(
    topic_id,
    score,
    total_questions,
    accuracy,
    time_taken_seconds,
    completed_at,
    signature=None
):
    query = """
        INSERT INTO quizzes
        (
            topic_id,
            score,
            total_questions,
            accuracy,
            time_taken_seconds,
            completed_at,
            signature
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    execute_query(
        query,
        (
            topic_id,
            score,
            total_questions,
            accuracy,
            time_taken_seconds,
            completed_at,
            signature
        )
    )

def search_topics(topic_name):
    query = """
        SELECT
            topics.id,
            topics.name AS topic_name,
            subjects.name AS subject_name,
            CASE
                WHEN notes.id IS NOT NULL THEN 'Yes'
                ELSE 'No'
            END AS notes_available
        FROM topics
        JOIN subjects
            ON topics.subject_id = subjects.id
        LEFT JOIN notes
            ON topics.id = notes.topic_id
        WHERE LOWER(topics.name) = LOWER(%s)
    """
    return fetch_all(query, (topic_name,))

def search_notes(keyword):
    query = """
        SELECT
            subjects.name AS subject_name,
            topics.name AS topic_name
        FROM notes
        JOIN topics
            ON notes.topic_id = topics.id
        JOIN subjects
            ON topics.subject_id = subjects.id
        WHERE LOWER(notes.content) LIKE LOWER(%s)
    """
    return fetch_all(query, (f"%{keyword}%",))


def get_study_report_data():
    query = """
        SELECT
            study_sessions.duration_minutes,
            subjects.name AS subject_name,
            topics.name AS topic_name
        FROM study_sessions
        JOIN topics
            ON study_sessions.topic_id = topics.id
        JOIN subjects
            ON topics.subject_id = subjects.id
        ORDER BY study_sessions.id
    """
    return fetch_all(query)

def get_quiz_report_data():
    query = """
        SELECT
            quizzes.score,
            quizzes.total_questions,
            quizzes.accuracy,
            topics.name AS topic_name
        FROM quizzes
        JOIN topics
            ON quizzes.topic_id = topics.id
        ORDER BY quizzes.id
    """
    return fetch_all(query)


def get_quiz_by_id(quiz_id):
    query = """
        SELECT
            id,
            topic_id,
            score,
            total_questions,
            accuracy,
            time_taken_seconds,
            completed_at,
            signature
        FROM quizzes
        WHERE id = %s
    """
    return fetch_one(query, (quiz_id,))


def verify_quiz_integrity(quiz_id):
    """Verify the ECDSA signature of a finalized quiz result.

    Returns:
        dict with 'status' key:
            'not_found' — quiz ID does not exist
            'unsigned'  — quiz exists but has no signature
            'valid'     — signature matches current quiz data
            'tampered'  — signature does NOT match current quiz data
    """
    from cryptoManager import canonicalize_quiz, verify_signature

    quiz = get_quiz_by_id(quiz_id)

    if not quiz:
        return {"status": "not_found"}

    if not quiz["signature"]:
        return {"status": "unsigned"}

    canonical_bytes = canonicalize_quiz(
        quiz_id=quiz["id"],
        topic_id=quiz["topic_id"],
        score=quiz["score"],
        total_questions=quiz["total_questions"],
        accuracy=quiz["accuracy"],
        time_taken_seconds=quiz["time_taken_seconds"],
        completed_at=quiz["completed_at"]
    )

    is_valid = verify_signature(canonical_bytes, quiz["signature"])

    if is_valid:
        return {"status": "valid"}
    else:
        return {"status": "tampered"}


def get_recent_quizzes(limit=10):
    query = """
        SELECT
            id,
            topic_id,
            score,
            total_questions,
            accuracy,
            time_taken_seconds,
            completed_at,
            signature
        FROM quizzes
        ORDER BY completed_at DESC, id DESC
        LIMIT %s
    """
    return fetch_all(query, (limit,))


def get_all_signed_quizzes():
    query = """
        SELECT
            id,
            topic_id,
            score,
            total_questions,
            accuracy,
            time_taken_seconds,
            completed_at,
            signature
        FROM quizzes
        WHERE signature IS NOT NULL
        ORDER BY completed_at DESC, id DESC
    """
    return fetch_all(query)