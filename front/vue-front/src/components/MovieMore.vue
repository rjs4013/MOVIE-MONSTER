<template>
  <div class="container">
    <!-- 섹션 제목과 뒤로가기 버튼 -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-center">{{ sectionTitle }} 영화</h2>
      <button class="btn-back" @click="goBack">
        <span class="arrow">&lt;</span> 뒤로가기
      </button>
      <!-- <button class="btn btn-secondary" @click="goBack">뒤로가기</button> -->
    </div>

    <!-- 영화 리스트 -->
    <div class="grid-container">
      <div
        class="card"
        v-for="movie in movies"
        :key="movie.movie_id"
        @click="goToDetail(movie.movie_id)"
      >
        <img
          :src="getFullPosterUrl(movie.poster_url)"
          class="card-img-top"
          :alt="movie.title"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const section = ref(route.params.section);
    const movies = ref([]);

    // 영화 데이터 가져오기
    const fetchMovies = async () => {
      try {
        const apiEndpoint =
          section.value === "popular"
            ? "/popular.json"
            : section.value === "recent"
            ? "/recent.json"
            : "/upcoming.json";

        const response = await axios.get(apiEndpoint);
        movies.value = response.data.map((item) => ({
          movie_id: item.fields.movie_id,
          title: item.fields.title,
          poster_url: item.fields.poster_url,
        }));
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    };

    // 섹션 제목 계산
    const sectionTitle = computed(() => {
      return section.value === "popular"
        ? "인기"
        : section.value === "recent"
        ? "최신"
        : "개봉예정";
    });

    // 영화 디테일 페이지 이동
    const goToDetail = (movieId) => {
      router.push({ name: "MovieDetail", params: { id: movieId } });
    };

    // 영화 포스터 URL 생성
    const getFullPosterUrl = (posterUrl) =>
      `https://image.tmdb.org/t/p/w500${posterUrl}`;

    // 뒤로가기 기능
    const goBack = () => {
      router.go(-1); // 이전 페이지로 이동
    };

    onMounted(fetchMovies);

    return {
      sectionTitle,
      movies,
      goToDetail,
      getFullPosterUrl,
      goBack, // 뒤로가기 메서드 반환
    };
  },
};
</script>

<style scoped>
.container {
  width: 100%; /* 전체 화면 너비 */
  padding: 0; /* 기본 패딩 제거 */
  margin-top: 20px;
}

.grid-container {
  display: flex;
  flex-wrap: wrap;
  row-gap: 2rem; /* 위아래 간격 */
  column-gap: 1.5rem; /* 좌우 간격 */
  justify-content: start;
}

.card {
  width: 240px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  text-align: center;
  transition: transform 0.2s ease-in-out;
  background-color: transparent; /* 카드 배경을 투명하게 설정 */
}

.card:hover {
  transform: scale(1.05);
}

.card-img-top {
  width: 100%;
  height: 360px;
  object-fit: cover;
}

.btn-back {
  display: inline-flex;
  align-items: center; /* 텍스트와 아이콘 정렬 */
  color: #e5e5e5; /* 기본 텍스트 색상 */
  font-size: 16px; /* 글자 크기 */
  font-weight: 500; /* 텍스트 두께 */
  background: none; /* 배경 제거 */
  border: none; /* 테두리 제거 */
  cursor: pointer; /* 포인터 커서 */
  padding: 5px 10px; /* 여백 */
  text-decoration: none; /* 밑줄 제거 */
  transition: color 0.3s ease-in-out; /* 호버 효과 */
}

.btn-back .arrow {
  margin-right: 5px; /* 아이콘과 텍스트 간격 */
  font-size: 18px; /* 화살표 크기 */
  color: inherit; /* 부모 색상 상속 */
}

.btn-back:hover {
  color: #ffffff; /* 호버 시 색상 변경 */
}
</style>
