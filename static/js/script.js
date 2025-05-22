document.addEventListener('DOMContentLoaded', function() {
    // Handle file name display for custom file input
    const fileInput = document.getElementById('transcript_file');
    const fileNameDisplay = document.getElementById('file-name-display');

    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = fileInput.files[0].name;
            } else {
                fileNameDisplay.textContent = 'No file chosen';
            }
        });
    }

    // Handle form submission validation
    const transcriptForm = document.getElementById('transcriptForm');
    if (transcriptForm) {
        transcriptForm.addEventListener('submit', function(event) {
            const fileInputElement = document.getElementById('transcript_file');
            const textInputElement = document.getElementById('transcript_text');

            // Check if file input exists and has files, or text input exists and has content
            const hasFile = fileInputElement && fileInputElement.files.length > 0;
            const hasText = textInputElement && textInputElement.value.trim() !== '';

            if (!hasFile && !hasText) {
                alert('Please upload a transcript file or paste the transcript text.');
                event.preventDefault(); // Prevent form submission
            }
            // Backend will prioritize file if both are provided.
        });
    }
});
