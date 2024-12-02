<template>
  <div class="container">
    <h1 class="text-center tracking-in-expand-fwd my-4">MOVIE MONSTER</h1>
    <!-- 장르 선택 -->
    <div class="genre-search-container">
    <GenreMovie @genre-selected="goToGenre" />

    <form @submit.prevent="searchMovie" class="search-bar">
      <input type="search" v-model="searchQuery" pattern=".*\S.*" required placeholder=" 영화 제목 검색" />
      <button class="search-btn" type="submit">
        <span>검색</span>
      </button>
    </form>
    </div>
    <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>

    <!-- 검색 결과 -->
    <div v-if="searchResults.length > 0" class="search-results">
      <h4>검색 결과</h4>
      <div class="grid-container">
        <div
          class="card"
          v-for="movie in searchResults"
          :key="movie.id"
          @click="goToDetail(movie.id)"
        >
          <img
            :src="getFullPosterUrl(movie.poster_url)"
            class="card-img-top"
            :alt="movie.title"
          />
        </div>
      </div>
    </div>

    <!-- 검색 결과가 없을 때만 기존 섹션 표시 -->
    <div v-else>
      <!-- <p v-if="searchQuery" class="text-center text-muted">검색 결과가 없습니다.</p> -->

      <!-- 인기/최신/개봉예정 섹션 -->
      <div v-for="section in sections" :key="section.name" class="mt-5">
        <div class="d-flex justify-content-between align-items-center">
          <h3 class="sectionpadd">{{ section.title }}</h3>
          <button class="btn-more" @click="goToMore(section.name)">
            더보기 <span class="arrow">&gt;</span>
          </button>
        </div>

        <!-- 캐러셀 -->
        <div class="carousel-wrapper">
          <button class="carousel-btn prev" @click="prevSlide(section.name)">
            &lt;
          </button>
          <div class="carousel-track-container">
            <div
              class="carousel-track"
              :style="{
                transform: `translateX(-${currentIndex[section.name] * 100}%)`,
              }"
            >
              <div
                class="carousel-slide"
                v-for="(chunk, index) in getChunks(section.movies, 5)"
                :key="index"
              >
                <div class="card" v-for="movie in chunk" :key="movie.movie_id"
                @click.stop="goToDetail(movie.movie_id)">
                  <img
                    :src="getFullPosterUrl(movie.poster_url)"
                    class="card-img-top"
                    :alt="movie.title"
                  />
                </div>
              </div>
            </div>
          </div>
          <button class="carousel-btn next" @click="nextSlide(section.name)">
            &gt;
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import GenreMovie from "@/components/GenreMovie.vue";
import axios from "axios";

