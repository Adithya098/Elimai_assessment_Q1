// app.js

/*
Handles audio recording and file upload for transcription. 
Enables live recording via MediaRecorder API with start/stop controls,
uploads audio files, sends audio data to backend API for transcription,
and displays transcribed text and structured data with user-friendly status updates.
*/

// Global variables to store MediaRecorder instance and audio chunks
let mediaRecorder;
let audioChunks = [];

// DOM elements references for playback, status messages, controls, and output display
const audioPlayer = document.getElementById('audioPlayer');
const statusText = document.getElementById('status');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const jsonOutput = document.getElementById('jsonOutput');
const fileInput = document.getElementById('fileInput'); // Upload input element

// Function to start recording
async function startRecording() {
  try {
    // Clear previous recording
    audioChunks = [];
    statusText.textContent = 'Recording...';
    statusText.className = 'recording';
    jsonOutput.textContent = ''; // Clear previous output

    // Request microphone access and create MediaRecorder instance
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    // Collect audio data chunks during recording
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        audioChunks.push(e.data);
      }
    };


    // When recording stops, process the recorded audio
    mediaRecorder.onstop = async () => {
      // Stop all tracks to release the microphone
      stream.getTracks().forEach(track => track.stop());
      
      const blob = new Blob(audioChunks, { type: 'audio/webm' });
      const audioUrl = URL.createObjectURL(blob);
      
      // Preview the audio file
      audioPlayer.style.display = 'block';
      audioPlayer.src = audioUrl;

      // Prepare the form data for sending to the backend
      const formData = new FormData();
      formData.append('file', blob, 'recording.webm');
      formData.append('language', 'en-US');

      // Show loading text while waiting for the transcription response
      statusText.textContent = 'Processing audio...';
      statusText.className = 'processing';

      try {
        // Send the audio file to the backend for transcription
        const backendBaseURL = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
        const response = await fetch(`${backendBaseURL}/api/transcribe/file`, {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // Show success status
        statusText.textContent = 'Transcription completed successfully!';
        statusText.className = 'success';

        // alert("Transcription:\n" + result.transcription);

        // Show the transcription and structured data with no gap between header and data
        jsonOutput.innerHTML = `
          <p><strong>Transcription:</strong> ${result.transcription}</p>
          <p><strong>Structured Data:</strong> ${JSON.stringify(result.structured_data, null, 2)}</p>
        `;

        
      } catch (error) {
        console.error("Error during transcription:", error);
        statusText.textContent = 'Error occurred during transcription.';
        statusText.className = 'error';
        
        // Show error details in JSON output
        jsonOutput.textContent = `Error: ${error.message}`;
        
        alert("Error occurred while sending the audio for transcription: " + error.message);
      }
    };

    // Start recording and update the UI: disable "Start" button and enable "Stop" button
    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
    } 

    catch (err) {
      console.error("Error starting recording:", err);
      statusText.textContent = 'Error accessing microphone. Please check your device and permissions.';
      statusText.className = 'error';
      
      if (err.name === 'NotAllowedError') {
        alert('Microphone access was denied. Please allow microphone access and try again.');
      } else if (err.name === 'NotFoundError') {
        alert('No microphone found. Please check your device.');
      } else {
        alert('Error accessing microphone: ' + err.message);
      }
    }
}

// Upload and transcribe an audio file selected by the user
async function uploadFile(event) {
  const file = event.target.files[0];
  if (!file) {
    alert("No file selected. Please choose an audio file.");
    return;
  }

  // Check if the uploaded file is an audio file
  if (!file.type.startsWith('audio/')) {
    alert("Please upload a valid audio file.");
    return;
  }

  // Show loading text while waiting for the transcription response
  statusText.textContent = 'Processing audio...';
  statusText.className = 'processing';
  jsonOutput.textContent = '';

  // Prepare the form data for sending to the backend
  const formData = new FormData();
  formData.append('file', file);
  formData.append('language', 'en-US');

  try {
    // Send the audio file to the backend for transcription
      const backendBaseURL = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
      const response = await fetch(`${backendBaseURL}/api/transcribe/file`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    // Show success status
    statusText.textContent = 'Transcription completed successfully!';
    statusText.className = 'success';

    // **Removed the alert** here
    // alert("Transcription:\n" + result.transcription);

    // **Show the transcription and structured data with no gap between header and data**
    jsonOutput.innerHTML = `
      <p><strong>Transcription:</strong> ${result.transcription}</p>
      <p><strong>Structured Data:</strong> ${JSON.stringify(result.structured_data, null, 2)}</p>
    `;


  } catch (error) {
    console.error("Error during transcription:", error);
    statusText.textContent = 'Error occurred during transcription.';
    statusText.className = 'error';
    
    // Show error details in JSON output
    jsonOutput.textContent = `Error: ${error.message}`;
    
    alert("Error occurred while sending the audio for transcription: " + error.message);
  }
}

// Stop the current recording session
function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
    statusText.textContent = 'Stopping recording...';
    statusText.className = 'processing';
    startBtn.disabled = false;
    stopBtn.disabled = true;
  }
} 

// Keyboard shortcuts: spacebar toggles start/stop recording when focused on body
window.startRecording = startRecording;
window.stopRecording = stopRecording;
window.uploadFile = uploadFile;

// Optional: Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
  if (e.code === 'Space' && !startBtn.disabled && e.target === document.body) {
    e.preventDefault();
    startRecording();
  } else if (e.code === 'Space' && !stopBtn.disabled && e.target === document.body) {
    e.preventDefault();
    stopRecording();
  }
});

// Prevent spacebar default scrolling when used for recording controls
document.addEventListener('keydown', (e) => {
  if (e.code === 'Space' && e.target === document.body) {
    e.preventDefault();
  }
});