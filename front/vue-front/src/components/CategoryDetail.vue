<template>
  <div class="category-container">
    <div class="category-header">
      <h1 class="collection-title">{{category.name}} Collection</h1>
    </div>
    <div class="top-menu">
      <div v-if="isOwner" class="edit-group">
        <a v-if="!isEditingName" class="add-movie-after" @click="startEditingName" >
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            이름 수정
        </a>
        <!-- <button @click="startEditingName" v-if="!isEditingName" class="edit-btn">이름 수정</button> -->
        <input
        v-if="isEditingName"
        v-model="newCategoryName"
        type="text"
        class="edit-category-input"
        placeholder="새 컬렉션 이름 입력"
        />
        <a v-if="isEditingName" class="add-movie-after" @click="saveCategoryName" >
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            저장
        </a>
        <a v-if="isEditingName" class="add-movie-after" @click="cancelEditingName" >
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            취소
        </a>
        <a class="add-movie-after" @click="openAddMovieModal" >
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            이 컬렉션에 영화 추가
        </a>
        <a class="add-movie-after" @click="deleteCategory" >
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            컬렉션 삭제
        </a>
        <!-- <button v-if="isEditingName" @click="saveCategoryName" class="save-btn">저장</button> -->
        <!-- <button v-if="isEditingName" @click="cancelEditingName" class="cancel-btn">취소</button> -->
        <!-- <button @click="openAddMovieModal" class="add-movie-btn">이 컬렉션에 영화 추가</button> -->
        <!-- <button @click="deleteCategory" class="delete-category-btn">컬렉션 삭제</button> -->
      </div>
    </div>

    <!-- 영화 추가 모달 -->
    <div v-if="showAddMovieModal" class="modal">
      <div class="modal-content">
        <h2>영화 검색</h2>
        <input v-model="searchQuery" @input="searchMovies" placeholder="영화 제목 입력" />
        <ul>
          <li v-for="movie in searchResults" :key="movie.id">
            {{ movie.title }}
            <button @click="confirmAddMovie(movie)">추가</button>
          </li>
        </ul>
        <button @click="closeAddMovieModal" class="close-modal-btn">닫기</button>
      </div>
    </div>

    <div v-if="movies.length === 0" class="plz-pass">
      <p>이 컬렉션에 추가된 영화가 없습니다.</p>
    </div>

    <div v-else class="movie-list">
      <div
        v-for="movie in movies"
        :key="movie.id"
        class="movie-card"
        @click="goToMovieDetail(movie.id)"
      >
        <!-- 영화 포스터 -->
        <div class="image-container">
          <img 
            :src="movie.poster_url ? getFullPosterUrl(movie.poster_url) : 'http://127.0.0.1:8000/media/default_movies/default-movie.png'" 
            alt="영화 포스터" 
            class="movie-poster" 
          />
        </div>
        <!-- 영화 정보 -->
        <h3>{{ movie.title }}</h3>
        <p>개봉일: {{ movie.release_date }}</p>
        <button 
          v-if="isOwner" 
          @click.stop="removeMovie(movie.id)" 
          class="remove-movie-btn"
        >삭제</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const category = ref({}); // 컬렉션 데이터
const movies = ref([]); // 영화 데이터
const store = useCounterStore();
const showAddMovieModal = ref(false);
const searchQuery = ref(""); // 영화 검색어
const searchResults = ref([]); // 검색 결과
const isEditingName = ref(false); // 이름 수정 상태
const newCategoryName = ref(""); // 새로운 컬렉션 이름

const startEditingName = () => {
  isEditingName.value = true;
};

const saveCategoryName = async () => {
  if (!newCategoryName.value.trim()) {
    alert("새 컬렉션 이름을 입력해주세요.");
    return;
  }
  try {
    const response = await axios.patch(
      `${store.API_URL}/accounts/categories/${category.value.id}/update/`,
      { name: newCategoryName.value.trim() },
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    category.value.name = response.data.name;
    isEditingName.value = false; // 저장 후 수정 모드 종료
    alert("컬렉션 이름이 수정되었습니다.");
  } catch (error) {
    console.error("Error saving category name:", error);
    alert("컬렉션 이름 저장에 실패했습니다.");
  }
};

const cancelEditingName = () => {
  newCategoryName.value = category.value.name; // 기존 이름 복원
  isEditingName.value = false; // 수정 모드 종료
};


// 현재 로그인한 유저와 컬렉션 소유자 비교
const isOwner = computed(() => store.user?.id === category.value?.owner_id); // owner_id는 백엔드에서 반환

// 포스터 URL을 처리하는 함수
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500"; // TMDB 이미지 베이스 URL
  return `${baseUrl}${posterUrl}`;
};