export default {
  components: { GenreMovie },
  setup() {
    const router = useRouter();
    const searchQuery = ref("");
    const errorMessage = ref("");
    const searchResults = ref([]);
    const defaultPoster = "http://127.0.0.1:8000/media/default_movies/default-movie.png";
    const sections = ref([
      { name: "popular", title: "인기영화", movies: [] },
      { name: "recent", title: "최신영화", movies: [] },
      { name: "upcoming", title: "개봉예정영화", movies: [] },
    ]);

    const currentIndex = ref({
      popular: 0,
      recent: 0,
      upcoming: 0,
    });

    const fetchMovies = async () => {
      const endpoints = {
        popular: "/popular.json",
        recent: "/recent.json",
        upcoming: "/upcoming.json",
      };

      for (const section of sections.value) {
        try {
          const response = await axios.get(endpoints[section.name]);
          section.movies = response.data.map((item) => ({
            movie_id: item.fields.movie_id,
            title: item.fields.title,
            poster_url: item.fields.poster_url,
          }));
        } catch (error) {
          console.error(`Error fetching ${section.name}:`, error);
        }
      }
    };

    const getChunks = (movies, size) => {
      const chunks = [];
      for (let i = 0; i < movies.length; i += size) {
        chunks.push(movies.slice(i, i + size));
      }
      return chunks;
    };

    const nextSlide = (sectionName) => {
      const totalSlides = Math.ceil(
        sections.value.find((s) => s.name === sectionName).movies.length / 5
      );
      if (currentIndex.value[sectionName] < totalSlides - 1) {
        currentIndex.value[sectionName]++;
      }
    };

    const prevSlide = (sectionName) => {
      if (currentIndex.value[sectionName] > 0) {
        currentIndex.value[sectionName]--;
      }
    };

    const getMoviesInOrder = (movies, count) => {
      return movies.slice(0, count);
    };

    const goToDetail = (movieId) => {
      router.push({ name: "MovieDetail", params: { id: movieId } });
    };

    const goToMore = (section) => {
      router.push({ name: "MovieMore", params: { section } });
    };

    const goToGenre = (genre) => {
      if (genre === "home") {
        router.push({ name: "MovieView" }).then(() => {
          window.location.reload();
        });
      } else {
        router.push({ name: "GenreMovie", params: { genre } });
      }
    };

    const getFullPosterUrl = (posterUrl) =>
      `https://image.tmdb.org/t/p/w500${posterUrl}`;

    const searchMovie = async () => {
      if (!searchQuery.value.trim()) {
        searchResults.value = [];
        errorMessage.value = "영화 제목을 입력해 주세요.";
        return;
      }

      try {
        const processedQuery = searchQuery.value.replace(/\s+/g, "");
        const response = await axios.get(
          "http://127.0.0.1:8000/api/v1/movies/search/",
          {
            params: { title: processedQuery },
          }
        );

        searchResults.value = response.data.map((movie) => ({
          id: movie.id,
          title: movie.title,
          poster_url: movie.poster_url,
          description: movie.description,
        }));
        errorMessage.value = "";
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error || "영화 검색에 실패했습니다.";
        searchResults.value = [];
      }
    };

    onMounted(fetchMovies);
    console.log('ssssssssssssssssss',searchResults)

    return {
      sections,
      searchQuery,
      errorMessage,
      currentIndex,
      getChunks,
      nextSlide,
      prevSlide,
      goToDetail,
      goToMore,
      goToGenre,
      getFullPosterUrl,
      getMoviesInOrder,
      searchMovie,
      defaultPoster,
      searchResults,
    };
  },
};
</script>


<style scoped>
.text-center {
  padding-top: 40px;
  color: #39ffe5;
  font-size: 2rem;
  font-weight: bold;
  animation: tracking-in-expand-fwd 0.8s cubic-bezier(0.215, 0.610, 0.355, 1.000) both; /* 애니메이션 추가 */
}
@keyframes tracking-in-expand-fwd {
  0% {
    letter-spacing: -0.5em;
    transform: translateZ(-700px);
    opacity: 0;
  }
  40% {
    opacity: 0.6;
  }
  100% {
    transform: translateZ(0);
    opacity: 1;
  }
}

.container {
  overflow: hidden; /* 넘치는 콘텐츠 숨김 */
  width: 100%; /* 컨테이너 너비를 화면에 맞춤 */
  padding: 0; /* 기본 패딩 제거 */
}

/* 장르 선택과 검색 컨테이너 */
.genre-search-container {
  display: flex;
  align-items: center;
  gap: 10px; /* 장르와 검색 사이 간격 */
  /* margin-bottom: 20px; */
}

.grid-container {
  display: flex; /* Flexbox로 가로 배치 */
  gap: 1rem; /* 카드 간의 간격 */
  width: calc(240px * 5 + 1rem * 4); /* 카드 5개 크기 + 간격 4개 */
  overflow: hidden; /* 넘치는 부분 숨김 */
  flex-wrap: wrap; /* 카드들을 여러 줄로 배치 */
}

