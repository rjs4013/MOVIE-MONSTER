<template>
  <div class="main-page-container">
    <h1 class="maintext">MOVIE MONSTER</h1>
    <!-- 인기 영화 섹션 -->
    <div class="popular-movies-section">
      <h2>요즘 핫한 영화</h2>
      <p>요즘 가장 인기 있는 영화들을 모아봤어요!</p>
      <div class="carousel-wrapper">
        <button class="carousel-btn prev" @click="prevSlide('popular')">&lt;</button>
        <div class="carousel-track-container">
          <div
            class="carousel-track"
            :style="{ transform: `translateX(-${currentIndex['popular'] * 100}%)` }"
          >
            <div
              class="carousel-slide"
              v-for="(chunk, index) in getChunks(popularMovies, 5)"
              :key="index"
            >
              <div
                class="card"
                v-for="movie in chunk"
                :key="movie.movie_id"
                @click.stop="goToDetail(movie.movie_id)"
              >
                <img
                  :src="getFullPosterUrl(movie.poster_url)"
                  class="card-img-top"
                  :alt="movie.title"
                />
                <div>
                  <p class = "movietitle">{{ movie.title }}</p>
                  <span>⭐ {{ movie.rating || 'N/A' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <button class="carousel-btn next" @click="nextSlide('popular')">&gt;</button>
      </div>
    </div>
    <!-- Top Ranking Section -->
    <div class="top-ranking-section">
      <!-- 카드 섹션 -->
      <div class="ranking-card-container">
        <h2 class="modiTop3">TOP 3 MONSTERS</h2>
        <div
          v-for="(rank, index) in topThreeRankings"
          :key="rank.username"
          class="ranking-card"
        >
          <div class="card-inner" @click="navigateToProfile(rank.username)">
            <!-- 앞면 -->
            <div class="card-front">
              <h1>{{ index + 1 }}st</h1>
              <img :src="getRankImage(rank.rank_title)" alt="랭크 이미지" class="rank-image" />
              <div class="profile-header">
                <img :src="getProfileImage(rank.profile_picture)" alt="프로필 사진" class="profile-image" />
                <p class="username">{{ rank.username }}</p>
              </div>
            </div>
            <!-- 뒷면 -->
            <div class="card-back">
              <div class="back-stats">
                <div class="back-stat">
                  <p>포인트</p>
                  <div class="circle">{{ rank.points }}</div>
                </div>
                <div class="back-stat">
                  <p>좋아요</p>
                  <div class="circle">{{ rank.likes_count }}</div>
                </div>
                <div class="back-stat">
                  <p>게시글</p>
                  <div class="circle">{{ rank.articles_count }}</div>
                </div>
                <div class="back-stat">
                  <p>팔로워</p>
                  <div class="circle">{{ rank.followers_count }}</div>
                </div>
              </div>
              <!-- <div class="recommendation"> -->
                <!-- <span class="recommendation-label">추천작:</span> -->
                <!-- <span class="recommendation-title">{{ rank.recommended_movie.movie.title || "없음" }}</span> -->
              <!-- </div> -->
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Best Reviews Section -->
    <div class="best-reviews-container">
      <h2>Best Review</h2>
      <p>금주 가장 ❤를 많이 받은 게시물은 무엇일까요?</p>
      <div v-if="isLoading" class="loading-message">리뷰 데이터를 불러오는 중입니다...</div>
      <div v-else class="best-reviews">
        <div
          v-for="review in topReviews"
          :key="review.id"
          class="review-card"
          @click="navigateToDetail(review.id)"
        >
          <img :src="review.movie.poster_url" alt="포스터 이미지" class="poster" />
          <div class="review-details">
            <h3>{{ review.title }}</h3>
            <p>작성자: {{ review.user }}</p>
            <p>⭐  {{ review.rating }} / 10</p>
            <p>{{ review.content }}...</p>
            <p>❤  {{ review.like_count }}</p>
            <p>작성일: {{ formatDate(review.created_at) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Categories of Top Ranker -->
    <div class="top-ranker-categories-container" v-if="topRankerCategories">
      <h2 class="zizon">zl존 M✪N⭑스✧ㅌr  💥 <span class="firstuser">{{ topThreeRankings[0]?.username }}</span> 💥님의 컬렉션을 만나보세요!</h2>
      <div class="categories">
        <div
          v-for="category in topRankerCategories"
          :key="category.id"
          class="category-card"
          @click="navigateToCategoryDetail(category.id)"
        >
          <img
            :src="category.movies.length > 0 ? getFullPosterUrl(category.movies[0].poster_url) : 'http://127.0.0.1:8000/media/default_categories/default-category.png'"
            alt="컬렉션 포스터"
            class="category-poster"
          />
          <h3>{{ category.name }}</h3>
          <p>영화 개수: {{ category.movies.length }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

// Pinia 상태 관리
const store = useCounterStore();
const router = useRouter();

// Top 3 랭킹 데이터 가져오기
const topThreeRankings = computed(() => store.rankings.slice(0, 3));

// 프로필 사진 URL 반환 함수
const getProfileImage = (path) => {
  return `http://127.0.0.1:8000${path}`;
};

// 상태 관리
const topReviews = ref([]);
const isLoading = ref(true);
const topRankerCategories = ref(null);
const isLoadingCategories = ref(false);

const popularMovies = ref([]); // 인기 영화 데이터
const currentIndex = ref({ popular: 0 }); // 캐러셀 현재 인덱스

// 날짜 포맷 함수
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
};

// 랭크 이미지를 가져오는 함수
import bronzeRank from "@/assets/BronzeRank.png";
import silverRank from "@/assets/SilverRank.png";
import goldRank from "@/assets/GoldRank.png";
import platinumRank from "@/assets/PlatinumRank.png";
import diamondRank from "@/assets/DiamondRank.png";

// 영화 상세 페이지로 이동
const goToDetail = (movieId) => {
      router.push({ name: "MovieDetail", params: { id: movieId } });
    };

const getRankImage = (rankTitle) => {
  switch (rankTitle) {
    case "Bronze":
      return bronzeRank;
    case "Silver":
      return silverRank;
    case "Gold":
      return goldRank;
    case "Platinum":
      return platinumRank;
    case "Diamond":
      return diamondRank;
    default:
      return bronzeRank; // 기본값
  }
};

// 포스터 URL 생성 함수
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500";
  return `${baseUrl}${posterUrl}`;
};

// 프로필로 이동하는 함수
const navigateToProfile = (username) => {
  // 라우터를 사용하여 프로필 페이지로 이동
  window.location.href = `/profile/${username}`;
};

// API 호출: Top Reviews
const fetchTopReviews = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/api/v1/communities/top-reviews/"
    );
    topReviews.value = response.data;
  } catch (error) {
    console.error("Error fetching top reviews:", error);
  } finally {
    isLoading.value = false;
  }
};

