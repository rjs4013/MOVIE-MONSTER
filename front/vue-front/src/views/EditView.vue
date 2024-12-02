<template>
  <div class="edit-container">
    <h1 class="title">게시글 수정</h1>

    <div v-if="posterUrl" class="poster-container">
      <!-- 영화 제목 -->
      <h3 class="poster-title">선택한 영화: {{ title }}</h3>
      <!-- 영화 포스터 -->
      <img :src="posterUrl" alt="영화 포스터" class="poster-image" />
    </div>

    <!-- 별점 매기기 -->
    <div class="stars">
      <div
        v-for="n in 10"
        :key="n"
        class="star"
        :class="{ filled: n <= hoverRating || n <= selectedRating }"
        @mouseover="hoverStar(n)"
        @mouseleave="clearHover"
        @click="selectRating(n)"
      ></div>
    </div>
    <p class="rating-text">선택한 별점: {{ selectedRating }} / 10</p>

    <!-- 게시글 수정 폼 -->
    <form @submit.prevent="submitEdit" class="form-container">
      <div class="form-group">
        <input
          v-model="title"
          id="title"
          type="text"
          class="form-input styled-input"
          placeholder="제목을 입력하세요"
          required
        />
      </div>

      <div class="form-group">
        <textarea
          v-model="content"
          id="content"
          class="form-textarea styled-textarea"
          placeholder="내용을 입력하세요"
          required
        ></textarea>
      </div>

      <button type="submit" class="submit-button">수정 저장</button>
    </form>
  </div>
</template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useCounterStore } from '@/stores/counter'
  import axios from 'axios'
  
  const store = useCounterStore()
  const route = useRoute()
  const router = useRouter()
  
  const title = ref('')
  const content = ref('')
  const posterUrl = ref('') // 포스터 URL
  
  onMounted(() => {
    // 기존 게시글 내용 로드
    axios.get(`${store.API_URL}/api/v1/communities/${route.params.id}/`, {
      headers: { Authorization: `Token ${store.token}` }
    })
      .then((res) => {
        title.value = res.data.title
        content.value = res.data.content
        console.log(res.data.movie.poster_url); // 포스터 URL 출력 확인
        posterUrl.value = res.data.movie.poster_url // 포스터 URL 설정
      })
      .catch((err) => console.log(err))
  })
  
  // 수정 데이터 제출
  const submitEdit = () => {
    axios.put(`${store.API_URL}/api/v1/communities/${route.params.id}/`, {
      title: title.value,
      content: content.value,
      rating: selectedRating.value
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })
      .then(() => {
        alert('수정이 완료되었습니다.')

          // store에 있는 articles 배열 업데이트
        store.getSortedArticles('recent');
        router.push({ name: 'DetailView', params: { id: route.params.id } }) // 수정 후 상세 페이지로 이동
      })
      .catch((err) => console.log(err))
  }
  // 별점 관련 함수 ---------------

const hoverRating = ref(0); // 마우스 위치에 따라 표시되는 별점

// 마우스 오버 함수
const hoverStar = (value) => {
  hoverRating.value = value; // 마우스 위치에 따라 별점 변경
};

// 마우스 아웃 함수
const clearHover = () => {
  hoverRating.value = 0; // 마우스가 별에서 떠나면 초기화
};
const selectedRating = ref(0);

const selectRating = (rating) => {
  selectedRating.value = rating; // 선택한 별점 업데이트
};
  </script>
  
  <style scoped>
  .edit-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background: #121212;
    color: #fff;
    border-radius: 8px;
  }
  
  .title {
    text-align: center;
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .cancel-btn {
    background: #ff4d4d;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 20px;
  }
  
  .select-movie-btn-container {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .select-movie-btn {
    background: #ff9800;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .poster-container {
    text-align: center;
    margin: 20px 0;
  }
  
  .poster-title {
    margin-bottom: 10px;
    font-size: 16px;
    font-weight: bold;
  }
  
  .poster-image {
    max-width: 200px;
    height: auto;
    display: block;
    margin: 10px auto;
    border-radius: 8px;
  }
  
  .stars {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
  }
  
  .star {
    width: 24px;
    height: 24px;
    background: url("/assets/images/gray-star.png") no-repeat center;
    background-size: contain;
    cursor: pointer;
  }
  
  .star.filled {
    background: url("/assets/images/yellow-star.png") no-repeat center;
    background-size: contain;
  }
  
  .rating-text {
    text-align: center;
  }
  
  .form-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
  }
  
  .styled-input,
  .styled-textarea {
    width: 100%;
    padding: 15px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 6px;
    background: #222;
    color: #fff;
  }
  
  .styled-input::placeholder,
  .styled-textarea::placeholder {
    color: #888;
  }
  
  .styled-input:focus,
  .styled-textarea:focus {
    outline: none;
    border-color: #ff9800;
    box-shadow: 0 0 5px rgba(255, 152, 0, 0.7);
  }
  
  .styled-textarea {
    min-height: 150px;
    resize: vertical;
  }
  
  .submit-button {
    padding: 10px;
    font-size: 16px;
    color: #fff;
    background-color: #ff9800;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    text-align: center;
  }
  
  .submit-button:hover {
    background-color: #e88e00;
  }
  </style>
  