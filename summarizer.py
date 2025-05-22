import re

def generate_summary(transcript_text):
    """
    Generates a structured summary from the transcript text.
    Identifies action items, decisions, and key discussion points based on keywords and sentence length.
    Args:
        transcript_text (str): The raw meeting transcript.
    Returns:
        dict: A structured summary with title, action items, decisions, key points, and a transcript preview.
    """
    summary = {
        "title": "Meeting Summary",
        "action_items": [],
        "decisions_made": [],
        "key_discussion_points": [],
        "full_transcript_preview": ""
    }

    if not transcript_text or not transcript_text.strip():
        summary["key_discussion_points"].append("The provided transcript was empty.")
        summary["action_items"].append("N/A")
        summary["decisions_made"].append("N/A")
        summary["full_transcript_preview"] = "Empty transcript."
        return summary

    # Split transcript into sentences. Handles common abbreviations.
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', transcript_text)
    sentences = [s.strip() for s in sentences if s.strip()] # Clean up empty strings after split

    action_keywords = ['action item', 'assign', 'task', 'to do', 'next step', 'responsible for', 'follow up', 'plan to']
    decision_keywords = ['decided', 'agreed', 'concluded', 'resolution', 'approved', 'confirmed', 'vote passed']
    # Minimum number of words for a sentence to be considered a key point (if not action/decision)
    key_point_min_words = 8 
    # Minimum character length for a sentence to be considered a key point (additional filter)
    key_point_min_chars = 25 

    processed_sentences = set() # To avoid duplicating sentences across sections

    for sentence in sentences:
        sentence_lower = sentence.lower()

        # Check for Action Items
        is_action = False
        for keyword in action_keywords:
            if keyword in sentence_lower:
                if sentence not in processed_sentences:
                    summary["action_items"].append(sentence)
                    processed_sentences.add(sentence)
                    is_action = True
                break
        if is_action: continue # Prioritize as action item

        # Check for Decisions
        is_decision = False
        for keyword in decision_keywords:
            if keyword in sentence_lower:
                if sentence not in processed_sentences:
                    summary["decisions_made"].append(sentence)
                    processed_sentences.add(sentence)
                    is_decision = True
                break
        if is_decision: continue # Prioritize as decision

    # Identify Key Discussion Points (sentences not already captured, meeting length criteria)
    for sentence in sentences:
        if sentence not in processed_sentences and \
           len(sentence.split()) >= key_point_min_words and \
           len(sentence) >= key_point_min_chars:
            summary["key_discussion_points"].append(sentence)
            # No need to add to processed_sentences if this is the last category checked for this sentence

    # Handle cases where no specific items were found
    raw_transcript_excerpt_length = 250 # Default preview length
    if not summary["action_items"] and not summary["decisions_made"] and not summary["key_discussion_points"]:
        summary["key_discussion_points"].append("No specific action items, decisions, or key discussion points were automatically identified from the transcript. Please review the full text.")
        raw_transcript_excerpt_length = 500 # Longer preview if no sections found
    
    if not summary["action_items"]:
        summary["action_items"].append("None identified.")
    if not summary["decisions_made"]:
        summary["decisions_made"].append("None identified.")

    # Create transcript preview
    preview_text = transcript_text[:raw_transcript_excerpt_length]
    if len(transcript_text) > raw_transcript_excerpt_length:
        preview_text += "..."
    summary["full_transcript_preview"] = preview_text

    return summary
