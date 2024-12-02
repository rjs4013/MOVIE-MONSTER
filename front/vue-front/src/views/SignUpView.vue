<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">회원가입</h1>
      <form @submit.prevent="signUp" class="login-form">
        <!-- 프로필 사진 업로드 -->
        <div class="form-group profile-container">
          <div class="profile-details">
            <label for="profilePicture" class="form-label">프로필 사진</label>
            <button type="button" class="upload-button" @click="triggerFileInput">파일 선택</button>
            <input type="file" id="profilePicture" ref="fileInput" @change="onFileChange" class="hidden-file-input">
          </div>
          <div v-if="profilePreview" class="form-preview">
            <img :src="profilePreview" alt="Profile Preview" class="profile-preview" />
          </div>
        </div>

        <!-- 기존 회원가입 필드 -->
        <div class="form-group">
          <label for="username" class="form-label">이름</label>
          <input type="text" id="username" v-model.trim="username" class="form-input">
        </div>
        <div class="form-group">
          <label for="password1" class="form-label">비밀번호</label>
          <input type="password" id="password1" v-model.trim="password1" class="form-input">
        </div>
        <div class="form-group">
          <label for="password2" class="form-label">비밀번호 확인</label>
          <input type="password" id="password2" v-model.trim="password2" class="form-input">
        </div>
        <div class="form-group submit-group">
          <input type="submit" value="Sign Up" class="submit-button">
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const username = ref('');
const password1 = ref('');
const password2 = ref('');
const profilePicture = ref(null);
const profilePreview = ref(null);
const fileInput = ref(null);

const store = useCounterStore();

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    profilePicture.value = file;
    profilePreview.value = URL.createObjectURL(file); // 미리보기 URL 생성
  }
};
const signUp = async () => {
  const formData = new FormData();
  formData.append('username', username.value);
  formData.append('password1', password1.value);
  formData.append('password2', password2.value);
  if (profilePicture.value) {
    formData.append('profile_picture', profilePicture.value);
  }

  console.log("DEBUG: FormData content:");
  for (let [key, value] of formData.entries()) {
    console.log(`${key}:`, value);
  }

  try {
    await store.signUp(formData); // 스토어에서 FormData 처리
    alert('회원가입 성공!');
  } catch (error) {
    console.error('회원가입 실패:', error);
    alert('회원가입 실패!');
  }
}
const triggerFileInput = () => {
  fileInput.value.click(); // 숨겨진 파일 입력 창 트리거
};

</script>

<style scoped>
/* 컨테이너 스타일 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
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
  height: auto;
  text-align: center;
  overflow: hidden;
  display: flex;
  flex-direction: column;
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
  justify-content: space-between;
}

/* 프로필 컨테이너 스타일 */
.profile-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

/* 프로필 세부사항 */
.profile-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* 라벨 스타일 */
.form-label {
  font-weight: bold;
  color: #555;
  margin-bottom: 0.5rem;
}

/* 숨겨진 파일 입력 */
.hidden-file-input {
  display: none;
}

/* 업로드 버튼 스타일 */
.upload-button {
  background-color: #6c63ff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s;
}

.upload-button:hover {
  background-color: #4b47c8;
}

/* 미리보기 스타일 */
.profile-preview {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #4b47c857;
  margin-right: 65px;
}

/* 폼 그룹 스타일 */
.form-group {
  margin-bottom: 1rem;
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
  text-align: right;
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
