<template>
    <div class="modal">
      <div class="modal-content">
        <h2>영화 추가</h2>
        <input
          v-model="searchTitle"
          placeholder="영화 제목을 입력하세요"
          class="search-input"
          @keyup.enter="searchMovies"
        />
        <button @click="searchMovies" class="search-btn">검색</button>
  
        <div v-if="searchResults.length">
          <h3>검색 결과:</h3>
          <ul>
            <li v-for="movie in searchResults" :key="movie.id">
              {{ movie.title }}
              <button @click="selectMovie(movie)" class="select-btn">추가</button>
            </li>
          </ul>
        </div>
  
        <div v-if="selectedMovie">
          <p>{{ selectedMovie.title }}를 컬렉션에 추가하시겠습니까?</p>
          <button @click="confirmAddMovie" class="confirm-btn">예</button>
          <button @click="cancelAddMovie" class="cancel-btn">아니오</button>
        </div>
  
        <button @click="$emit('close')" class="close-btn">닫기</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useCounterStore } from "@/stores/counter";
  
  const store = useCounterStore();
  
  const searchTitle = ref("");
  const searchResults = ref([]);
  const selectedMovie = ref(null);
  
  // 영화 검색
  const searchMovies = async () => {
    searchResults.value = await store.searchMovies(searchTitle.value);
  };
  
  // 영화 선택
  const selectMovie = (movie) => {
    selectedMovie.value = movie;
  };
  
  // 추가 확인
  const confirmAddMovie = () => {
    $emit("movieSelected", selectedMovie.value);
    selectedMovie.value = null;
  };
  
  // 추가 취소
  const cancelAddMovie = () => {
    selectedMovie.value = null;
  };
  </script>
  
  <style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
  }
  
  .search-input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
  }
  
  .search-btn, .close-btn, .select-btn, .confirm-btn, .cancel-btn {
    padding: 8px 16px;
    margin: 5px;
  }
  </style>
  