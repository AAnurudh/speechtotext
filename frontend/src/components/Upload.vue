<template>
    <div>
      <input type="file" @change="handleFileUpload" />
      <button @click="submitFile">Upload</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        file: null,
      };
    },
    methods: {
      handleFileUpload(event) {
        this.file = event.target.files[0];
      },
      async submitFile() {
        const formData = new FormData();
        formData.append('file', this.file);
        try {
          const response = await fetch('/api/transcribe', {
            method: 'POST',
            body: formData,
          });
          const data = await response.json();
          console.log(data);  // Output transcription/translation
        } catch (error) {
          console.error('Error:', error);
        }
      },
    },
  };
  </script>
  