// 컬렉션 상세 데이터 가져오기
const fetchCategoryDetails = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/accounts/categories/${route.params.categoryId}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );

    console.log("Category Details Response:", response.data); // 응답 데이터 로깅
    category.value = response.data;
    movies.value = response.data.movies; // 영화 데이터 설정
    newCategoryName.value = response.data.name; // 기존 이름 설정
  } catch (error) {
    console.error("Error fetching category details:", error);
  }
};

// 영화 삭제 함수
const removeMovie = async (movieId) => {
  try {
    await axios.post(
      `http://127.0.0.1:8000/accounts/categories/remove-movie/`,
      {
        category_id: route.params.categoryId,
        movie_id: movieId,
      },
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    movies.value = movies.value.filter((movie) => movie.id !== movieId);
    alert("영화가 삭제되었습니다.");
  } catch (error) {
    console.error("Error removing movie:", error);
  }
};

// 영화 디테일 페이지로 이동
const goToMovieDetail = (movieId) => {
  router.push({ name: "MovieDetail", params: { id: movieId } });
};

// 영화 추가 모달 열기/닫기
const openAddMovieModal = () => (showAddMovieModal.value = true);
const closeAddMovieModal = () => {
  showAddMovieModal.value = false;
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
    const response = await axios.get(`${store.API_URL}/accounts/movies/search/`, {
      params: { title: searchQuery.value.trim() },
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });
    searchResults.value = response.data;
  } catch (error) {
    console.error("Error searching movies:", error);
  }
};

// 영화 추가 확인 및 추가
const confirmAddMovie = async (movie) => {
  const confirmed = confirm(`영화 "${movie.title}"를 컬렉션에 추가하시겠습니까?`);
  if (confirmed) {
    await addMovieToCategory(movie);
  }
};

// 영화 추가
const addMovieToCategory = async (movie) => {
  try {
    await store.addMovieToCategory(route.params.categoryId, movie.id);
    await fetchCategoryDetails(); // 컬렉션 데이터 갱신
    closeAddMovieModal();
  } catch (error) {
    console.error("Error adding movie to category:", error);
  }
};

// **컬렉션 삭제 함수**
const deleteCategory = async () => {
  const confirmed = confirm("진짜 삭제하시겠습니까?");
  if (confirmed) {
    try {
      await axios.delete(
        `${store.API_URL}/accounts/categories/${category.value.id}/delete/`,
        {
          headers: {
            Authorization: `Token ${store.token}`,
          },
        }
      );
      alert("컬렉션이 삭제되었습니다.");
      router.push(`/profile/${store.user.username}`);
    } catch (error) {
      console.error("Error deleting category:", error);
      alert("컬렉션 삭제에 실패했습니다.");
    }
  }
};

// 컴포넌트 마운트 시 데이터 로드
onMounted(async () => {
  try {
    await fetchCategoryDetails();
    await store.fetchUser()
    await store.fetchUserPoints(); // 사용자 포인트 정보 가져오기
    console.log("isOwner:", isOwner.value);
    console.log("store.user:", store.user);
    console.log("category.value:", category.value);


  } catch (error) {
    console.error("Error in onMounted:", error);
  }
});
</script>

<style scoped>

/* 컬렉션 페이지 전체 레이아웃에 패딩 추가 */
.category-container {
  padding: 0 230px; /* 양쪽에 40px 패딩 추가 */
}

/* 왼쪽 상단으로 이동 및 스타일 수정 */
.category-header {
  position: relative; /* 상대 위치 지정 */
  top: 50px; /* 상단에서 50px 아래로 */
  left: 50px; /* 왼쪽에서 50px 오른쪽으로 */
}

.collection-title {
  font-size: 2.5rem; /* 글씨 크기 키움 */
  font-weight: bold; /* 두꺼운 글씨 */
  color: #e02ff0; /* 네온 핑크와 일치하는 색상 */
  text-shadow: 0 0 2px #e02ff0, 0 0 4px #e02ff0, 0 0 6px #e02ff0;
  font-family: 'Arial', sans-serif; /* 깔끔하고 현대적인 글씨체 */
  animation: neon-flicker 2s infinite; /* 깜빡이는 애니메이션 */
}

/* 깜빡이는 네온 효과 애니메이션 */
@keyframes neon-flicker {
  0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
    text-shadow: 0 0 2px #e02ff0, 0 0 4px #e02ff0, 0 0 6px #e02ff0;
    opacity: 1;
  }
  20%, 24%, 55% {
    text-shadow: 0 0 1px #e02ff0, 0 0 2px #e02ff0, 0 0 3px #e02ff0;
    opacity: 0.8;
  }
  22% {
    text-shadow: 0 0 4px #ff00ff, 0 0 8px #ff00ff, 0 0 12px #ff00ff;
    opacity: 0.6;
  }
}



