"""
Django views for the AI Study Assistant web application.
Each view corresponds to a CLI feature from the original project.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, Count, Avg, Max, Min
from datetime import datetime

from .models import Subject, Topic, Note, StudySession, Quiz
from .ai_service import (
    resolve_doubt,
    generate_quiz,
    save_quiz_result,
    summarize_note,
    generate_study_plan,
    QUIZ_SIZE,
)
from storageManager import verify_quiz_integrity


# ─── Dashboard ───────────────────────────────────────────────────────

def dashboard(request):
    """Home page with overview statistics."""
    subject_count = Subject.objects.count()
    topic_count = Topic.objects.count()
    note_count = Note.objects.count()
    session_count = StudySession.objects.count()
    quiz_count = Quiz.objects.count()

    total_study_minutes = (
        StudySession.objects.aggregate(total=Sum('duration_minutes'))['total'] or 0
    )

    avg_accuracy = Quiz.objects.aggregate(avg=Avg('accuracy'))['avg']
    avg_accuracy = round(float(avg_accuracy), 1) if avg_accuracy else 0

    recent_sessions = StudySession.objects.select_related(
        'topic__subject'
    ).order_by('-start_time')[:5]

    recent_quizzes = Quiz.objects.select_related(
        'topic__subject'
    ).order_by('-completed_at')[:5]

    context = {
        'subject_count': subject_count,
        'topic_count': topic_count,
        'note_count': note_count,
        'session_count': session_count,
        'quiz_count': quiz_count,
        'total_study_minutes': total_study_minutes,
        'avg_accuracy': avg_accuracy,
        'recent_sessions': recent_sessions,
        'recent_quizzes': recent_quizzes,
    }
    return render(request, 'study/dashboard.html', context)


# ─── Subject Management ─────────────────────────────────────────────

def subject_list(request):
    """List all subjects with their topic counts."""
    subjects = Subject.objects.annotate(
        topic_count=Count('topic')
    ).order_by('name')
    return render(request, 'study/subjects.html', {'subjects': subjects})


def subject_add(request):
    """Add a new subject."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'Subject name cannot be empty.')
        elif Subject.objects.filter(name__iexact=name).exists():
            messages.warning(request, f'Subject "{name}" already exists.')
        else:
            Subject.objects.create(name=name)
            messages.success(request, f'Subject "{name}" added.')
        return redirect('subject_list')
    return render(request, 'study/subject_add.html')


def subject_rename(request, pk):
    """Rename an existing subject."""
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        new_name = request.POST.get('name', '').strip()
        if not new_name:
            messages.error(request, 'Name cannot be empty.')
        elif Subject.objects.filter(name__iexact=new_name).exclude(pk=pk).exists():
            messages.warning(request, f'Subject "{new_name}" already exists.')
        else:
            subject.name = new_name
            subject.save()
            messages.success(request, f'Subject renamed to "{new_name}".')
            return redirect('subject_list')
    return render(request, 'study/subject_rename.html', {'subject': subject})


def subject_delete(request, pk):
    """Delete a subject (cascades via MySQL FK)."""
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        name = subject.name
        subject.delete()
        messages.success(request, f'Subject "{name}" deleted.')
        return redirect('subject_list')
    return render(request, 'study/subject_confirm_delete.html', {'subject': subject})


# ─── Topic Management ───────────────────────────────────────────────

def topic_list(request, subject_id):
    """List topics under a subject."""
    subject = get_object_or_404(Subject, pk=subject_id)
    topics = Topic.objects.filter(subject=subject).order_by('name')
    # Annotate each topic with whether it has a note
    for t in topics:
        t.has_note = Note.objects.filter(topic=t).exists()
    return render(request, 'study/topics.html', {
        'subject': subject,
        'topics': topics,
    })


def topic_add(request, subject_id):
    """Add a new topic to a subject."""
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'Topic name cannot be empty.')
        elif Topic.objects.filter(subject=subject, name__iexact=name).exists():
            messages.warning(request, f'Topic "{name}" already exists in {subject.name}.')
        else:
            Topic.objects.create(subject=subject, name=name)
            messages.success(request, f'Topic "{name}" added to {subject.name}.')
        return redirect('topic_list', subject_id=subject.id)
    return render(request, 'study/topic_add.html', {'subject': subject})


