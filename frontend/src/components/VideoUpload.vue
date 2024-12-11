<template>
  <div class="upload-container">
    <h2>Upload Your Video</h2>
    <p>Upload your video to get started with transcription and translation.</p>

    <!-- File input for selecting video file -->
    <input type="file" @change="onFileChange" accept="video/*" />

    <!-- Upload button, disabled until a file is selected -->
    <button @click="uploadFile" :disabled="!selectedFile || loading">
      {{ loading ? 'Processing...' : 'Upload' }}
    </button>

    <!-- Loader to indicate processing -->
    <div v-if="loading" class="loader">Processing your file...</div>

    <!-- Display error if there is an issue -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Show transcription, translation, summarization, and download link after processing -->
    <div v-if="transcription || translation || summarization || downloadLink" class="results">
      <div class="result">
        <h3 v-if="transcription">Transcription:</h3>
        <p v-if="transcription">{{ transcription }}</p>
        <a v-if="transcription" :href="transcriptionUrl" download>Download Transcription</a>
      </div>
      
      <div class="result">
        <h3 v-if="translation">Translation:</h3>
        <p v-if="translation">{{ translation }}</p>
        <a v-if="translation" :href="translationUrl" download>Download Translation</a>
      </div>

      <div class="result">
        <h3 v-if="summarization">Summarization:</h3>
        <p v-if="summarization">{{ summarization }}</p>
        <a v-if="summarizationUrl" :href="summarizationUrl" download>Download Summarization</a>
      </div>

      <!-- Link to download the video with subtitles -->
      <a v-if="downloadLink" :href="downloadLink" download class="download-link">Download Video with Subtitles</a>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,         // Store the selected video file
      transcription: '',          // Store the transcription text
      translation: '',            // Store the translation text
      summarization: '',          // Store the summarization text
      downloadLink: '',           // URL for downloading video with subtitles
      transcriptionUrl: '',       // URL for downloading transcription
      translationUrl: '',         // URL for downloading translation
      summarizationUrl: '',       // URL for downloading summarization
      loading: false,             // Show loading state during upload/processing
      error: ''                   // Error message handling
    };
  },
  methods: {
    // Triggered when a file is selected
    onFileChange(event) {
      this.selectedFile = event.target.files[0]; // Get the selected file
      this.error = '';                           // Reset error state
    },

    // Upload the selected file and handle transcription/translation
    async uploadFile() {
      if (!this.selectedFile) return; // Don't proceed if no file is selected

      this.loading = true;            // Start loading animation
      this.error = '';                // Reset error
      this.transcription = '';        // Reset previous transcription
      this.translation = '';          // Reset previous translation
      this.summarization = '';        // Reset previous summarization
      this.downloadLink = '';         // Reset previous download link
      this.transcriptionUrl = '';     // Reset transcription download link
      this.translationUrl = '';       // Reset translation download link
      this.summarizationUrl = '';     // Reset summarization download link

      const formData = new FormData();
      formData.append('file', this.selectedFile); // Append file to form data

      try {
        const response = await fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error('Failed to upload the file.');
        }

        const result = await response.json();
        console.log("Processing result:", result);

        // Display transcription, translation, and summarization data, and provide download URLs
        this.transcription = result.transcription || 'No transcription available.';
        this.translation = result.translation || 'No translation available.';
        this.summarization = result.summarization || 'No summarization available.';
        this.downloadLink = result.video_url || '';       // Video with subtitles
        this.transcriptionUrl = result.transcription_url; // Transcription file download URL
        this.translationUrl = result.translation_url;     // Translation file download URL
        this.summarizationUrl = result.summarization_url; // Summarization file download URL

      } catch (err) {
        console.error("Error during upload or processing:", err);
        this.error = err.message || 'An error occurred during processing.'; // Set error message
      } finally {
        this.loading = false; // Stop loading animation
      }
    }
  }
};
</script>

<style scoped>
.upload-container {
  background: linear-gradient(to right, #ff7e5f, #feb47b);
  padding: 2em;
  color: #fff;
  text-align: center;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  max-width: 600px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

h2 {
  margin-bottom: 1em;
}

input[type="file"] {
  display: block;
  margin: 1em auto;
}

button {
  margin-top: 1em;
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #2980b9;
}

button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.loader {
  color: #fff;
  font-size: 18px;
  margin-top: 20px;
  animation: fadeIn 1s ease-in-out infinite;
}

@keyframes fadeIn {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.results {
  margin-top: 20px;
}

.results .result {
  background: rgba(255, 255, 255, 0.2);
  padding: 1em;
  border-radius: 8px;
  margin: 1em 0;
  text-align: left;
}

.error {
  color: red;
  margin-top: 1em;
}

.download-link {
  display: inline-block;
  margin-top: 1em;
  padding: 10px 20px;
  background-color: #2ecc71;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
}

.download-link:hover {
  background-color: #27ae60;
}
</style>
