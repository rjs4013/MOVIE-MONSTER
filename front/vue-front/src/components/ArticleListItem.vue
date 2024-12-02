<template>
  <div class="review-card">
    <!-- 작성자 정보 -->
    <div class="author-section" @click="navigateToReviewDetail(article.id)">
      <img
        v-if="article.user_profile_image"
        :src="`${store.API_URL}${article.user_profile_image}`"
        alt="프로필 이미지"
        class="profile-image"
        @click.stop="navigateToProfile(article.user)"
      />
      <div class="user-info">
        <p class="username">{{ article.user }}</p>
        <p class="created-at">{{ store.formatDate(article.created_at) }}</p>
        <p class="rating">⭐ {{ article.rating ? article.rating.toFixed(1) : 'N/A' }}</p>
      </div>
    </div>

    <!-- 리뷰 내용 -->
    <div class="review-content">
      <p class="review-text">{{ article.content }}</p>
    </div>

    <!-- 영화 정보 카드 -->
    <div v-if="article.movie" class="movie-card" @click="navigateToMovieDetail(article.movie.movie_id)">
      <img
        v-if="article.movie"
        :src="article.movie.poster_url"
        alt="영화 포스터"
        class="poster-image"
      />
      <div class="movie-info">
        <h4 class="movie-title">{{ article.movie.title }}</h4>
        <div class="movie-genres">
          <span v-for="genre in article.movie.genres" :key="genre" class="genre">
            {{ genre }}
          </span>
        </div>
        <p class="movie-overview">{{ article.movie.description }}</p>
        <p class="movie-rating">⭐ {{ article.movie.vote_avg ? article.movie.vote_avg.toFixed(1) : 'N/A' }}</p>
      </div>
    </div>
    <div v-else>
      <!-- 영화 정보가 없는 경우 보여줄 내용 -->
      <p>영화 정보가 없습니다.</p>
    </div>


     <!-- 좋아요 기능 -->
     <div class="like-container">
      <button class="like-button" @click="toggleLike">
        <!-- props.article.is_liked 대신 로컬 상태 isLiked 사용 -->
        <span v-if="isLiked" class="liked-icon">❤️</span>
        <span v-else class="like-icon">🤍</span>
      </button>
      <span class="like-count">{{ likeCount }}</span>

      <div class="comment-count" @click="navigateToReviewDetail(article.id)">
        <button class="like-button">
          <span class="comment-icon">💬</span>
          <span class="comment-count-value">{{ article.comment_count }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import axios from "axios"; // axios 임포트

const props = defineProps({ article: { type: Object, required: true } });
const emit = defineEmits(["update:article"]); // 부모에게 상태 전달 이벤트 정의


const store = useCounterStore();
const router = useRouter();

// 반응형 데이터
const article = ref({ ...props.article }); // props.article을 반응형으로 관리

const parseGenres = (genres) => {
  try {
    if (typeof genres === 'string') {
      return JSON.parse(genres);
    }
    return genres;  // 이미 배열이라면 그대로 반환
  } catch (e) {
    console.error("Failed to parse genres:", e);
    return [];  // 파싱 실패 시 빈 배열 반환
  }
};


// 초기화: props.article.is_liked를 기반으로 isLiked를 설정
const isLiked = ref(props.article.is_liked ?? false); // nullish coalescing: 없으면 false
const likeCount = ref(props.article.like_count ?? 0);

// 좋아요 토글
const toggleLike = async () => {
  try {
    const updatedArticle = await store.updateLikeStatus(article.value.id);

    // Local state 업데이트
    article.value.is_liked = updatedArticle.action === "added";
    article.value.like_count = updatedArticle.like_count;
    console.log('pp',article.value)

    // 부모 컴포넌트에 업데이트 알림
    emit("update-article", article.value);
  } catch (err) {
    console.error("좋아요 상태 업데이트 실패:", err);
  }
};


// Props 변경 감지
watch(
  () => props.article,
  (newArticle) => {
    if (newArticle) {
      console.log("Updated props.article:", newArticle);
      isLiked.value = newArticle.is_liked ?? false; // is_liked 반영
      likeCount.value = newArticle.like_count ?? 0; // like_count 반영
      console.log("Local state isLiked:", isLiked.value);
    }
  },
  { immediate: true } // 초기에도 실행
);

// 디테일 페이지 이동
const navigateToReviewDetail = (articleId) => {
  router.push({ name: "DetailView", params: { id: articleId } });
};

// 프로필 페이지 이동
const navigateToProfile = (username) => {
  router.push({ name: "ProfileView", params: { username } });
};

// 영화 디테일 페이지 이동
const navigateToMovieDetail = (movieId) => {
  router.push({ name: "MovieDetail", params: { id: movieId } });
};

// 포스터 URL 생성
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500";
  return `${baseUrl}${posterUrl}`;
};

console.log('pppppppppp',article.value.movie)
</script>