def topic_rename(request, pk):
    """Rename a topic."""
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        new_name = request.POST.get('name', '').strip()
        if not new_name:
            messages.error(request, 'Name cannot be empty.')
        elif Topic.objects.filter(
            subject=topic.subject, name__iexact=new_name
        ).exclude(pk=pk).exists():
            messages.warning(request, f'Topic "{new_name}" already exists.')
        else:
            topic.name = new_name
            topic.save()
            messages.success(request, f'Topic renamed to "{new_name}".')
            return redirect('topic_list', subject_id=topic.subject_id)
    return render(request, 'study/topic_rename.html', {'topic': topic})


def topic_delete(request, pk):
    """Delete a topic."""
    topic = get_object_or_404(Topic, pk=pk)
    subject_id = topic.subject_id
    if request.method == 'POST':
        name = topic.name
        topic.delete()
        messages.success(request, f'Topic "{name}" deleted.')
        return redirect('topic_list', subject_id=subject_id)
    return render(request, 'study/topic_confirm_delete.html', {'topic': topic})


# ─── Notes Management ───────────────────────────────────────────────

def note_view(request, topic_id):
    """View / edit / create the note for a topic."""
    topic = get_object_or_404(Topic, pk=topic_id)
    try:
        note = Note.objects.get(topic=topic)
    except Note.DoesNotExist:
        note = None

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content:
            messages.error(request, 'Note content cannot be empty.')
        else:
            if note:
                note.content = content
                note.save()
                messages.success(request, 'Note updated.')
            else:
                Note.objects.create(topic=topic, content=content)
                messages.success(request, 'Note saved.')
        return redirect('note_view', topic_id=topic.id)

    return render(request, 'study/note.html', {'topic': topic, 'note': note})


def note_delete(request, topic_id):
    """Delete the note attached to a topic."""
    topic = get_object_or_404(Topic, pk=topic_id)
    try:
        note = Note.objects.get(topic=topic)
    except Note.DoesNotExist:
        messages.warning(request, 'No note to delete.')
        return redirect('topic_list', subject_id=topic.subject_id)

    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted.')
        return redirect('topic_list', subject_id=topic.subject_id)
    return render(request, 'study/note_confirm_delete.html', {
        'topic': topic, 'note': note,
    })


# ─── AI Features ─────────────────────────────────────────────────────

def ai_doubt(request):
    """Ask a question and get an AI response."""
    answer = None
    question = ''
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        if len(question) < 5:
            messages.error(request, 'Please enter a question with at least 5 characters.')
        else:
            answer = resolve_doubt(question)
    return render(request, 'study/ai_doubt.html', {
        'answer': answer, 'question': question,
    })


def ai_quiz(request):
    """Generate and take a quiz."""
    subjects = Subject.objects.order_by('name')

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'generate':
            subject_id = request.POST.get('subject_id')
            topic_input = request.POST.get('topic_input', '').strip()

            if not subject_id or not topic_input:
                messages.error(request, 'Please select a subject and enter a topic.')
                return render(request, 'study/ai_quiz.html', {'subjects': subjects})

            subject = get_object_or_404(Subject, pk=subject_id)
            result = generate_quiz(topic_input)

            if result['error']:
                messages.error(request, result['error'])
                return render(request, 'study/ai_quiz.html', {'subjects': subjects})

            # Verify topic exists in database
            extracted = result['extracted_topic']
            topic = Topic.objects.filter(
                subject=subject, name__iexact=extracted
            ).first()

            if not topic:
                messages.error(
                    request,
                    f'Topic "{extracted}" not found under "{subject.name}". '
                    f'Please add the topic first.'
                )
                return render(request, 'study/ai_quiz.html', {'subjects': subjects})

            # Store quiz data in session for the answer step
            request.session['quiz_data'] = {
                'subject_name': subject.name,
                'topic_id': topic.id,
                'topic_name': topic.name,
                'questions': result['questions'],
                'answer_list': result['answer_list'],
                'quiz_text': result['quiz_text'],
            }

            return render(request, 'study/ai_quiz_take.html', {
                'quiz_data': request.session['quiz_data'],
                'quiz_size': QUIZ_SIZE,
            })

        elif action == 'submit':
            quiz_data = request.session.get('quiz_data')
            if not quiz_data:
                messages.error(request, 'Quiz session expired. Please generate a new quiz.')
                return redirect('ai_quiz')

            answer_list = quiz_data['answer_list']
            user_answers = []
            for i in range(QUIZ_SIZE):
                ans = request.POST.get(f'answer_{i}', '').upper()
                user_answers.append(ans)

            score = sum(
                1 for u, c in zip(user_answers, answer_list) if u == c
            )
            accuracy = score / QUIZ_SIZE * 100

            # Build review data
            review = []
            for i in range(QUIZ_SIZE):
                review.append({
                    'number': i + 1,
                    'user_answer': user_answers[i],
                    'correct_answer': answer_list[i],
                    'is_correct': user_answers[i] == answer_list[i],
                })

            # Save quiz with ECDSA signature
            try:
                save_quiz_result(quiz_data['topic_id'], score, accuracy)
            except Exception as e:
                messages.warning(request, f'Quiz saved without signature: {e}')

            # Clean up session
            del request.session['quiz_data']

            return render(request, 'study/ai_quiz_result.html', {
                'subject_name': quiz_data['subject_name'],
                'topic_name': quiz_data['topic_name'],
                'score': score,
                'total': QUIZ_SIZE,
                'accuracy': accuracy,
                'review': review,
                'questions': quiz_data['questions'],
            })

    return render(request, 'study/ai_quiz.html', {'subjects': subjects})


