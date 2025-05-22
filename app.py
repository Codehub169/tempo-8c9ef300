from flask import Flask, render_template, request
import os
from summarizer import generate_summary # Assuming summarizer.py is in the same directory

app = Flask(__name__)

# Flask will look for templates in a 'templates' folder 
# and static files in a 'static' folder by default.

@app.route('/', methods=['GET'])
def index():
    """Serves the main page for transcript input."""
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize_transcript_route():
    """Handles transcript submission and displays the generated summary."""
    transcript_text = ""
    error_message = None

    # Get data from form
    file = request.files.get('transcript_file')
    text_area_content = request.form.get('transcript_text', '').strip()

    # Strategy: Prioritize file if provided and valid. 
    # If file is problematic or empty, try text area content.

    if file and file.filename != '':
        # A file has been uploaded
        if file.mimetype == 'text/plain' or \
           file.filename.endswith('.txt') or \
           file.mimetype == 'application/octet-stream': # Common for .txt uploads
            try:
                file_content = file.read().decode('utf-8')
                if file_content.strip():
                    transcript_text = file_content.strip()
                # If file is empty, transcript_text remains empty, will check text_area_content next
            except UnicodeDecodeError:
                error_message = "Error decoding file. Please ensure it's a UTF-8 encoded text file."
                # Fall through to check text_area_content
            except Exception as e:
                error_message = f"Error reading file: {str(e)}"
                # Fall through to check text_area_content
        else:
            error_message = "Invalid file type. Please upload a .txt file."
            # Fall through to check text_area_content

    # If transcript_text is not set from file (no file, empty file, or file error) 
    # AND text_area_content is available, use text_area_content.
    if not transcript_text and text_area_content:
        transcript_text = text_area_content
        error_message = None # Clear any previous file-related error if text area provides valid content

    # Final validation after attempting both sources
    if not transcript_text:
        # If transcript_text is still empty, use existing error_message or a generic one
        if not error_message:
            error_message = "No transcript content provided. Please upload a file or paste text."
        return render_template('index.html', error=error_message)
    
    # If an error_message was set (e.g. invalid file type) but transcript_text was subsequently 
    # populated (e.g. from text area), we should proceed if transcript_text is valid.
    # The logic above (error_message = None) handles clearing it if text area is used successfully.
    # However, if an error occurred AND transcript_text is still empty, then we show error.
    if error_message and not transcript_text: # This should be caught by the block above
        return render_template('index.html', error=error_message)

    # Generate summary using the summarizer module
    summary_data = generate_summary(transcript_text)
    
    # Pass the summary data to the summary display page
    return render_template('summary_display.html', summary=summary_data)

if __name__ == '__main__':
    # This block is for direct execution (e.g., `python app.py`)
    # The startup.sh script will use `flask run` or gunicorn, which handles port and host.
    app.run(host='0.0.0.0', port=9000, debug=False) 
