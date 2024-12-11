<template>
    <div class="translation-section">
      <h2>Translation</h2>
      <p>{{ translation }}</p>
    </div>
  </template>
  
  <script>
  export default {
    props: ['translation']
  };
  </script>
  
  <style>
  .translation-section {
    background: linear-gradient(to right, #a1c4fd, #c2e9fb);
    padding: 20px;
  }
  </style>
  