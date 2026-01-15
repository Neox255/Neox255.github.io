def handle_license_order(course_id, teacher_email, correspondence_language, license_type, usage_count, workbook):
    """
    Logik:
    - <= 3 Nutzungen: Excel-Eintrag für manuelle Bearbeitung
    - > 3 Nutzungen: keine Excel-Liste, Bestellung wird normal automatisch verarbeitet
    """
    if usage_count <= 3:
        save_to_excel(
            [course_id, teacher_email, correspondence_language],
            workbook
        )
        return "manual_check"
    return "auto_process"
