<template>
  <div class="movie-background"></div> <!-- 배경포스터 -->
  <div class="container movie-detail">
    <div class="row">
      <!-- 좌측: 포스터 섹션 -->
      <div class="col-md-4 text-center">
        <img
          :src="getFullPosterUrl(movie.poster_url)"
          class="img-fluid rounded shadow"
          :alt="movie.title"
        />
      </div>

      <!-- 우측: 상세 정보 섹션 -->
      <div class="col-md-8">
        <h1 class="mb-3">{{ movie.title }}</h1>
        <p><strong>개봉일:</strong> {{ movie.release_date }}</p>
        <p><strong>평점:</strong> {{ movie.vote_avg }}</p>
        <p><strong>줄거리:</strong> {{ movie.description }}</p>
        <p><strong>장르:</strong> {{ movie.genres?.join(", ") }}</p>
        <p><strong>배우:</strong> {{ movie.actors?.join(", ") }}</p>
        <p><strong>감독:</strong> {{ movie.director }}</p>
        <!-- 컬렉션 추가 버튼 -->
        <div class="button-container d-flex align-items-center">
          <a href="#" @click.prevent="showCategoryModal = true">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            컬렉션 추가
          </a>
        
        <button
            type="button"
            class="btn youtube-btn"
            data-bs-toggle="modal"
            data-bs-target="#youtubeTrailerModal"
          >
        <img :src="youtubeLogo" alt="YouTube" class="youtube-logo" />
        <!-- YouTube 섹션 -->
        <!-- <div class="movie-youtube mt-4 text-center"> -->
          
            
          </button>
        </div>
        </div>
      </div>
    
    <!-- 컬렉션 추가 모달 -->
    <AddToCategoryModal
      v-if="showCategoryModal"
      :movie-id="movie.id"
      @close="showCategoryModal = false"
    />
    <YoutubeTrailerModal :movieTitle="movie.title" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios"; 
import AddToCategoryModal from "@/components/AddToCategoryModal.vue";
import youtubeLogo from "@/assets/youtubeLogo.svg";
import YoutubeTrailerModal from "@/components/YoutubeTrailerModal.vue";

const route = useRoute();

const movie = ref({}); // 영화 데이터를 저장할 객체
const showCategoryModal = ref(false); // 컬렉션 모달 상태

// TMDB 이미지 URL 생성
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500";
  return `${baseUrl}${posterUrl}`;
};

// 영화 데이터 가져오기
const fetchMovie = async () => {
  const movieId = route.params.id; // 라우터에서 영화 ID 가져오기
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/movies/${movieId}/`
    );
    movie.value = response.data; // 응답 데이터 저장

    // 배경 이미지 동적으로 설정
    const backdropUrl = `https://image.tmdb.org/t/p/original${movie.value.backdrop_url}`;
    const backgroundElement = document.querySelector(".movie-background");
    if (backgroundElement) {
      backgroundElement.style.backgroundImage = `url('${backdropUrl}')`;
    }
  } catch (error) {
    console.error("Error loading movie:", error);
  }
};

// 컴포넌트 마운트 시 영화 데이터 로드
onMounted(fetchMovie);
</script>

<style scoped>
/* 배경포스터 스타일 */
.movie-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-color: #000; /* 배경 이미지가 없을 경우 대비 */
  z-index: -2; /* app.vue의 배경색 위에 표시 */
}

/* 메인 컨테이너 */
.container {
  margin-top: 40px;
  padding: 20px;
  background-color: rgba(0, 0, 0, 0.842); /* 반투명 검은색 배경 */
  border-radius: 8px;
  color: white;
  max-width: 1200px;
  width: 90%;
  margin: 0 auto;
}

.movie-detail {
  padding: 40px;
  margin-top: 40px;
}

.row {
  align-items: center;
}

.img-fluid {
  max-height: 500px; /* 포스터 최대 높이 */
  object-fit: cover;
  margin-bottom: 20px;
}

.col-md-4 {
  margin-bottom: 20px; /* 작은 화면에서 좌측과 우측 간격 */
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
}

p {
  font-size: 1rem;
  margin-bottom: 10px;
}

.button-container {
  display: flex;
  align-items: center;
  gap: 15px; /* 버튼 사이 간격 */
}

.youtube-logo {
  width: 50px;
  height: 50px;
}

.youtube-btn {
  background: none; /* 버튼 배경 없애기 */
  border: none; /* 버튼 테두리 없애기 */
  margin-top: 20px;
  padding: 0;
  cursor: pointer;
}

.movie-youtube {
  margin-top: 20px;
  text-align: center;
}

.category-button {
  margin-top: 23px; /* Adjust this value as needed to align with the YouTube logo */
}

/* 네온 버튼 스타일 */
a {
  position: relative;
  display: inline-block;
  padding: 15px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
    margin: 20px 0; /* 여백 조정 */
  color: #e02ff0;
  text-decoration: none;
  text-transform: uppercase;
  transition: 0.5s;
  letter-spacing: 1px;
  overflow: hidden;
  margin-right: 20px;
  margin-top: 40px;
}

a:hover {
  background: #e02ff0;
  color: #050801;
  box-shadow: 0 0 5px #e02ff0, 0 0 25px #e02ff0, 0 0 50px #e02ff0,
    0 0 200px #e02ff0;
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0005);
}

a span {
  position: absolute;
  display: block;
}

a span:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #e02ff0);
  animation: animate1 1s linear infinite;
}

@keyframes animate1 {
  0% {
    left: -100%;
  }
  50%,
  100% {
    left: 100%;
  }
}

a span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #e02ff0);
  animation: animate2 1s linear infinite;
  animation-delay: 0.25s;
}

@keyframes animate2 {
  0% {
    top: -100%;
  }
  50%,
  100% {
    top: 100%;
  }
}

a span:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #e02ff0);
  animation: animate3 1s linear infinite;
  animation-delay: 0.5s;
}

@keyframes animate3 {
  0% {
    right: -100%;
  }
  50%,
  100% {
    right: 100%;
  }
}

a span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #e02ff0);
  animation: animate4 1s linear infinite;
  animation-delay: 0.75s;
}

@keyframes animate4 {
  0% {
    bottom: -100%;
  }
  50%,
  100% {
    bottom: 100%;
  }
}
</style>
