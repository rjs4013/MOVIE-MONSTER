<template>
  <div class="container">
    <h1 class="text-center tracking-in-expand-fwd my-4">PROFILE</h1>
    <div class="profile-page">
      <!-- 좌측: 프로필 정보 -->
      <div class="profile-info">
        <div class="follow-button-wrapper">
        <div class="profile-header">
          
          <img :src="`http://127.0.0.1:8000${user.profile_picture}`" class="profile-img" alt="프로필 사진">
          <div class="profile-basic">
            <h1 class="profile-title">{{ user.username }}</h1>
            <div class="profile-follow-stats">
              <p>팔로잉 {{ user.followingsCount }}</p><hr/><hr/>
              <p>팔로워 {{ user.followersCount }}</p>
            </div>
            
          </div>
          </div>
          <button v-if="!isOwnProfile" class="follow-button" @click="toggleFollow">
              {{ isFollowed ? '언팔로우' : '팔로우' }}
            </button>
        </div>
        <div class="profile-details">
          <div class="stats-row">
            <div class="stat-box">
              <img :src="getRankImage(user.rank_title)" alt="랭크 이미지" class="rank-icon-small" />
              <p class="stat-num">{{ user.points }}</p>
            </div>
            <div class="stat-box">
              <h1>📝</h1>
              <p class="stat-num-count">{{ user.articlesCount }}</p>
            </div>
            <div class="stat-box">
              <h1>❤️</h1>
              <p class="stat-num">{{ user.likesCount }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 우측: 추천 영화 -->
      <div class="recommended-movie-section">
        <h2>이거 안보면 진짜 후회해요!</h2>
        <div v-if="!recommendedMovie" class="not_yet_recommend">
          <p>아직 추천하는 영화가 없어요.</p>
          <a v-if="isOwnProfile" class="add-movie" @click="openRecommendationModal">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            영화 추천하기
          </a>
        </div>
        <div v-else class="yes_recommend">
          <div class="yes-yes-recommend">
            <img :src="recommendedMovie.posterUrl"  alt="추천 영화 포스터" />
            <a v-if="isOwnProfile" class="add-movie-after" @click="editRecommendation" >
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              영화 수정
            </a>
          </div>
          
          <div class="recommend-detail">
          <h3>{{ recommendedMovie.title }}</h3>
          <p class="recommendation-reason">추천 이유: {{ recommendedMovie.reason }}</p>
        </div>
          
        </div>
      </div>
    </div>

    <!-- 유저의 컬렉션 섹션 -->
    <div class="category-section">
      <div class="category-header">
        <h2>{{ user.username }}의 컬렉션</h2>
        <a v-if="isOwnProfile" class="add-category" @click.prevent="showCreateCategoryModal = true">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            새 컬렉션
        </a>
      </div>
      <div v-if="categories.length === 0" class="empty-message">
        <p>아직 컬렉션이 없습니다.</p>
      </div>

      <div v-else class="categories">
      <div
        v-for="category in categories"
        :key="category.id"
        class="category-card"
        @click="goToCategoryDetail(category.id)"
      >
        <!-- 영화 포스터 또는 디폴트 이미지 -->
        <img :src="category.movies.length > 0 ? getFullPosterUrl(category.movies[0].poster_url) : 'http://127.0.0.1:8000/media/default_categories/default-category.png'" 
        alt="컬렉션 이미지" 
        class="category-poster">
      <h3>{{ category.name }}</h3>
      <p>영화 개수: {{ category.movies.length }}</p>
    </div>
  </div>
      
  <!-- 새 컬렉션 추가 모달 -->
  <CreateCategoryModal
    v-if="showCreateCategoryModal"
    @close="closeCreateCategoryModal"
    @categoryCreated="addCategory"
  />
    </div>

    

    <!-- 추천 영화 모달 -->
    <div v-show="showRecommendationModal" class="modal">
      <div class="modal-content">
        <h2>추천 영화 선택</h2>
          <input v-model="searchQuery" @input="searchMovies" placeholder="영화 제목 입력" />
          <!-- 영화 검색 결과 -->
          <ul>
            <li v-for="movie in searchResults" :key="movie.id">
              {{ movie.title }}
              <button @click="selectRecommendedMovie(movie)">선택</button>
            </li>
          </ul>

          <!-- 선택된 영화 포스터 및 정보 -->
          <div v-if="selectedMovie" class="selected-movie-preview">
            <h3>선택된 영화:</h3>
            <img :src="selectedMovie.posterUrl" alt="선택된 영화 포스터" class="movie-poster-preview" />
            <p>{{ selectedMovie.title }}</p>
          </div>

          <!-- 추천 이유 작성 -->
          <textarea
            v-model="recommendationReason"
            placeholder="추천 이유를 작성해주세요"
            class="recommendation-reason"
          ></textarea>
          <div class="modal-actions">
            <button class="save-btn" @click="saveRecommendation">완료</button>
            <button class="close-modal-btn" @click="closeRecommendationModal">닫기</button>
          </div>
      </div>
      <!-- 컬렉션 추가 모달 -->
    <AddToCategoryModal
      v-if="showCategoryModal"
      :movie-id="movie.id"
      @close="showCategoryModal = false"
    />
  </div>
</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import CreateCategoryModal from "@/components/CreateCategoryModal.vue";

// Vue Router와 Pinia 스토어 사용
const route = useRoute();
const router = useRouter();
const store = useCounterStore();

const toggleFollow = async () => {
  console.log("Toggle Follow clicked"); // 디버깅용
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/accounts/${user.value.id}/follow/`,
      null,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    // 응답 데이터를 사용하여 상태 업데이트
    isFollowed.value = response.data.is_followed;
    user.value.followersCount = response.data.followers_count;
    user.value.followingsCount = response.data.followings_count;

    console.log("Follow toggle success:", response.data); // 디버깅용
  } catch (error) {
    console.error("Error toggling follow:", error);
  }
};

const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500"; // TMDB 이미지 베이스 URL
  return `${baseUrl}${posterUrl}`;
};

// 랭크 이미지를 가져오는 함수
import bronzeRank from '@/assets/BronzeRank.png';
import silverRank from '@/assets/SilverRank.png';
import goldRank from '@/assets/GoldRank.png';
import platinumRank from '@/assets/PlatinumRank.png';
import diamondRank from '@/assets/DiamondRank.png';

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

// 유저 데이터 상태 관리
const user = ref({
  username: '',
  rank_title: '',
  followingsCount: 0,
  followersCount: 0,
  articlesCount: 0, // 작성한 게시글 수
  likesCount: 0, // 받은 좋아요 수
});
const isFollowed = ref(false);
const categories = ref([]);
const showCreateCategoryModal = ref(false); // 모달 표시 여부
const showRecommendationModal = ref(false);
const recommendedMovie = ref(null); // 추천 영화 상태
const recommendationReason = ref('');
const searchQuery = ref('');
const searchResults = ref([]);
const selectedMovie = ref(null); // 선택된 영화 상태 추가

// 현재 프로필이 로그인된 사용자의 것인지 확인
const isOwnProfile = computed(() => store.user.username === route.params.username);

// API를 통해 프로필 데이터 가져오기
const fetchProfile = async () => {
  try {
    const { data } = await axios.get(
      `http://127.0.0.1:8000/accounts/profile/${route.params.username}/`, 
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );

    // Use store.getRankTitle to calculate the rank_title if not provided
    const rankTitle = data.rank_title || store.getRankTitle(data.points);

    user.value = {
      id: data.id,
      username: data.username,
      points: data.points,
      rank_title: rankTitle, // Use calculated rank_title
      followingsCount: data.followings_count,
      followersCount: data.followers_count,
      articlesCount: data.articles_count,
      likesCount: data.likes_count,
      profile_picture: data.profile_image,
      // reason: data.recommended_movie.reason, // 추천 이유
    };

    // 추천 영화 데이터 처리
    if (data.recommended_movie) {
      recommendedMovie.value = {
        id: data.recommended_movie.movie.id,
        title: data.recommended_movie.movie.title,
        posterUrl: getFullPosterUrl(data.recommended_movie.movie.poster_url),
        reason: data.recommended_movie.reason,
      };
      console.log("추천 영화 로드 성공:", recommendedMovie.value);
    } else {
      recommendedMovie.value = null;
      console.log("추천 영화 데이터 없음");
    }
    console.log("프로필 데이터 로드 성공:", user.value);
    console.log("추천 영화 데이터:", recommendedMovie.value);

    console.log(user.value);
    isFollowed.value = data.is_followed;
    categories.value = data.categories;
    // recommendedMovie.value = data.recommended_movie || null; // 추천 영화 데이터
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
};

