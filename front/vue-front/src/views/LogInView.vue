<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">로그인</h1>
      <form @submit.prevent="logIn" class="login-form">
        <div class="form-group">
          <label for="username" class="form-label">이름</label>
          <input type="text" id="username" v-model.trim="username" placeholder="사용하실 이름을 적어주세요." class="form-input">
        </div>
        <div class="form-group">
          <label for="password" class="form-label">비밀번호</label>
          <input type="password" id="password" v-model.trim="password" placeholder="비밀번호를 적어주세요." class="form-input">
        </div>
        <div class="form-group submit-group">
          <input type="submit" value="Log In" class="submit-button">
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref(null)
const password = ref(null)

const store = useCounterStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}
</script>

<style>
/* 컨테이너 스타일 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh; /* 화면 높이에 맞춤 */
  font-family: Arial, sans-serif;
  padding: 1rem;
  box-sizing: border-box;
}

/* 카드 스타일 */
.login-card {
  background: #fff;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  width: 400px;
  max-width: 90%;
  height: 450px; /* 높이 축소 */
  text-align: center;
  overflow: hidden; /* 스크롤 방지 */
  display: flex;
  flex-direction: column; /* 내부 요소를 수직 정렬 */
  justify-content: space-between; /* 간격 균형 유지 */
}

/* 제목 스타일 */
.login-title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 2.5rem;
}

/* 폼 스타일 */
.login-form {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 버튼과 입력 필드 사이 균형 유지 */
}

/* 폼 그룹 스타일 */
.form-group {
  margin-bottom: 1rem;
}

/* 라벨 스타일 */
.form-label {
  display: block;
  font-weight: bold;
  color: #555;
  margin-bottom: 0.5rem;
  text-align: left;
}

/* 인풋 스타일 */
.form-input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #4b47c857;
  border-radius: 5px;
  font-size: 0.9rem;
  box-sizing: border-box;
}

/* 버튼 스타일 */
.submit-group {
  text-align: right; /* 버튼을 우측 정렬 */
}

.submit-button {
  background: #6c63ff;
  color: #fff;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.3s;
}

.submit-button:hover {
  background: #4b47c8;
}
</style>
