<template>
  <div class="review-container">
    <h1 class="title">리뷰 작성</h1>

    <button @click="goBack" class="cancel-btn">리뷰 작성 취소</button>

    <!-- '리뷰 작성할 영화 선택하기' 버튼 -->
    <div class="select-movie-btn-container">
      <button @click="openMovieSelectModal" class="select-movie-btn">리뷰 작성할 영화 선택하기</button>
    </div>

    <!-- 영화 추가 모달 -->
    <div v-if="showMovieModal" class="modal">
      <div class="modal-content">
        <h2>영화 검색</h2>
        <input v-model="searchQuery" @input="searchMovies" placeholder="영화 제목 입력" />
        <ul>
          <li v-for="movie in searchResults" :key="movie.id">
            {{ movie.title }}
            <button @click="selectMovie(movie)">추가</button>
          </li>
        </ul>
        <button @click="closeMovieModal" class="close-modal-btn">닫기</button>
      </div>
    </div>

    <!-- 선택한 영화 포스터 및 타이틀 표시 -->
    <div v-if="selectedMovie" class="selected-movie">
      <h3>선택한 영화: {{ selectedMovie.title }}</h3>
      <img :src="selectedMoviePoster" alt="선택된 영화 포스터" class="poster-image" />
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

    <!-- 게시글 작성 폼 -->
    <form @submit.prevent="createArticle" class="form-container">
      <div class="form-group">
        <input
          type="text"
          v-model.trim="title"
          class="form-input styled-input"
          placeholder="제목을 입력하세요"
        />
      </div>
      <div class="form-group">
        <textarea
          v-model.trim="content"
          class="form-textarea styled-textarea"
          placeholder="내용을 입력하세요"
        ></textarea>
      </div>
      <button type="submit" class="submit-btn">작성</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

// 상태 정의
const title = ref("");
const content = ref("");
const searchQuery = ref("");
const searchResults = ref([]);
const selectedMovie = ref(null); // 선택된 영화 객체
const selectedMoviePoster = ref(null); // 선택된 영화의 포스터 URL
const errorMessage = ref("");
const showMovieModal = ref(false);
const hoverRating = ref(0);
const selectedRating = ref(0);

const store = useCounterStore();
const router = useRouter();

const goBack = () => {
  router.go(-1);
};

// 모달 열기/닫기
const openMovieSelectModal = () => (showMovieModal.value = true);
const closeMovieModal = () => {
  showMovieModal.value = false;
  searchQuery.value = "";
  searchResults.value = [];
};

// 영화 검색
const searchMovies = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = [];
    return;
  }

  try {
    const response = await store.searchMovies(searchQuery.value.trim());
    searchResults.value = response;
  } catch (error) {
    console.error("Error searching movies:", error);
    errorMessage.value = "영화를 검색하는데 실패했습니다.";
  }
};

// 영화 선택
const selectMovie = (movie) => {
  selectedMovie.value = movie; // 선택된 영화 객체 저장
  selectedMoviePoster.value = `https://image.tmdb.org/t/p/w500${movie.poster_url}`; // 포스터 URL 저장
  closeMovieModal();
};

// 별점 관련 함수
const hoverStar = (value) => (hoverRating.value = value);
const clearHover = () => (hoverRating.value = 0);
const selectRating = (rating) => (selectedRating.value = rating);

// 게시글 작성
const isSubmitting = ref(false);

const createArticle = async () => {
  if (isSubmitting.value) return; // 이미 요청 중이면 중지
  isSubmitting.value = true;

  if (!selectedMovie.value) {
    alert("리뷰 작성할 영화를 선택해주세요.");
    isSubmitting.value = false;
    return;
  }

  try {
    const newArticle = await store.createArticle({
      title: title.value,
      content: content.value,
      poster_url: selectedMoviePoster.value,
      rating: selectedRating.value,
      movie: selectedMovie.value.id,
    });

    // 작성된 리뷰를 프론트엔드의 상태에 추가
    store.articles.unshift(newArticle);  // 최신순으로 추가
    await store.fetchUserPoints(); // 사용자 정보를 다시 가져와 업데이트
    alert("리뷰가 성공적으로 작성되었습니다.");
    router.push({ name: "ArticleView" });
  } catch (error) {
    console.error("Error creating article:", error);
    alert("리뷰 작성에 실패했습니다.");
  } finally {
    isSubmitting.value = false; // 요청 완료 후 플래그 초기화
  }
};

