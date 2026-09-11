from storageManager import get_subject_by_name
from storageManager import get_topic_by_name
from storageManager import save_study_session
from datetime import datetime

subject = get_subject_by_name("Probability")
topic = get_topic_by_name(subject["id"], "Conditional Probability")

start = datetime.now()
end = datetime.now()

save_study_session(
    topic["id"],
    start,
    end,
    1
)

print("Study session saved.")