def calculate_attendance(total, attended):
    if total == 0:
        return 0
    return (attended / total) * 100

def get_status(percentage):
    if percentage >= 75:
        return "Safe"
    elif percentage >= 60:
        return "Warning"
    else:
        return "Danger"
    
import math

def classes_needed_for_75(total, attended):
    required = 0.75
    x = 0

    while True:
        if (attended + x) / (total + x) >= required:
            return x
        x += 1

def predict_future(total, attended, missed_classes):
    new_total = total + missed_classes
    new_attended = attended
    return (new_attended / new_total) * 100