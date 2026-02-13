#!/usr/bin/env python3
"""
Inworld TTS Voice Configuration

Voice IDs and assignments for TOEFL practice materials.
Voice IDs are typically capitalized versions of the voice names.

To verify voice IDs, use the Inworld API:
  curl -X GET 'https://api.inworld.ai/tts/v1/voices?filter=language=en' \
    -H 'Authorization: Basic <api-key>'
"""

# ==================== VOICE ID MAPPINGS ====================
# Map voice names to their Inworld API voice IDs
VOICE_IDS = {
    # Female voices
    "ashley": "Ashley",      # Warm, natural female voice
    "deborah": "Deborah",    # Female voice (verify ID)
    "sarah": "Sarah",        # Female voice (verify ID)
    
    # Male voices (general)
    "dennis": "Dennis",      # Middle-aged man, smooth, calm, friendly
    "mark": "Mark",          # Male voice (verify ID)
    
    # Male admin/professional voices
    "edward": "Edward",      # Male admin/prof voice (verify ID)
    "craig": "Craig",        # British male admin/prof voice (verify ID)
    "carter": "Carter",      # Male admin/prof voice (verify ID)
}

# ==================== VOICE ASSIGNMENTS BY CONTENT TYPE ====================

# Listen & Repeat Sets (sentence-by-sentence practice)
LR_VOICES = {
    "S01": "ashley",      # Campus Bookstore Tour (A2-B1) - friendly tour guide
    "S02": "deborah",     # Natural History Museum Tour (B1-B2) - tour guide
    "S03": "edward",      # University Orientation (B2-C1) - Dr. Chen, academic administrator
    "S04": "sarah",       # Campus Dining Hall Tour (A2-B1) - friendly staff member
    "S05": "carter",      # Biology Lab Safety Orientation (B1-B2) - instructor/professor
    "S06": "craig",       # Art History Lecture (B2-C1) - professor/lecturer (British accent)
}

# Interview Practice Sets (interviewer voices)
INTERVIEW_VOICES = {
    "PT1": "edward",      # Work-Life Balance - Research Study interviewer (Dr. Williams)
    "SC1": "craig",       # Scholarship Application - Professor Adams (British academic)
    "OA1": "edward",      # Outdoor Activities - Research Study interviewer (Dr. Chen)
    "CL1": "sarah",       # Campus Life - Student Survey interviewer (Ms. Thompson)
    "ZJ1": "sarah",       # 真题 2026-01-21 — Health and Habits (Graduate Researcher)
}

# Conversation Practice (dialogue between two speakers)
CONVERSATION_VOICES = {
    "female": "ashley",   # Default female voice for conversations
    "male": "dennis",     # Default male voice for conversations
}

# Choose Response Practice (short dialogues)
CHOOSE_RESPONSE_VOICES = {
    "female": "ashley",   # Default female voice
    "male": "dennis",     # Default male voice
}

# Announcement Practice (campus announcements)
ANNOUNCEMENT_VOICES = {
    "default": "mark",    # General announcements
    "female": "sarah",    # Female announcer option
    "male": "mark",       # Male announcer option
}

# Academic Talk Practice (short lectures A2–C1)
# Voice direction: clear, moderate pace; authoritative but approachable; American primary, British for history/seminar.
ACADEMIC_TALK_VOICES = {
    "A2-01": "sarah",   # Four Seasons — warm, clear; ideal for beginners (science class)
    "A2-02": "sarah",   # A Day at School — same voice for A2 tier consistency (orientation)
    "B1-01": "dennis",  # How Libraries Work — calm, friendly (library orientation)
    "B1-02": "ashley",  # Why We Have Weekends — warm, natural (social studies)
    "B2-01": "carter",  # Photosynthesis — instructor/professor tone (biology)
    "B2-02": "craig",   # Roman Aqueducts — British, fits history/classics
    "C1-01": "edward",  # Climate Feedback — serious, academic (environmental science)
    "C1-02": "craig",   # Historical Causation — British, seminar/lecture tone
}


# ==================== HELPER FUNCTIONS ====================

def get_voice_id(voice_name):
    """Get the Inworld API voice ID for a voice name."""
    voice_name_lower = voice_name.lower()
    if voice_name_lower in VOICE_IDS:
        return VOICE_IDS[voice_name_lower]
    # If not found, try capitalized version
    return voice_name.capitalize()


def get_lr_voice(set_id):
    """Get the voice name for a Listen & Repeat set."""
    return LR_VOICES.get(set_id, "ashley")  # Default to Ashley


def get_interview_voice(set_id):
    """Get the voice name for an Interview practice set."""
    return INTERVIEW_VOICES.get(set_id, "edward")  # Default to Edward


def get_voice_id_for_lr_set(set_id):
    """Get the Inworld API voice ID for a Listen & Repeat set."""
    voice_name = get_lr_voice(set_id)
    return get_voice_id(voice_name)


def get_voice_id_for_interview_set(set_id):
    """Get the Inworld API voice ID for an Interview practice set."""
    voice_name = get_interview_voice(set_id)
    return get_voice_id(voice_name)


def get_academic_talk_voice(talk_id):
    """Get the voice name for an Academic Talk (e.g. A2-01, B1-02)."""
    return ACADEMIC_TALK_VOICES.get(talk_id, "carter")  # Default: professor tone


def get_voice_id_for_academic_talk(talk_id):
    """Get the Inworld API voice ID for an Academic Talk."""
    voice_name = get_academic_talk_voice(talk_id)
    return get_voice_id(voice_name)


# ==================== VOICE DESCRIPTIONS ====================
VOICE_DESCRIPTIONS = {
    "ashley": "Warm, natural female voice - good for friendly, approachable content",
    "deborah": "Female voice - good for tour guides and informational content",
    "sarah": "Female voice - good for student services and campus life content",
    "dennis": "Middle-aged man with smooth, calm, friendly voice - good for general conversations",
    "mark": "Male voice - good for announcements and general content",
    "edward": "Male admin/professional voice - good for academic administrators and researchers",
    "craig": "British male admin/professional voice - good for academic/professional content",
    "carter": "Male admin/professional voice - good for instructors and professors",
}