<style scoped>
/* 동일한 스타일 유지 */
.review-card {
  display: flex;
  flex-direction: column;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
  background-color: #f8f9fa;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
}

/* 작성자 정보 수평 정렬 */
.author-section {
  display: flex;
  align-items: center;
  gap: 5px; /* 간격 축소 */
  margin-bottom: 3px; /* 전체 하단 마진 축소 */
  cursor: pointer;
  /* border-bottom: 1px solid #ddd; */
  padding-bottom: 3px;
}

.profile-image {
  width: 40px; /* 크기 축소 */
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  margin-bottom: 80px;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px; /* 유저명, 작성일, 별점 간격 축소 */
}

.username {
  font-weight: bold;
  font-size: 18px; /* 크기 축소 */
  color: #000; /* 글자색 검정 */
}

.created-at {
  color: #000;
  font-size: 12px;
}

.rating {
  font-size: 15px;
  color: #f39c12;
  font-weight: bold;
}

/* 리뷰 내용 배치 조정 */
.review-content .review-text {
  font-size: 14px;
  margin-bottom: 10px;
  line-height: 1.4;
  color: #000; /* 글자색 검정 */
}

/* 영화 카드: 수평 정렬 */
.movie-card {
  display: flex;
  flex-direction: row;
  gap: 10px;
  align-items: flex-start;
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
  background-color: #d3d3d3; /* 배경색 회색 */
  margin-top: 10px;
  padding: 10px;
}
.movie-card:hover {
  transform: scale(1.02);
}

.poster-image {
  width: 80px; /* 크기 조정 */
  height: 120px;
  object-fit: cover;
}

.movie-info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 0;
  gap: 5px;
  color: #000; /* 텍스트 검정색 */
}

.movie-title {
  font-size: 14px; /* 크기 축소 */
  font-weight: bold;
  margin: 0;
  color: #000; /* 텍스트 검정색 */
}

.movie-genres {
  display: flex;
  gap: 5px;
  flex-wrap: wrap; /* 장르가 많을 경우 줄바꿈 */
  color: #000; /* 장르 텍스트 검정 */
}

.genre {
  background-color: #f1f1f1;
  padding: 2px 5px;
  font-size: 12px;
  border-radius: 4px;
  color: #000; /* 장르 텍스트 검정 */
}

.movie-overview {
  font-size: 12px;
  color: #000; /* 텍스트 검정색 */
  margin-top: 10px;
  line-height: 1.4;
}

.movie-rating {
  font-weight: bold;
  color: #f39c12;
}

/* 좋아요 기능 스타일 */
/* 좋아요 및 댓글 컨테이너 */
.like-container {
  display: flex;
  align-items: center;
  gap: 20px; /* 좋아요와 댓글 사이 간격 조정 */
  margin-top: 10px; /* 상단 마진 */
  justify-content: flex-start; /* 왼쪽 정렬 */
}

/* 좋아요 버튼 */
.like-button {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  cursor: pointer;
  gap: 22px; /* 아이콘과 숫자 사이 간격 */
  font-size: 14px; /* 숫자 크기 통일 */
  color: #000; /* 검정색 텍스트 */
  transition: color 0.3s ease; /* 색상 변화 애니메이션 추가 */
}

/* 좋아요 아이콘 */
.like-button:hover .like-icon,
.like-button:hover .liked-icon {
  color: #e74c3c; /* hover 시 빨간색으로 변경 */
}

.like-button:hover .like-count {
  color: #e74c3c; /* 좋아요 숫자도 hover 시 동일한 색상으로 변경 */
}

.like-icon,
.liked-icon {
  font-size: 20px; /* 좋아요 아이콘 크기 */
  color: #ff6b6b; /* 좋아요 아이콘 색상 */
}

/* 좋아요 숫자 */
.like-count {
  font-size: 14px; /* 숫자 크기 */
  color: #000; /* 숫자 색상 */
}

/* 댓글 버튼 */
.comment-count {
  display: flex;
  align-items: center;
  gap: 8px; /* 아이콘과 숫자 사이 간격 */
  font-size: 14px; /* 숫자 크기 통일 */
  color: #000; /* 검정색 텍스트 */
  transition: color 0.3s ease; /* 색상 변화 애니메이션 추가 */
}

.comment-count:hover .comment-icon {
  color: #3498db; /* hover 시 파란색으로 변경 */
}

.comment-count:hover .comment-count-value {
  color: #3498db; /* 댓글 숫자도 hover 시 동일한 색상으로 변경 */
}

/* 댓글 아이콘 */
.comment-icon {
  font-size: 20px; /* 댓글 아이콘 크기 */
  color: #000; /* 아이콘 색상 */
}

/* 댓글 숫자 */
.comment-count-value {
  font-size: 14px; /* 숫자 크기 */
  color: #000; /* 숫자 색상 */
}

</style>