// 컬렉션 상세 페이지로 이동
const goToCategoryDetail = (categoryId) => {
  router.push(`/categories/${categoryId}`);
};

// 새 컬렉션 모달 열기/닫기
const openCreateCategoryModal = () => {
  showCreateCategoryModal.value = true;
};
const closeCreateCategoryModal = () => {
  showCreateCategoryModal.value = false;
};

// 새 컬렉션 목록에 추가
const addCategory = (category) => {
  categories.value.push(category);
};

// 추천 영화 모달 열기/닫기
// const openRecommendationModal = () => (showRecommendationModal.value = true);
const openRecommendationModal = () => {
  console.log("추천 수정 클릭됨");
  console.log("모달 상태 이전:", showRecommendationModal.value);
  showRecommendationModal.value = true; // 모달을 열기 위해 값 변경
  console.log("모달 상태 이후:", showRecommendationModal.value);
};
const closeRecommendationModal = () => {
  showRecommendationModal.value = false;
  searchQuery.value = '';
  searchResults.value = [];
  recommendationReason.value = '';
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
      headers: { Authorization: `Token ${store.token}` },
    });
    searchResults.value = response.data;
  } catch (error) {
    console.error('Error searching movies:', error);
  }
};

const selectRecommendedMovie = (movie) => {
  // 선택된 영화 데이터를 업데이트
  selectedMovie.value = {
    id: movie.id,
    title: movie.title,
    posterUrl: getFullPosterUrl(movie.poster_url), // 포스터 URL 생성
  };

  // 추천 영화 데이터에도 반영 (저장을 위해 필요)
  recommendedMovie.value = {
    id: movie.id,
    title: movie.title,
    posterUrl: getFullPosterUrl(movie.poster_url),
  };

  console.log("선택된 영화 데이터:", selectedMovie.value); // 디버깅용
};