def ai_summarize(request):
    """Summarize a note using Gemini."""
    subjects = Subject.objects.order_by('name')
    summary = None
    selected_subject_id = None
    selected_topic_id = None

    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        if not topic_id:
            messages.error(request, 'Please select a topic.')
        else:
            topic = get_object_or_404(Topic, pk=topic_id)
            try:
                note = Note.objects.get(topic=topic)
            except Note.DoesNotExist:
                messages.error(request, f'No note found for "{topic.name}".')
                return render(request, 'study/ai_summarize.html', {
                    'subjects': subjects,
                })

            summary = summarize_note(note.content)
            selected_subject_id = topic.subject_id
            selected_topic_id = topic.id

    return render(request, 'study/ai_summarize.html', {
        'subjects': subjects,
        'summary': summary,
        'selected_subject_id': selected_subject_id,
        'selected_topic_id': selected_topic_id,
    })


def ai_study_plan(request):
    """Generate a personalized study plan."""
    plan = None
    goal = ''
    duration = ''
    study_hours = ''

    if request.method == 'POST':
        goal = request.POST.get('goal', '').strip()
        duration = request.POST.get('duration', '').strip()
        study_hours = request.POST.get('study_hours', '').strip()

        if not goal:
            messages.error(request, 'Please enter your study goal.')
        else:
            try:
                dur = int(duration)
                hrs = int(study_hours)
                if dur <= 0 or hrs <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                messages.error(request, 'Duration and hours must be positive numbers.')
                return render(request, 'study/ai_study_plan.html', {
                    'goal': goal, 'duration': duration,
                    'study_hours': study_hours,
                })

            plan = generate_study_plan(goal, dur, hrs)

    return render(request, 'study/ai_study_plan.html', {
        'plan': plan, 'goal': goal, 'duration': duration,
        'study_hours': study_hours,
    })


# ─── Study Sessions ─────────────────────────────────────────────────

def session_start(request):
    """Start or record a study session."""
    subjects = Subject.objects.order_by('name')

    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        duration = request.POST.get('duration', '').strip()

        if not topic_id or not duration:
            messages.error(request, 'Please select a topic and enter duration.')
            return render(request, 'study/session_start.html', {
                'subjects': subjects,
            })

        try:
            duration_minutes = int(duration)
            if duration_minutes <= 0:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, 'Duration must be a positive number.')
            return render(request, 'study/session_start.html', {
                'subjects': subjects,
            })

        topic = get_object_or_404(Topic, pk=topic_id)
        now = datetime.now()

        StudySession.objects.create(
            topic=topic,
            start_time=now,
            end_time=now,
            duration_minutes=duration_minutes,
        )

        messages.success(
            request,
            f'Study session recorded: {topic.name} — {duration_minutes} minutes.'
        )
        return redirect('session_start')

    return render(request, 'study/session_start.html', {'subjects': subjects})


# ─── AJAX helper: load topics for a subject ──────────────────────────

