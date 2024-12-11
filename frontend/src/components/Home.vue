<template>
  <div class="home-container">
    <div class="content">
      <h1>Welcome to Voice-to-Text Application</h1>
      <p>
        Our application allows you to easily transcribe and translate your  video files. 
        Experience the importance of voice-to-text technology in communication, accessibility, 
        and content creation.
      </p>
      <div class="options">
        <router-link to="/upload" class="option">
          <div class="icon">📤</div>
          <span>Voice-to-Text</span>
        </router-link>
        <router-link to="/chat" class="option">
          <div class="icon">💬</div>
          <span>Video Chat</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
};
</script>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #ff7e5f, #feb47b);
  color: white;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.content {
  position: relative;
  z-index: 2;
  padding: 20px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.5);
}

.options {
  display: flex;
  justify-content: space-around;
  margin-top: 30px;
}

.option {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: white;
  text-decoration: none;
  transition: transform 0.3s;
}

.option:hover {
  transform: scale(1.1);
}

.icon {
  font-size: 50px; /* You can change this size */
}

@keyframes backgroundAnimation {
  0% { background-color: rgba(255, 126, 95, 0.5); }
  50% { background-color: rgba(254, 180, 123, 0.5); }
  100% { background-color: rgba(255, 126, 95, 0.5); }
}

/* Optional: Animated background */
.home::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #ff7e5f, #feb47b);
  animation: backgroundAnimation 10s infinite alternate;
  z-index: 1;
}
</style>
  