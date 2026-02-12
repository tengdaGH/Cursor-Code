#!/usr/bin/env python3
"""
Generate audio for "Listen and Choose a Response" practice questions.
Creates short dialogues (2-3 turns) with American accent voices.
"""

import os
import sys
import requests
import base64
import wave
import struct
import subprocess
from pathlib import Path

# Load API key from .env file
def load_env():
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('INWORLD_API_KEY='):
                    return line.split('=', 1)[1].strip()
    return None

API_KEY = load_env() or os.getenv('INWORLD_API_KEY')
if not API_KEY:
    print("Error: Set INWORLD_API_KEY environment variable or add it to .env file")
    sys.exit(1)

API_URL = "https://api.inworld.ai/tts/v1/voice"
VOICE_FEMALE = "Olivia"  # American female
VOICE_MALE = "Dennis"    # American male
MODEL_ID = "inworld-tts-1.5-mini"
SAMPLE_RATE = 48000
PAUSE_BETWEEN_TURNS = 0.8  # seconds
LEADING_SILENCE = 0.5  # seconds

# Question sets with dialogues - All 30 questions for R01
# Voices alternate between male and female for natural conversation flow
QUESTIONS = {
    "R01-01": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Excuse me, do you know what time it is?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Sorry, I don't have my watch with me."}
        ]
    },
    "R01-02": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Hi, I'd like to return this shirt. I bought it yesterday, but it doesn't fit."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Do you have the receipt?"}
        ]
    },
    "R01-03": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm having trouble understanding this assignment. Could you explain it again?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Of course. What part would you like me to clarify?"}
        ]
    },
    "R01-04": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Thank you so much for helping me with my project."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "You're welcome. I'm glad I could help."}
        ]
    },
    "R01-05": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Excuse me, where is the restroom?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "It's down the hall, second door on your right."}
        ]
    },
    "R01-06": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'm looking for the library. Can you point me in the right direction?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Sure. Go straight ahead, and you'll see it on your left."}
        ]
    },
    "R01-07": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm sorry I couldn't make it to your party last weekend."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "That's okay. We missed you, though."}
        ]
    },
    "R01-08": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'd like to make a reservation for dinner tonight."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "For how many people?"}
        ]
    },
    "R01-09": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I missed class yesterday. Did I miss anything important?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "We went over the midterm review. You should check with a classmate for the notes."}
        ]
    },
    "R01-10": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Do you know if the student center is open on weekends?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Yes, it's open from 9 AM to 5 PM on Saturdays and Sundays."}
        ]
    },
    "R01-11": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Would you mind if I sat here?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Not at all. Please, go ahead."}
        ]
    },
    "R01-12": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'm looking for a book by John Smith. Do you have it?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Let me check our system. What's the title?"}
        ]
    },
    "R01-13": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm struggling with this course. Do you think I should drop it?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "That's a big decision. Have you talked to your professor about it?"}
        ]
    },
    "R01-14": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Excuse me, is there a coffee shop nearby?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Yes, there's one right across the street."}
        ]
    },
    "R01-15": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I heard you got a new job. Congratulations!"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Thank you! I'm really excited about it."}
        ]
    },
    "R01-16": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'd like to cancel my appointment for tomorrow."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Sure. Can I have your name, please?"}
        ]
    },
    "R01-17": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm not sure I understand this concept. Could you explain it differently?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Of course. Let me try another approach."}
        ]
    },
    "R01-18": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Do you know where the parking garage is?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "It's behind the main building, on the left side."}
        ]
    },
    "R01-19": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm really sorry about what happened yesterday. I didn't mean to upset you."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "I understand. These things happen sometimes."}
        ]
    },
    "R01-20": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'd like to return this item. It doesn't work properly."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Do you have the original packaging?"}
        ]
    },
    "R01-21": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm having trouble finding research materials for my paper."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Have you tried the library's online database?"}
        ]
    },
    "R01-22": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Is the gym open late on weekdays?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Yes, it's open until 10 PM Monday through Friday."}
        ]
    },
    "R01-23": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Would you like to join us for lunch?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "That sounds great! What time are you going?"}
        ]
    },
    "R01-24": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'm not satisfied with the service I received. I'd like to speak to a manager."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "I understand your concern. Let me get the manager for you."}
        ]
    },
    "R01-25": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I missed the deadline for the assignment. Is there any way I can still submit it?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "The late policy allows submissions up to 48 hours after the deadline with a penalty."}
        ]
    },
    "R01-26": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Do you know if there's a printer I can use nearby?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "There's one in the computer lab, just down the hall."}
        ]
    },
    "R01-27": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I wanted to apologize for my behavior at the meeting. I was out of line."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "I appreciate you saying that. We can move forward from here."}
        ]
    },
    "R01-28": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'd like to change my flight to an earlier time."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Let me check what's available. What time would you prefer?"}
        ]
    },
    "R01-29": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm concerned about my grade in this course. I've been working hard, but I'm not seeing improvement."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Have you considered meeting with me during office hours to discuss study strategies?"}
        ]
    },
    "R01-30": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'm new here. Can you tell me where the main office is?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Sure. It's on the second floor, room 205."}
        ]
    },
    # R02 Set - Campus & Academic (30 questions)
    "R02-01": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Where can I find the registrar's office?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "It's on the first floor of the administration building."}
        ]
    },
    "R02-02": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm not sure which textbook I need for this course."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "The required textbook is listed on the course syllabus."}
        ]
    },
    "R02-03": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Is the dining hall open during spring break?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "No, it's closed during spring break, but the café in the student center stays open."}
        ]
    },
    "R02-04": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Can I get an extension on this assignment?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "What's your reason for needing an extension?"}
        ]
    },
    "R02-05": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Do you know where I can buy my parking permit?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "You can purchase it online or at the campus security office."}
        ]
    },
    "R02-06": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm worried that I won't be able to keep up with the coursework. Should I drop this class?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Before making that decision, have you considered using the tutoring center? They offer free help for students."}
        ]
    },
    "R02-07": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Where can I pick up my student ID card?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "The ID office is in the student services building, room 101."}
        ]
    },
    "R02-08": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I missed the last lecture. Can I get the notes from someone?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "The lecture slides are posted on the course website, and you can also ask a classmate."}
        ]
    },
    "R02-09": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Is there a place where I can study quietly?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "The library has quiet study areas on the third and fourth floors."}
        ]
    },
    "R02-10": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm having trouble accessing the online course materials."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Have you tried logging in with your student email and password?"}
        ]
    },
    "R02-11": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Where can I find information about campus clubs and organizations?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "There's a student activities fair next week, or you can check the website."}
        ]
    },
    "R02-12": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm not sure if I should take this advanced course. I'm worried it might be too difficult."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Have you completed the prerequisites? That usually helps students prepare for the advanced level."}
        ]
    },
    "R02-13": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Do you know if the bookstore is open today?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Yes, it's open from 9 AM to 6 PM on weekdays."}
        ]
    },
    "R02-14": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I submitted my paper online, but I'm not sure if it went through."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "You should receive a confirmation email. Did you check your inbox?"}
        ]
    },
    "R02-15": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I need to find a place to print my assignment. Where can I do that?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "There are printers in the computer lab on the second floor, and you can also use the library printers."}
        ]
    },
    "R02-16": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm confused about the grading rubric for this project."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "The rubric is posted on the course website under the assignments section."}
        ]
    },
    "R02-17": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Is there a place where I can store my bike safely?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "There are bike racks near the main entrance of most buildings."}
        ]
    },
    "R02-18": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm considering changing my major, but I'm not sure what to choose."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "The career counseling center offers assessments that can help you explore different options."}
        ]
    },
    "R02-19": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Where can I find the schedule for campus events?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "You can check the campus calendar online or pick up a printed schedule at the student center."}
        ]
    },
    "R02-20": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm not sure how to cite sources in my research paper."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "The library has citation guides available, and there are also online resources."}
        ]
    },
    "R02-21": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Is there a lost and found office on campus?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Yes, it's located in the student services building, first floor."}
        ]
    },
    "R02-22": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I missed the exam review session. Is there another way I can prepare?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "The review materials are posted online, and you can also form a study group with classmates."}
        ]
    },
    "R02-23": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Where can I get help with my resume?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "The career center offers resume review services. You can make an appointment online."}
        ]
    },
    "R02-24": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm struggling to balance my coursework with my part-time job. I'm worried about my grades."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Have you talked to your academic advisor? They can help you create a schedule that works better."}
        ]
    },
    "R02-25": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Is there a place where I can get my laptop fixed?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "The IT support center can help with computer repairs. It's in the library building."}
        ]
    },
    "R02-26": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm not sure if I understand the assignment instructions correctly."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "The instructions are detailed in the assignment handout. Have you read through it carefully?"}
        ]
    },
    "R02-27": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Where can I find information about on-campus housing?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "The housing office has all the details, and you can also check their website for availability."}
        ]
    },
    "R02-28": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm concerned that I won't be able to complete all the required courses before graduation."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Have you met with your advisor to create a graduation plan? They can help you map out your remaining semesters."}
        ]
    },
    "R02-29": {
        "topic": "Campus",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Is there a place where I can charge my phone?"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "There are charging stations in the student center and library."}
        ]
    },
    "R02-30": {
        "topic": "Academic",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm not sure how to access the online discussion forum for this course."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "You need to log in through the course website, and there's a link to the forum in the navigation menu."}
        ]
    },
    # R03 Set - Service & Social (30 questions)
    "R03-01": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to order a coffee, please."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "What size would you like?"}
        ]
    },
    "R03-02": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Happy birthday! I hope you have a wonderful day."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Thank you so much! That's very kind of you."}
        ]
    },
    "R03-03": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to book a hotel room for next weekend."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "How many nights will you be staying?"}
        ]
    },
    "R03-04": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I really enjoyed the movie we saw together last night."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "I'm glad you liked it! I thought it was great too."}
        ]
    },
    "R03-05": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Excuse me, do you accept credit cards?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Yes, we accept all major credit cards."}
        ]
    },
    "R03-06": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I heard you're moving to a new apartment. How exciting!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Yes, I'm really looking forward to it. The new place is much closer to campus."}
        ]
    },
    "R03-07": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to return this item. It's defective."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Do you have your receipt with you?"}
        ]
    },
    "R03-08": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Congratulations on your graduation!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Thank you! I can't believe it's finally here."}
        ]
    },
    "R03-09": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to schedule a haircut appointment."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "What day works best for you?"}
        ]
    },
    "R03-10": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to thank you for helping me move last weekend. I really appreciate it."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "You're welcome! I was happy to help. How are you settling into the new place?"}
        ]
    },
    "R03-11": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Do you have this shirt in a larger size?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Let me check for you. What size are you looking for?"}
        ]
    },
    "R03-12": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'm so sorry I forgot to call you back yesterday."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "That's okay. I understand you've been busy."}
        ]
    },
    "R03-13": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to exchange this for a different color."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Sure. What color would you prefer?"}
        ]
    },
    "R03-14": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I hope you feel better soon!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Thank you! I'm starting to feel a bit better already."}
        ]
    },
    "R03-15": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm not happy with the service I received. The food took over an hour to arrive."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "I sincerely apologize for the delay. Let me speak with the manager about this."}
        ]
    },
    "R03-16": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to let you know that I got accepted into graduate school!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "That's fantastic news! Congratulations!"}
        ]
    },
    "R03-17": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Can I pay with cash?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Of course. Cash is accepted."}
        ]
    },
    "R03-18": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'm really sorry I couldn't attend your presentation yesterday."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "That's all right. I understand you had other commitments."}
        ]
    },
    "R03-19": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to make a complaint about my recent order."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "I'm sorry to hear that. Can you tell me what happened?"}
        ]
    },
    "R03-20": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to apologize for my comment at the meeting. It was inappropriate."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "I appreciate you saying that. We can move past this."}
        ]
    },
    "R03-21": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Is this item on sale?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Yes, it's 30% off this week."}
        ]
    },
    "R03-22": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I heard you got promoted! That's amazing!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Thank you! I'm really excited about the new role."}
        ]
    },
    "R03-23": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to cancel my subscription."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "I can help with that. Can I have your account number?"}
        ]
    },
    "R03-24": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to thank you for being so supportive during my job search. Your advice really helped."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "I'm so glad I could help! How is everything going now?"}
        ]
    },
    "R03-25": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Do you offer delivery?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Yes, we deliver within a 5-mile radius."}
        ]
    },
    "R03-26": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'm really sorry I forgot your birthday. I feel terrible about it."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Don't worry about it. I know you've been busy lately."}
        ]
    },
    "R03-27": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to upgrade my phone plan."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "What features are you looking for in the upgrade?"}
        ]
    },
    "R03-28": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to apologize for not responding to your messages. I've been dealing with some personal issues."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "I understand. Is everything okay now?"}
        ]
    },
    "R03-29": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Can I get a refund for this purchase?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Do you have the receipt with you?"}
        ]
    },
    "R03-30": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to thank you for helping me prepare for my interview. Your tips were really helpful!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "You're welcome! I'm glad I could help. How did it go?"}
        ]
    }
}