</script>


<style scoped>
.review-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: #121212;
  color: #fff;
  border-radius: 8px;
}
/* 공통 스타일 */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 제목 입력 필드 스타일 */
.styled-input {
  width: 100%;
  padding: 15px;
  font-size: 18px;
  font-weight: bold;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #222; /* 어두운 배경 */
  color: #fff;
  box-sizing: border-box;
}

.styled-input::placeholder {
  color: #888; /* 플레이스홀더 색상 */
  font-weight: normal;
}

/* 내용 입력 필드 스타일 */
.styled-textarea {
  width: 100%;
  padding: 15px;
  font-size: 16px;
  line-height: 1.5;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #222; /* 어두운 배경 */
  color: #fff;
  min-height: 150px; /* 최소 높이 */
  resize: vertical; /* 사용자가 높이 조정 가능 */
  box-sizing: border-box;
}

.styled-textarea::placeholder {
  color: #888; /* 플레이스홀더 색상 */
  font-weight: normal;
}

/* 입력 필드 포커스 효과 */
.styled-input:focus,
.styled-textarea:focus {
  outline: none;
  border-color: #ff9800; /* 포커스 시 강조 색상 */
  box-shadow: 0 0 5px rgba(255, 152, 0, 0.7); /* 포커스 시 외곽선 */
}

/* 작성 버튼 */
.submit-btn {
  background: #ff9800;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn:hover {
  background: #e88e00;
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

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6); /* 어두운 반투명 배경 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 모달이 항상 위에 보이도록 설정 */
}

.modal-content {
  background: #2b2b2b; /* 어두운 배경 */
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  color: #fff;
  position: relative; /* 닫기 버튼 배치를 위한 설정 */
  display: flex;
  flex-direction: column; /* 내부 요소를 세로 정렬 */
  gap: 15px; /* 요소 간격 */
}
.modal-content h2 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #fff;
  text-align: center;
}

.modal-content input {
  width: 100%;
  padding: 10px;
  border: 1px solid #555;
  border-radius: 4px;
  background: #1f1f1f; /* 입력 필드 배경 */
  color: #fff;
  font-size: 14px;
}

.modal-content input::placeholder {
  color: #888;
}

.modal-content ul {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 200px; /* 리스트의 최대 높이를 제한 */
  overflow-y: auto; /* 스크롤이 필요한 경우 표시 */
}

.modal-content ul li {
  display: flex;
  justify-content: space-between; /* 추가 버튼과 영화 제목 간격 유지 */
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #444; /* 리스트 아이템 구분선 */
  font-size: 16px;
}

.modal-content ul li:last-child {
  border-bottom: none; /* 마지막 아이템의 테두리 제거 */
}

.modal-content ul li button {
  background: #ff9800; /* 기본 버튼 색상 */
  color: white;
  border: none;
  padding: 5px 10px; /* 버튼 크기 축소 */
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.modal-content ul li button:hover {
  background: #e88e00; /* 호버 시 약간 어두운 색상 */
}

.close-modal-btn {
  align-self: flex-end; /* 닫기 버튼을 오른쪽으로 정렬 */
  background: #d32f2f; /* 닫기 버튼 색상 */
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.close-modal-btn:hover {
  background: #b71c1c; /* 닫기 버튼 호버 색상 */
}
.selected-movie {
  text-align: center;
  margin: 20px 0;
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
  gap: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 16px;
  margin-bottom: 5px;
}

.form-input,
.form-textarea {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-btn {
  background: #ff9800;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
