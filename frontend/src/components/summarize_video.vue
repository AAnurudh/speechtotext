<template>
    <div>
        <h1>Video Upload</h1>
        <input type="file" @change="onFileChange" />
        <button @click="uploadVideo">Upload and Summarize</button>
        <div v-if="summary">
            <h2>Summary</h2>
            <p>{{ summary }}</p>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            selectedFile: null,
            summary: '',
        };
    },
    methods: {
        onFileChange(event) {
            this.selectedFile = event.target.files[0];
        },
        async uploadVideo() {
            const formData = new FormData();
            formData.append('video', this.selectedFile);

            try {
                const response = await fetch('http://localhost:5000/summarize_video', {
                    method: 'POST',
                    body: formData,
                });

                const data = await response.json();
                this.summary = data.summary; // Save the summary for display
            } catch (error) {
                console.error('Error:', error);
            }
        },
    },
};
</script>
