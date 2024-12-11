<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/upload">Voice-to-text</router-link> |
      <router-link to="/chat">Video Chat</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style scoped>
nav {
  text-align: center;
  margin: 20px;
}

nav a {
  color: #3498db;
  text-decoration: none;
  margin: 0 10px;
  font-weight: bold;
}

nav a:hover {
  text-decoration: underline;
}
</style>