// 추천 영화 저장
const saveRecommendation = async () => {
  if (!recommendedMovie.value || !recommendedMovie.value.id || !recommendationReason.value.trim()) {
    alert("영화와 추천 이유를 모두 입력해주세요.");
    console.error("추천 영화 저장 실패 - 데이터 확인:", {
      movie: recommendedMovie.value,
      reason: recommendationReason.value,
    });
    return;
  }
  try {
    const response = await axios.post(
      `${store.API_URL}/accounts/recommend-movie/`,
      {
        movie_id: recommendedMovie.value.id,
        reason: recommendationReason.value.trim(),
      },
      { headers: { Authorization: `Token ${store.token}` } }
    );

    // 서버 응답을 추천 영화 데이터로 반영
    recommendedMovie.value = {
      id: response.data.movie.id,
      title: response.data.movie.title,
      posterUrl: getFullPosterUrl(response.data.movie.poster_url),
      reason: response.data.reason,
    };

    console.log("추천 영화 저장 성공:", response.data);

    closeRecommendationModal();
    alert("추천 영화가 저장되었습니다!");
  } catch (error) {
    console.error("추천 영화 저장 중 오류 발생:", error.response?.data || error);
  }
};

// 추천 영화 수정
const editRecommendation = () => {
  console.log("추천 수정 버튼 클릭됨"); // 디버깅용 로그
  openRecommendationModal();
  recommendationReason.value = recommendedMovie.value.reason || '';
};

onMounted(() => {
  fetchProfile();
});

// 라우트 변경을 감지하고 새 데이터를 로드
watch(() => route.params.username, (newUsername, oldUsername) => {
  console.log(`Route username changed: ${oldUsername} -> ${newUsername}`);
  fetchProfile();
});
</script>




<style scoped>



