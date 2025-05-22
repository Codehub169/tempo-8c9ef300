from flask import Flask, render_template, request
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
        if file.filename.endswith('.txt') or \
           file.mimetype in {'text/plain', 'application/octet-stream'}:
            try:
                file_content = file.read().decode('utf-8')
                if file_content.strip():
                    transcript_text = file_content.strip()
                # If file is empty or only whitespace, transcript_text remains "", 
                # allowing fallback to text_area_content.
            except UnicodeDecodeError:
                error_message = "Error decoding file. Please ensure it's a UTF-8 encoded text file."
                # Fall through to check text_area_content
            except Exception as e:
                app.logger.error(f"Error reading file: {e}") # Log the actual exception
                error_message = "Error reading file: An unexpected error occurred."
                # Fall through to check text_area_content
        else:
            error_message = "Invalid file type. Please upload a .txt file."
            # Fall through to check text_area_content

    # If transcript_text (from file) is effectively empty and text_area_content is available, use text_area_content.
    if not transcript_text.strip() and text_area_content:
        transcript_text = text_area_content # text_area_content is already stripped
        error_message = None # Clear any previous file-related error if text area provides valid content

    # Final validation after attempting both sources
    if not transcript_text.strip():
        # If transcript_text is still effectively empty, use existing error_message or a generic one
        if not error_message:
            error_message = "No transcript content provided. Please upload a file or paste text."
        return render_template('index.html', error=error_message, previous_text_input=request.form.get('transcript_text', ''))
    
    # At this point, transcript_text has been validated to contain non-whitespace content.
    # It's also been assigned from a .strip() operation from either file or text area.
    summary_data = generate_summary(transcript_text)
    
    # Pass the summary data to the summary display page
    return render_template('summary_display.html', summary_data=summary_data)

if __name__ == '__main__':
    # This block is for direct execution (e.g., `python app.py`)
    # The startup.sh script will use `flask run` or gunicorn, which handles port and host.
    app.run(host='0.0.0.0', port=9000, debug=False)