/* 상단 메뉴 스타일 */
.top-menu {
  display: flex;
  justify-content: flex-end; /* 오른쪽 정렬 */
  gap: 10px; /* 버튼 간 간격 */
  padding: 10px 20px; /* 상단 여백 */
  position: relative;
  top: 10px; /* 페이지 상단에서 떨어진 거리 */
  right: 0;
  padding-right: 38px;
}

.edit-group {
  display: flex;
  align-items: center;
  gap: 15px; /* 요소 간격 */
}

.inline-group {
  display: flex;
  align-items: center;
  gap: 10px; /* 텍스트 박스와 버튼 간 간격 */
}

.category-title {
  text-align: center; /* 중앙 정렬 */
  margin-top: 60px; /* 상단 메뉴와의 간격 */
  font-size: 24px;
  color: #fff; /* 텍스트 색상 */
}

/* 모달 스타일 */
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
  background: #e02ff0; /* 기본 버튼 색상 */
  color: white;
  border: none;
  padding: 5px 10px; /* 버튼 크기 축소 */
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.modal-content ul li button:hover {
  background: #e02ff0; /* 호버 시 약간 어두운 색상 */
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
/* 영화 리스트 */
.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px; /* 카드 간 간격 */
  justify-content: center; /* 카드들을 가운데 정렬 */
  padding: 20px 0; /* 리스트 위아래 여백 추가 */
}


.movie-card {
  border: 2px solid #e02ff0; /* 네온 테두리 */
  border-radius: 10px;
  padding: 15px;
  background-color: rgba(15, 15, 15, 0.9); /* 반투명 어두운 배경 */
  width: 250px; /* 카드 크기 */
  box-shadow: 0 0 15px rgba(224, 47, 240, 0.6); /* 네온 효과 */
  transition: transform 0.3s, box-shadow 0.3s;
  text-align: center; /* 텍스트 가운데 정렬 */
  position: relative; /* 삭제 버튼을 정렬하기 위해 필요 */
}

.movie-card:hover {
  transform: scale(1.05); /* 호버 시 확대 */
  box-shadow: 0 0 30px rgba(224, 47, 240, 0.9); /* 네온 효과 강화 */
}

.movie-card h3 {
  margin: 10px 0 5px; /* 제목 간격 */
  font-size: 1.2em;
  color: #fff; /* 흰색 텍스트 */
  font-weight: bold;
}

.movie-card p {
  font-size: 0.9em;
  color: #aaa; /* 부드러운 텍스트 색상 */
  margin-bottom: 20px; /* 제목과 개봉일 간 간격 */
}

.image-container {
  width: 100%;
  height: 300px;
  overflow: hidden;
  border-radius: 10px; /* 카드와 동일한 둥근 모서리 */
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 포스터가 카드에 맞게 조정 */
  border-radius: 10px; /* 이미지 둥근 모서리 */
}

.remove-movie-btn {
  position: absolute; /* 버튼을 카드 내에서 절대 위치 */
  bottom: 5px; /* 카드 하단에서 15px 위로 배치 */
  right: 5px; /* 카드 오른쪽에서 15px 안쪽으로 배치 */
  background: #e02ff0;
  color: #050801;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  font-size: 0.8em;
  cursor: pointer;
  transition: background 0.3s;
}

.remove-movie-btn:hover {
  background: rgba(224, 47, 240, 0.8);
  color: white;
}


/* 기존 네온 버튼 스타일과 통일된 텍스트 박스 스타일 */
.edit-category-input {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
  color: #e02ff0;
  background: transparent;
  border: 2px solid #e02ff0;
  border-radius: 4px;
  outline: none;
  transition: 0.5s;
  letter-spacing: 1px;
  overflow: hidden;
  margin-right: 20px;
  margin-top: 0px;
  margin-bottom: 10px;
}

.edit-category-input:focus,
.edit-category-input:hover {
  background: #e02ff0;
  color: #050801;
  box-shadow: 0 0 5px #e02ff0, 0 0 25px #e02ff0, 0 0 50px #e02ff0,
    0 0 200px #e02ff0;
}

.edit-category-input::placeholder {
  color: #e02ff0;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.edit-category-input::placeholder {
  color: #e02ff0;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

/* 네온 버튼 스타일 */
a {
  position: relative;
  display: inline-block;
  padding: 15px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
    margin: 50px 0; /* 여백 조정 */
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

.plz-pass {
  padding-top: 100px;
  padding-left: 50px;
}
</style>