.container {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.text-center {
  color: #e02ff0;
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


/* 전체 페이지 스타일 */
.profile-page {
  width: 80%; /* 전체 컨테이너 너비를 80%로 설정 */
  max-width: 1200px; /* 최대 고정 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 */
  display: grid;
  grid-template-columns: 1fr 1fr; /* 좌측 1, 우측 2 비율 */
  gap: 20px;
  padding: 20px;
  /* background-color: #e02ff017; */
  color: #f5f5f5;
  border-radius: 10px;
}


/* 프로필 정보 (좌측 섹션) */
.profile-info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 425px;
  padding: 30px;
  background-color: #e02ff01c;
  border-radius: 10px;
  margin: 20px;
  position: relative; /* 하단 고정을 위해 부모 요소 위치 기준 설정 */
  gap: 20px;
  
}

.profile-details {
  position: absolute; /* 부모 요소의 하단에 고정 */
  bottom: 0; /* 아래쪽 여백 제거 */
  left: 0;
  right: 0; /* 좌우로 꽉 차게 */
  padding: 0px 20px; /* 내부 여백 */
  margin-top: auto; /* 프로필 헤더와 버튼 사이 고정된 거리 확보 */
  border-top: 1px solid #e02ff06b; /* 상단에 경계선 추가 */
  /* padding-top: 15px; */
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 30px;
  justify-content: center; /* 중앙 정렬 */
  margin-bottom: 20px;
}

.profile-header img {
  display: flex;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 1.2px solid #e02ff0;
}


.profile-basic {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}

.profile-title {
  /* align-items: center; */
  font-size: 2.5rem;
  color: white;
  margin-bottom: 5px;
  /* font-weight: bold; */
}

.profile-follow-stats {
  display: flex;
  gap: 20px;
  font-size: 1rem;
  color: #f5f5f5;
  justify-content: space-between; /* 왼쪽 정렬 */
}

.follow-button-wrapper {
  margin-top: 20px; /* 팔로잉/팔로워와 버튼 간격 */
  text-align: right; /* 버튼을 중앙 정렬 */
}


.follow-button {
  margin-top: -10px;
  margin-bottom: 20px;
  padding: 8px;
  width: 50%; /* 버튼 길이를 프로필 스탯에 맞춤 */
  background-color: #3897f0;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
}

.follow-button:hover {
  background-color: #217ac0;
}


/* 랭크 이미지 */
.rank-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 랭크 이미지 및 유저 이름 */
.username-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rank-icon-small {
  width: 58px;
  height: 58px;
}

.rank-stats {
  font-size: 0.9rem;
}


/* 포인트, 게시글, 좋아요 수 */
.stats-row {
  display: flex;
  justify-content: space-around;
  /* margin-top: 20px; */
  /* background-color: #e02ff02c; */
  padding: 10px 0;
  text-align: center;
  /* border: 1px solid #e02ff06b; */
  /* border-top: 1px solid #e02ff06b; */
  color: white;
  font-size: 2rem;
}

.stat-box {
  /* background-color: #282b3b; */
  padding: 10px 20px;
  margin-top: 0px;
  /* border-radius: 10px; */
  text-align: center;
  color: white;
  font-size: 1rem;
}
.stat-num {
  padding-top: 20px;
}
.stat-num-count {
  padding-top: 20px;
  padding-right: 5px;
}
/* 추천 영화 섹션 */
.not_yet_recommend {
  text-align: center;
  padding-top: 15%;
  flex-direction: column;
  display: flex;
}

.yes_recommend {
  display: flex;
  flex-direction: row; /* 가로 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  justify-content: space-between; /* 양 끝 정렬 */
  gap: 20px; /* 간격 추가 */
  width: 100%; /* 부모 요소 너비 */
}


.yes_recommend img {
  width: 150px; /* 이미지 크기 고정 */
  height: auto;
  object-fit: cover; /* 이미지 비율 유지 */
  border-radius: 10px;
  border: 2px solid #e02ff0; /* 테두리 */
}

.recommend-detail {
  display: flex;
  flex-direction: column; /* 세로 정렬 */
  justify-content: center;
  text-align: left;
}

.recommend-detail h3 {
  font-size: 1.5rem;
  color: #fff;
  margin-bottom: 10px;
}

.recommend-detail p {
  display: block; /* 블록 레벨 요소 */
  font-size: 1rem; /* 글씨 크기 */
  color: #ffffff; /* 하얀색 텍스트 */
  margin-top: 5px; /* 제목과의 간격 */
  text-align: left; /* 왼쪽 정렬 */
  background: none; /* 박스 배경 제거 */
  border: none; /* 경계선 제거 */
  padding: 0; /* 내부 여백 제거 */
}

.yes_yes_recommend {
  flex-direction: column;
}

.add-movie {
  
  bottom: 20px; /* 하단 여백 */
  left: 20px; /* 좌측 여백 */
}
.recommended-movie-section {
  position: relative;
  display: flex;
  text-align: center;
  flex-direction: column;
  align-items: center;
  padding: 30px;
  background-color: #e02ff01c;
  border-radius: 10px;
  height: 425px;
  margin: 20px;
  
  gap: 20px;
}

.recommended-movie-section > div {
  display: flex;
  align-items: flex-start;
  gap: 20px; /* 포스터와 텍스트 간 간격 */
}

.recommended-movie-section img {
  width: 150px;
  height: 225px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 10px;
  border: 1px solid #e02ff0;
}

.recommended-movie-section h3 {
  font-size: 1rem;
  margin: 0 0 10px 0;
}


.recommendation-reason {
  display: -webkit-box;
  -webkit-line-clamp: 7; /* 최대 3줄까지만 보이게 설정 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-align: left; /* 추천 이유 왼쪽 정렬 */
  /* text-overflow: ellipsis; */
  /* white-space: normal; */
  font-size: 0.9rem; /* 글자 크기 조정 */
  line-height: 1.4; /* 줄 간격 조정 */
  color: #aaa; /* 텍스트 색상 */
  margin: 5px 0;

  width: 100%; /* 텍스트박스 전체 너비 */
  height: 150px; /* 높이 지정 */
  /* margin-top: 10px; */
  padding: 10px;
  /* font-size: 1rem; */
  /* border: 1px solid #ddd; */
  border-radius: 5px;
  resize: none;
}

.recommended-movie-section h2 {
  font-size: 1.2rem;
  margin-bottom: 15px;
  color: #f5f5f5;
}

.recommended-movie-section p {
  font-size: 0.9rem;
  color: #aaa;
  margin: 5px 0;
}




/* 컬렉션 섹션 */
.category-section {
  width: 950px;
  text-align: left; /* 전체 섹션 텍스트 왼쪽 정렬 */
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  
}
.category-header h2 {
  font-size: 2.2rem;
  /* font-weight: bold; */
  /* color: #333; */
}

.empty-message {
  text-align: left;
  font-size: 1rem;
  color: #999;
  padding: 0 0 20px 0;
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  
}

.category-card {
  width: calc(25% - 20px);
  border: 1px solid #e02ff0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
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
}

.category-card p {
  font-size: 14px;
  margin: 0 10px 10px;
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #2b2b2b; /* 어두운 배경 */
  z-index: 9999;
  width: 80%;
  max-width: 500px; /* 모달 최대 너비 */
  max-height: 80%;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4), 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 20px;
  color: #fff; /* 흰색 텍스트 */
  
}

