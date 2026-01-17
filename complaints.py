def add_complaint(complaint_list, cid, user, msg, priority):
    new_complaint = {
        "id": cid,
        "user": user,
        "message": msg,
        "priority": priority,
        "status": "Pending"
    }
    complaint_list.append(new_complaint)
    print("✅ Complaint registered successfully.")
    return complaint_list