.card {
  flex: 0 0 auto; /* 크기 고정 */
  width: 240px; /* 카드 너비 */
  height: 360px; /* 카드 높이 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s ease-in-out;
  background-color: transparent; /* 카드 배경을 투명하게 설정 */
}

.card img {
  width: 100%; /* 카드 크기에 맞춰 이미지 크기 */
  height: 100%; /* 고정된 높이 맞춤 */
  object-fit: cover; /* 이미지 비율 유지 */
} 

.card:hover {
  transform: scale(1.05); /* 호버 시 살짝 확대 */
}


.btn-more {
  display: inline-flex;
  align-items: center; /* 텍스트와 아이콘 정렬 */
  color: #d9d9d9; /* 평소 텍스트 색상 */
  font-size: 16px; /* 글자 크기 */
  font-weight: 500; /* 적당한 두께 */
  background: none; /* 배경 제거 */
  border: none; /* 버튼 테두리 제거 */
  cursor: pointer; /* 커서를 포인터로 변경 */
  padding: 5px 10px; /* 버튼 안쪽 여백 */
  text-decoration: none; /* 텍스트 장식 제거 */
  transition: color 0.3s ease-in-out;
}

.btn-more .arrow {
  margin-left: 5px; /* 텍스트와 화살표 간격 */
  font-size: 18px; /* 화살표 크기 */
  color: inherit; /* 부모의 텍스트 색상 상속 */
}

.carousel-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

.carousel-track-container {
  overflow: hidden;
  width: 100%;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease-in-out; /* 부드러운 이동 효과 */
  gap: 0; /* 각 슬라이드 사이의 간격 제거 */
}

.carousel-slide {
  display: flex;
  flex-shrink: 0; /* 크기 축소 방지 */
  width: 100%; /* 슬라이드 하나의 너비를 컨테이너의 100%로 설정 */
  justify-content: space-between; /* 내부 카드 간격 유지 */
}

.card {
  width: 240px;
  height: 360px;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  color: #39ffe5;
  border: none;
  font-weight: bold;
  cursor: pointer;
  padding: 10px 15px;
  z-index: 10;
}

.carousel-btn.prev {
  left: 0;
}

.carousel-btn.next {
  right: 0;
}

* {
	border: 0;
	box-sizing: border-box;
	margin: 0;
	padding: 0;
}
:root {
	font-size: calc(16px + (24 - 16)*(100vw - 320px)/(1920 - 320));
}
body, button, input {
	font: 1em Hind, sans-serif;
	line-height: 1.5em;
}
body, input {
	color: #171717;
}
body, .search-bar {
	display: flex;
}
body {
	background: #f1f1f1;
	height: 100vh;
}



.search-bar input {
  background: #fff;
  border-radius: 20px 0 0 20px;
  border: 1px solid #ccc;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
  padding: 0.75em;
  font-size: 14px;
  width: 100%;
}

.search-bar input:focus {
  outline: none;
  border-color: #3a3a3a;
}