.modal-content {
  background-color: #1e1e1e; /* 어두운 배경 */
  color: #ffffff; /* 흰색 텍스트 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal-content h2 {
  text-align: center;
  font-size: 1.5rem;
  color: #ffffff;
  margin-bottom: 15px;
}

.modal-content input {
  background-color: #333333; /* 입력 필드 배경 */
  color: #ffffff; /* 흰색 텍스트 */
  border: 1px solid #555555; /* 필드 경계선 */
  padding: 10px;
  border-radius: 5px;
}
.modal-content input::placeholder {
  color: #bbbbbb; /* 플레이스홀더 색상 */
}

.modal-content ul {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 200px; /* 리스트의 최대 높이를 제한 */
  overflow-y: auto; /* 스크롤이 필요한 경우 표시 */
}

.modal-content ul li {
  background-color: #2a2a2a; /* 리스트 아이템 배경 */
  color: #ffffff; /* 텍스트를 흰색으로 변경 */
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-content ul li:last-child {
  border-bottom: none; /* 마지막 아이템의 테두리 제거 */
}

.modal-content ul li button {
  background-color: #e02ff0; /* 버튼 배경색 */
  color: #ffffff; /* 버튼 텍스트 색상 */
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.modal-content ul li button:hover {
  background-color: #ff3ff3; /* 호버 시 더 밝은 색상 */
}

textarea.recommendation-reason {
  background-color: #333333; /* 텍스트박스 배경 */
  color: #ffffff; /* 흰색 텍스트 */
  border: 1px solid #555555; /* 경계선 */
  padding: 10px;
  border-radius: 5px;
}

.selected-movie-preview {
  display: flex;
  flex-direction: column; /* 수직 정렬 */
  align-items: center; /* 중앙 정렬 */
  gap: 10px; /* 간격 추가 */
  margin-top: 20px;
}

.selected-movie-preview h3 {
  font-size: 1.2rem;
  color: #ffffff;
  margin-bottom: 10px;
}

.selected-movie-preview img {
  width: 150px; /* 포스터 크기 조정 */
  height: 225px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 10px;
}

.selected-movie-preview p {
  font-size: 1rem;
  color: #bbbbbb;
}

.recommendation-reason {
  width: 100%;
  height: 80px; /* 텍스트박스 높이 */
  padding: 10px;
  font-size: 14px;
  border: 1px solid #444;
  border-radius: 4px;
  background: #1f1f1f;
  color: #fff;
  resize: none;
}

.save-btn,
.close-modal-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  color: #fff;
  transition: background 0.3s;
}

.save-btn {
  background-color: #e02ff0; /* 완료 버튼 색상 */
}

.save-btn:hover {
  background-color: #ff3ff2ad; /* 호버 효과 */
}

.close-modal-btn {
  background-color: #505050; /* 닫기 버튼 색상 */
}

.close-modal-btn:hover {
  background-color: #505050a8; /* 호버 효과 */
}

/* 버튼 부모 요소: flexbox를 사용해 우측 정렬 및 한 줄 배치 */
.modal-actions {
  display: flex;
  justify-content: flex-end; /* 버튼을 우측 정렬 */
  gap: 10px; /* 버튼 간 간격 */
  margin-top: 20px; /* 상단 여백 */
}




.hidden {
  display: none; /* 숨김 */
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
</style>