def ajax_topics(request, subject_id):
    """Return topics for a subject as JSON (used by select dropdowns)."""
    topics = Topic.objects.filter(subject_id=subject_id).order_by('name')
    data = [{'id': t.id, 'name': t.name} for t in topics]
    return JsonResponse(data, safe=False)


# ─── Search ──────────────────────────────────────────────────────────

def search_view(request):
    """Search subjects, topics, and notes."""
    query = request.GET.get('q', '').strip()
    results = {
        'subjects': [],
        'topics': [],
        'notes': [],
    }

    if query:
        results['subjects'] = Subject.objects.filter(
            name__icontains=query
        ).annotate(topic_count=Count('topic'))

        results['topics'] = Topic.objects.filter(
            name__icontains=query
        ).select_related('subject')

        results['notes'] = Note.objects.filter(
            content__icontains=query
        ).select_related('topic__subject')

    return render(request, 'study/search.html', {
        'query': query, 'results': results,
    })


# ─── Reports ─────────────────────────────────────────────────────────

def reports_view(request):
    """Show study and quiz reports."""
    # Study statistics
    sessions = StudySession.objects.select_related('topic__subject').all()
    study_stats = None
    if sessions.exists():
        total_sessions = sessions.count()
        total_minutes = sessions.aggregate(total=Sum('duration_minutes'))['total'] or 0
        avg_duration = round(total_minutes / total_sessions, 1) if total_sessions else 0

        # Most studied subject
        subject_counts = {}
        topic_counts = {}
        for s in sessions:
            sn = s.topic.subject.name
            tn = s.topic.name
            subject_counts[sn] = subject_counts.get(sn, 0) + 1
            topic_counts[tn] = topic_counts.get(tn, 0) + 1

        study_stats = {
            'total_sessions': total_sessions,
            'total_minutes': total_minutes,
            'avg_duration': avg_duration,
            'most_subject': max(subject_counts, key=subject_counts.get) if subject_counts else 'N/A',
            'most_topic': max(topic_counts, key=topic_counts.get) if topic_counts else 'N/A',
        }

    # Quiz statistics
    quizzes = Quiz.objects.select_related('topic').all()
    quiz_stats = None
    if quizzes.exists():
        total_quizzes = quizzes.count()
        avg_accuracy = round(
            float(quizzes.aggregate(avg=Avg('accuracy'))['avg'] or 0), 1
        )
        avg_score = round(
            float(quizzes.aggregate(avg=Avg('score'))['avg'] or 0), 1
        )
        highest = quizzes.aggregate(mx=Max('score'))['mx'] or 0
        lowest = quizzes.aggregate(mn=Min('score'))['mn'] or 0

        topic_counts = {}
        for q in quizzes:
            tn = q.topic.name
            topic_counts[tn] = topic_counts.get(tn, 0) + 1

        quiz_stats = {
            'total_quizzes': total_quizzes,
            'avg_accuracy': avg_accuracy,
            'avg_score': avg_score,
            'highest_score': highest,
            'lowest_score': lowest,
            'most_topic': max(topic_counts, key=topic_counts.get) if topic_counts else 'N/A',
        }

    return render(request, 'study/reports.html', {
        'study_stats': study_stats,
        'quiz_stats': quiz_stats,
    })


# ─── Quiz Integrity ─────────────────────────────────────────────────

def quiz_integrity(request):
    """ECDSA quiz integrity verification."""
    recent_quizzes = Quiz.objects.select_related('topic').order_by(
        '-completed_at', '-id'
    )[:10]

    results = []
    for quiz in recent_quizzes:
        status = _verify_quiz(quiz)
        results.append({
            'quiz': quiz,
            'status': status,
        })

    # Tampered quizzes
    signed_quizzes = Quiz.objects.filter(
        signature__isnull=False
    ).exclude(signature='').select_related('topic').order_by(
        '-completed_at', '-id'
    )

    tampered = []
    for quiz in signed_quizzes:
        status = _verify_quiz(quiz)
        if status == 'tampered':
            tampered.append({
                'quiz': quiz,
                'status': status,
            })

    return render(request, 'study/quiz_integrity.html', {
        'results': results,
        'tampered': tampered,
    })


def _verify_quiz(quiz):
    """
    Verify ECDSA signature of a quiz.
    Uses storageManager.verify_quiz_integrity for canonical verification.
    """
    res = verify_quiz_integrity(quiz.id)
    return res.get('status', 'error')