// 인기 영화 가져오기
const fetchPopularMovies = async () => {
  try {
    const response = await axios.get("/popular.json");
    popularMovies.value = response.data.map((item) => ({
      movie_id: item.fields.movie_id,
      title: item.fields.title,
      poster_url: item.fields.poster_url,
      rating: item.fields.vote_avg || "N/A", // 평점 추가 (없으면 N/A)
    }));
    console.log('ww',popularMovies.value)
  } catch (error) {
    console.error("Error fetching popular movies:", error);
  }
};

// 슬라이드 이동
const nextSlide = (section) => {
  const totalSlides = Math.ceil(popularMovies.value.length / 5);
  if (currentIndex.value[section] < totalSlides - 1) {
    currentIndex.value[section]++;
  }
};

const prevSlide = (section) => {
  if (currentIndex.value[section] > 0) {
    currentIndex.value[section]--;
  }
};

// 데이터를 5개씩 나누기
const getChunks = (movies, size) => {
  const chunks = [];
  for (let i = 0; i < movies.length; i += size) {
    chunks.push(movies.slice(i, i + size));
  }
  return chunks;
};

// API 호출: Top Ranker Categories
const fetchTopRankerCategories = async () => {
  if (!topThreeRankings.value[0]?.username) return;

  isLoadingCategories.value = true;
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/accounts/profile/${topThreeRankings.value[0].username}/categories/`,
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );
    topRankerCategories.value = response.data; // 성공적으로 데이터를 받음
  } catch (error) {
    console.error("Failed to fetch categories:", error);
  } finally {
    isLoadingCategories.value = false;
  }
};

// 상세 페이지로 이동
const navigateToDetail = (id) => {
  router.push({ name: "DetailView", params: { id } });
};

const navigateToCategoryDetail = (categoryId) => {
  window.location.href = `/categories/${categoryId}`;
};

// 데이터 로드
onMounted(async () => {
  if (!store.rankings.length) {
    await store.fetchRankings();
  }
  await fetchTopReviews();
  await fetchTopRankerCategories();
  await fetchPopularMovies(); // 인기 영화 데이터 가져오기
});

console.log('ppss', topThreeRankings)
</script>


<style scoped>
/* 메인 페이지 컨테이너 스타일 */
.main-page-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 50px;
}

.maintext {
  text-align: center;
  font-size: 4rem; /* 글자 크기 */
  font-weight: bold; /* 굵기 */
  background: linear-gradient(135deg, #e02ff0, #39ffe5); /* 그래디언트 색상 */
  -webkit-background-clip: text; /* 그래디언트가 글자 내부에만 표시되게 함 */
  -webkit-text-fill-color: transparent; /* 텍스트 색상을 투명으로 */
  text-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* 입체감을 위한 그림자 */
  transform: perspective(500px) rotateX(10deg); /* 휘어진 효과 */
  letter-spacing: 3px; /* 글자 간격 */
  margin-bottom: 20px; /* 아래쪽 여백 */
}

/* 인기 영화 섹션 */
.popular-movies-section {
  margin-bottom: 50px;
  padding-bottom: 30px;
  border-bottom: 2px solid transparent; /* 기본 투명 */
  border-image: linear-gradient(135deg, #e02ff0, #39ffe5); /* 그래디언트 색상 */
  border-image-slice: 1; /* 전체 영역 적용 */
}

.popular-movies-section h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.popular-movies-section p {
  font-size: 14px;
  color: #f9f9f9;
  margin-bottom: 20px;
}

.movietitle {
  color: #f9f9f9
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
  transition: transform 0.5s ease-in-out;
}

.carousel-slide {
  display: flex;
  flex-shrink: 0; /* 크기 축소 방지 */
  justify-content: space-between;
  width: 100%;
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
  padding: 5px;
}

.card img {
  width: 100%;
  height: 300px; /* 고정된 크기 */
  object-fit: cover; /* 이미지 비율 유지 */
  border-radius: 10px;
}

.card p {
  margin: 10px 0 0;
  font-size: 14px;
  font-weight: bold;
}

.card span {
  font-size: 14px;
  color: #666;
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

/* Top 랭킹 섹션 스타일 */
.top-ranking {
  position: relative;
  width: 400px;
  height: 300px;
}

.first {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.second {
  position: absolute;
  top: 120px;
  left: 20%;
  transform: translateX(-50%);
  text-align: center;
}

.third {
  position: absolute;
  top: 120px;
  right: 20%;
  transform: translateX(50%);
  text-align: center;
}

.position-icon {
  width: 50px;
  height: 50px;
  cursor: pointer;
  transition: transform 0.2s;
}

.position-icon:hover {
  transform: scale(1.1);
}

.user-info {
  margin-top: 10px;
}

.rank-icon {
  width: 30px;
  height: 30px;
}

.username {
  font-size: 16px;
  font-weight: bold;
  margin-top: 5px;
  display: block;
}

/* 베스트 리뷰 섹션 */
.best-reviews-container {
  width: 100%;
  padding: 20px;
  border-top: 2px solid transparent; /* 기본 투명 */
  border-image: linear-gradient(135deg, #e02ff0, #39ffe5); /* 그래디언트 색상 */
  border-image-slice: 1; /* 전체 영역 적용 */
}

.loading-message {
  text-align: center;
  font-size: 16px;
  color: #888;
}

.best-reviews {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.review-card {
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: #f9f9f9; /* 조금 더 밝은 배경색 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.review-card:hover {
  transform: scale(1.03); /* 살짝 확대 효과 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 호버 시 강조된 그림자 */
}

.poster {
  width: 100px;
  height: 150px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 포스터 그림자 */
}

.review-details {
  display: flex;
  flex-direction: column;
  justify-content: center; /* 텍스트가 수직 중앙 정렬 */
  flex-grow: 1; /* 텍스트가 충분히 공간을 차지하도록 설정 */
}

.review-details h3 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
  color: #333; /* 다소 어두운 글씨 */
}

.review-details p {
  margin: 5px 0;
  font-size: 14px;
  color: #555; /* 중간 밝기의 글씨 */
}

.review-details p:first-of-type {
  font-weight: bold; /* 작성자 이름 강조 */
}

.review-details p:last-of-type {
  color: #777; /* 작성일자 다소 흐릿하게 표시 */
  font-size: 12px;
}


/* Top Ranker Categories Section */
.top-ranker-categories-container {
  border-top: 2px solid transparent; /* 기본 투명 */
  border-image: linear-gradient(135deg, #e02ff0, #39ffe5); /* 그래디언트 색상 */
  border-image-slice: 1; /* 전체 영역 적용 */
  padding-top: 20px;
  padding-left: 20px
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.category-card {
  width: calc(25% - 20px);
  border: 1px solid transparent; /* 기본 테두리 투명 */
  border-radius: 8px; /* 테두리에 둥근 효과 */
  background: linear-gradient(135deg, #e02ff0, #39ffe5) border-box; /* 그래디언트 테두리 */
  overflow: hidden; /* 내부 요소가 영역을 넘지 않도록 */
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.category-card:hover {
  transform: scale(1.02);
}

.category-poster {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.category-card h3 {
  font-size: 18px;
  margin: 10px;
  color: black;
  font-weight: bold;
}

.category-card p {
  font-size: 14px;
  margin: 0 10px 10px;
  color: black;

}

.zizon {
  margin-bottom: 30px;
}

/* 카드 컨테이너 */
.ranking-card-container {
  display: flex;
  justify-content: center;
  gap: 0px;
  margin-top: 0px;
  margin-bottom: 50px;
}

/* 카드 */
.ranking-card {
  width: 500px;
  height: 390px;
  perspective: 1000px;
  margin-inline: 50px;
  margin-bottom: -40px;
  margin-top: -5px;
}

/* 카드 내부 */
.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.8s;
  cursor: pointer;
}

/* 카드 회전 */
.card-inner:hover {
  transform: rotateY(180deg);
}

/* 카드 앞면 */
.card-front,
.card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 카드 앞면 스타일 */
.card-front {
  background: linear-gradient(135deg, #e02ff0, #39ffe5);
  color: white;
}

.card-front h1 {
  font-size: 4rem;
  margin: 0;
}

.card-front .rank-image {
  width: 80px;
  height: 80px;
  margin: 10px 0;
}

.card-front .username {
  font-size: 2.5rem;
  font-weight: bold;
}

/* 카드 뒷면 스타일 */
.card-back {
  background: linear-gradient(135deg, #e02ff0, #39ffe5);
  transform: rotateY(180deg);
  color: #333;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.back-stats {
  display: grid; /* 그리드 레이아웃 사용 */
  grid-template-columns: repeat(2, 1fr); /* 2열로 설정 */
  gap: 20px; /* 항목 간의 간격 */
  justify-content: center;
  align-items: center;
}

.back-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.back-stat p {
  font-size: 1rem;
  margin: 0;
  color: #555;
}

.circle {
  width: 60px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  background-color: #f0f0f0;
  color: #333;
  font-size: 1.2rem;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 5px;
}

.top-ranking-section {
  margin-top: -50px;
}

.back-recommend {
  margin-top: 20px;
  text-align: center;
}

.back-recommend p {
  font-size: 1rem;
  margin: 0;
  color: #555;
}

.recommendation {
  display: flex;
  align-items: center; /* 세로로 중앙 정렬 */
  justify-content: center; /* 가로로 중앙 정렬 */
  margin-top: 20px;
  font-size: 1rem;
  color: #333;
}

.recommendation-label {
  font-weight: bold;
  margin-right: 10px;
}

.recommendation-title {
  display: inline-block;
  padding: 5px 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  color: #555;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


.card-back h3 {
  margin: 10px 0;
  font-size: 1.2rem;
}

.back-section {
  margin-bottom: 10px;
  padding: 5px;
}

.back-section p {
  font-size: 1.1rem;
  margin: 5px 0;
}

.back-section strong {
  color: #555;
}

.profile-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-right: 0px;
  border: 2px solid white;
  object-fit: cover;
}

.username {
  font-size: 10rem;
  font-weight: bold;
}

/* 프로필 헤더 */
.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px; /* 중앙 정렬을 위한 여백 추가 */
}

.firstuser {
  font-weight: bold;
  background: linear-gradient(135deg, #e02ff0, #39ffe5);
  -webkit-background-clip: text;  /* 웹킷 기반 브라우저에서 배경을 텍스트에 맞게 자르기 */
  background-clip: text;         /* 비-웹킷 브라우저에서 배경을 텍스트에 맞게 자르기 */
  color: transparent;            /* 텍스트 색상은 투명하게 처리 */
}
</style>