def synthesize_sentence(text, voice_id):
    """Call Inworld TTS API for a single sentence. Returns raw PCM audio bytes."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {API_KEY}"
    }
    data = {
        "text": text,
        "voice_id": voice_id,
        "model_id": MODEL_ID,
        "audio_config": {
            "audio_encoding": "LINEAR16",
            "sample_rate_hertz": SAMPLE_RATE
        }
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        audio_bytes = base64.b64decode(result["audioContent"])
        # Strip WAV header if present
        if len(audio_bytes) > 44 and audio_bytes[:4] == b'RIFF':
            audio_bytes = audio_bytes[44:]
        return audio_bytes
    except requests.exceptions.RequestException as e:
        print(f"Error synthesizing '{text[:50]}...': {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise

def generate_silence(duration_seconds):
    """Generate raw PCM silence (16-bit mono)."""
    num_samples = int(SAMPLE_RATE * duration_seconds)
    return b'\x00\x00' * num_samples

def combine_to_wav(audio_chunks, output_wav):
    """Combine raw PCM chunks into a WAV file."""
    import wave
    with wave.open(str(output_wav), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        for chunk in audio_chunks:
            wf.writeframes(chunk)

def wav_to_mp3(wav_path, mp3_path):
    """Convert WAV to MP3 using ffmpeg."""
    import subprocess
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(wav_path),
            "-codec:a", "libmp3lame", "-qscale:a", "2",
            str(mp3_path)
        ], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting to MP3: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.")
        return False

def generate_audio(question_id, dialogue_data):
    """Generate audio for a single dialogue."""
    print(f"\nGenerating audio for {question_id}...")
    
    audio_chunks = []
    
    # Add leading silence
    audio_chunks.append(generate_silence(LEADING_SILENCE))
    
    # Synthesize each turn
    for i, turn in enumerate(dialogue_data["dialogue"]):
        print(f"  Synthesizing: {turn['speaker']} - '{turn['text'][:50]}...'")
        audio_data = synthesize_sentence(turn['text'], turn['voice'])
        audio_chunks.append(audio_data)
        
        # Add pause between turns (except after last turn)
        if i < len(dialogue_data["dialogue"]) - 1:
            audio_chunks.append(generate_silence(PAUSE_BETWEEN_TURNS))
    
    # Save to file
    output_dir = Path(__file__).parent.parent / 'audio' / 'listening'
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_wav = output_dir / f"LCR-{question_id}.tmp.wav"
    output_path = output_dir / f"LCR-{question_id}.mp3"
    
    # Combine into WAV
    combine_to_wav(audio_chunks, temp_wav)
    
    # Convert to MP3
    if wav_to_mp3(temp_wav, output_path):
        temp_wav.unlink()  # Remove temp file
        file_size = output_path.stat().st_size / 1024  # KB
        print(f"  ✓ Saved: {output_path} ({file_size:.1f} KB)")
        return True
    else:
        return False

def main():
    print("Generating audio for 'Listen and Choose a Response' questions...")
    print(f"Using API: {API_URL}")
    print(f"Voices: {VOICE_MALE} (male), {VOICE_FEMALE} (female)")
    
    success_count = 0
    total = len(QUESTIONS)
    
    for question_id, dialogue_data in QUESTIONS.items():
        if generate_audio(question_id, dialogue_data):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Complete: {success_count}/{total} audio files generated")
    if success_count < total:
        print(f"Failed: {total - success_count} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