.search-btn {
  background: #171717;
  border-radius: 0 20px 20px 0;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.search-btn:hover {
  background-color: #3a3a3a;
}

.search-btn:before,
.search-btn:after {
  content: "";
  display: block;
  position: absolute;
  opacity: 1; /* 항상 보이도록 설정 */
  transition: all 0.25s ease;
}

/* 버튼 손잡이 - 흰색 */
.search-btn:after {
  background: #fff; 
  border-radius: 0 0.25em 0.25em 0;
  top: 51%;
  left: 51%;
  width: 0.75em;
  height: 0.25em;
  transform: translate(0.2em, 0) rotate(45deg);
  transform-origin: 0 50%;
}

.search-btn:after {
  width: 8px;
  height: 2px;
  transform: rotate(45deg);
  top: 18px;
  left: 20px;
}

.search-btn span {
  display: none; /* 텍스트 숨김 */
}

/* 호버 시 효과 */
.search-bar input:focus + .search-btn:hover,
.search-bar input:valid + .search-btn:hover {
  background: #3a3a3a;
}

.search-bar input,
.search-btn, 
.search-btn:before, 
.search-btn:after {
	transition: all 0.25s ease-out;
}
.search-bar input,
.search-btn {
	width: 3em;
	height: 3em;
}
.search-bar input:invalid:not(:focus),
.search-btn {
	cursor: pointer;
}
.search-bar input:focus,
.search-bar input:valid  {
	width: 100%;
}
.search-bar input:focus,
.search-bar input:not(:focus) + .search-btn:focus {
	outline: transparent;
}
.search-bar {
	margin: auto;
	padding: 1.5em;
	justify-content: flex-end;
	/*  60em; */
  max-width: none;
  width: 60em;
  display: flex;
  align-items: center;
}
.search-bar input {
	background: transparent;
	border-radius: 1.5em;
	box-shadow: 0 0 0 0.4em #39ffe5 inset;
	padding: 0.75em;
	transform: translate(0.5em,0.5em) scale(0.5);
	transform-origin: 100% 0;
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
}
.search-bar input::-webkit-search-decoration {
	-webkit-appearance: none;
}
.search-bar input:focus,
.search-bar input:valid {
	background: #fff;
	border-radius: 0.375em 0 0 0.375em;
	box-shadow: 0 0 0 0.1em #d9d9d9 inset;
	transform: scale(1);
}
.search-btn {
	background: #39ffe5; /* 흰색 손잡이 */
	border-radius: 0 0.75em 0.75em 0 / 0 1.5em 1.5em 0;
	padding: 0.75em;
	position: relative;
	transform: translate(0.25em,0.25em) rotate(45deg) scale(0.25,0.125);
	transform-origin: 0 50%;
}
.search-btn:before, 
.search-btn:after {
	content: "";
	display: block;
	opacity: 0;
	position: absolute;
}
.search-btn:before {
	border-radius: 50%;
	box-shadow: 0 0 0 0.2em #f1f1f1 inset;
	top: 0.75em;
	left: 0.75em;
	width: 1.2em;
	height: 1.2em;
}
.search-btn:after {
	background: #f1f1f1;
	border-radius: 0 0.25em 0.25em 0;
	top: 51%;
	left: 51%;
	width: 0.75em;
	height: 0.25em;
	transform: translate(0.2em,0) rotate(45deg);
	transform-origin: 0 50%;
}
.search-btn span {
	display: inline-block;
	overflow: hidden;
	width: 1px;
	height: 1px;
}

/* Active state */
.search-bar input:focus + .search-btn,
.search-bar input:valid + .search-btn {
	background: #39ffe5af;
	border-radius: 0 0.375em 0.375em 0;
	transform: scale(1);
}
.search-bar input:focus + .search-btn:before, 
.search-bar input:focus + .search-btn:after,
.search-bar input:valid + .search-btn:before, 
.search-bar input:valid + .search-btn:after {
	opacity: 1;
}
.search-bar input:focus + .search-btn:hover,
.search-bar input:valid + .search-btn:hover,
.search-bar input:valid:not(:focus) + .search-btn:focus {
	background: #39ffe5d8;
}
.search-bar input:focus + .search-btn:active,
.search-bar input:valid + .search-btn:active {
	transform: translateY(1px);
}

@media screen and (prefers-color-scheme: dark) {
	body, input {
		color: #f1f1f1;
	}
	body {
		background: #171717;
	}
	.search-bar input {
		box-shadow: 0 0 0 0.4em #f1f1f1 inset;
	}
	.search-bar input:focus,
	.search-bar input:valid {
		background: #39ffe5;
		box-shadow: 0 0 0 0.1em #3d3d3d inset;
	}
	.search-btn {
		background: #f1f1f1;
	}
}

.sectionpadd {
  padding-bottom: 10px;
}
</style>
