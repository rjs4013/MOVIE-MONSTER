<template>
  <div class="container">
    <button @click="goBack">전체 리뷰로 돌아가기</button>
    <div v-if="article">
      <!-- 제목 -->
      <h2>제목 : {{ article.title }}</h2>
      
      <div class="author-container">
        <div class="author">작성자: {{ article.user }}</div>
        <div class="date-info">
          <span>작성일: 2024-11-26 15:23</span>
          <span>수정일: 2024-11-26 15:27</span>
        </div>
      </div>
      

      <!-- 게시글 수정 및 삭제 버튼 -->
      <div v-if="isAuthor" class="article-actions">
        <button class="edit-article-button" @click="goToEdit">게시글 수정</button>
        <button class="delete-article-button" @click="deleteArticle">게시글 삭제</button>
      </div>

      <!-- 리뷰 내용 -->
      <div class="content-text">
        <h6>{{ article.content }}</h6>
      </div>

      <!-- 영화 정보 카드 -->
      <div class="movie-card" @click="navigateToMovieDetail(article.movie.movie_id)">
        <img
          v-if="article.movie.poster_url"
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

      <!-- 별점 -->
      <p class="rating-container">
        <span>별점:</span><div class="stars">
          <div
            v-for="(star, index) in store.displayStars(article.rating)"
            :key="index"
            class="star"
            :class="{ filled: star.filled }"
          ></div>
        </div>
      </p>

      <!-- 좋아요 및 댓글 섹션 -->
      <div class="like-comment-container">
        <button class="like-button" @click="toggleLike">
          <span v-if="article.is_liked" class="liked-icon">❤️</span>
          <span v-else class="like-icon">🤍</span>
        </button>
        <span class="like-count">{{ article.like_count }}</span>

        <div class="comment-count">
          <span class="comment-icon">💬</span>
          <span class="comment-count-value">{{ comments.length }}</span>
        </div>
      </div>

      <!-- 댓글 섹션 -->
      <div class="comment-section">
      <h3>댓글</h3>
      <div v-if="comments && comments.length > 0">
        <div class="comment-card" v-for="comment in comments" :key="comment.id">
          <div class="comment-header">
            <strong>{{ comment.user }} : </strong>
            <p class="comment-content">{{ comment.content }}</p>
            <div class="comment-actions" v-if="comment.user === store.Username">
              <button class="edit-button" @click="editComment(comment)">수정</button>
              <button class="delete-button" @click="removeComment(comment.id)">삭제</button>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p class="no-comments">댓글이 없습니다.</p>
      </div>

      <!-- 댓글 작성 -->
      <div v-if="!editingComment" class="comment-input-container">
        <textarea v-model="newComment" placeholder="댓글을 작성하세요"></textarea>
        <button class="submit-button" @click="submitComment">댓글 작성</button>
      </div>

      <!-- 댓글 수정 -->
      <div v-if="editingComment" class="comment-edit-container">
        <textarea v-model="updatedCommentContent"></textarea>
        <button class="submit-button" @click="submitUpdatedComment">수정 완료</button>
        <button class="cancel-button" @click="cancelEdit">취소</button>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";

const store = useCounterStore();
const route = useRoute();
const router = useRouter();

const article = ref(null); // 게시글 데이터
const comments = ref([]); // 댓글 목록
const newComment = ref(""); // 새로운 댓글 내용
const editingComment = ref(null); // 수정 중인 댓글
const updatedCommentContent = ref(""); // 수정 중인 댓글 내용
const isAuthor = ref(false); // 사용자가 작성자인지 여부

const toggleLike = async () => {
  try {
    const updatedArticle = await store.updateLikeStatus(article.value.id);

    // Local state 업데이트
    article.value.is_liked = updatedArticle.action === "added";
    article.value.like_count = updatedArticle.like_count;

    // store의 articles 상태도 업데이트
    const index = store.articles.findIndex((a) => a.id === article.value.id);
    if (index !== -1) {
      store.articles[index] = { ...article.value };
    }
  } catch (err) {
    console.error("좋아요 상태 업데이트 실패:", err);
  }
};

// 영화 디테일 페이지로 이동
const navigateToMovieDetail = (movieId) => {
  router.push({ name: "MovieDetail", params: { id: movieId } });
};

// 영화 포스터 URL 생성
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500";
  return `${baseUrl}${posterUrl}`;
};

// 게시글 및 댓글 데이터 가져오기
onMounted(() => {
  const articleId = route.params.id;
  fetchArticle(articleId);
  fetchComments(articleId);
  console.log('ooooooooo',article.value)
});

// 게시글 데이터 불러오기
const fetchArticle = (articleId) => {
  axios
    .get(`${store.API_URL}/api/v1/communities/${articleId}/`, {
      headers: { Authorization: `Token ${store.token}` },
    })
    .then((response) => {
      article.value = response.data;
      isAuthor.value = response.data.user === store.Username;
    })
    .catch((error) => {
      console.error("게시글 불러오기 실패:", error);
    });
};

// 댓글 목록 불러오기
const fetchComments = () => {
  axios
    .get(`${store.API_URL}/api/v1/communities/${route.params.id}/comments/list/`, {
      headers: { Authorization: `Token ${store.token}` },
    })
    .then((res) => {
      comments.value = res.data; // 댓글 목록 저장
    })
    .catch((err) => {
      console.error("댓글 불러오기 실패:", err);
    });
};

// 댓글 작성하기
const submitComment = () => {
  if (!newComment.value.trim()) {
    return; // 빈 댓글 방지
  }

  axios
    .post(
      `${store.API_URL}/api/v1/communities/${route.params.id}/comments/`,
      { content: newComment.value },
      { headers: { Authorization: `Token ${store.token}` } }
    )
    .then((res) => {
      const { comment, comment_count } = res.data;

      comments.value.push(comment);
      article.value.comment_count = comment_count;

      // store.articles에 최신 comment_count 반영
      const index = store.articles.findIndex((a) => a.id === article.value.id);
      if (index !== -1) {
        store.articles[index].comment_count = comment_count;
      }

      newComment.value = ""; // 입력 필드 초기화
    })
    .catch((err) => {
      console.error("댓글 작성 실패:", err);
    });
};

// 댓글 수정 시작
const editComment = (comment) => {
  editingComment.value = comment;
  updatedCommentContent.value = comment.content;
};

// 댓글 수정 완료
const submitUpdatedComment = () => {
  if (!updatedCommentContent.value.trim()) return;
  axios
    .put(
      `${store.API_URL}/api/v1/communities/${route.params.id}/comments/${editingComment.value.id}/update/`,
      { content: updatedCommentContent.value },
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    )
    .then((response) => {
      const index = comments.value.findIndex((c) => c.id === editingComment.value.id);
      if (index !== -1) {
        comments.value[index] = response.data;
      }
      editingComment.value = null;
      updatedCommentContent.value = "";
    })
    .catch((error) => {
      console.error("댓글 수정 실패:", error);
    });
};

// 댓글 삭제
const removeComment = (commentId) => {
  axios
    .delete(
      `${store.API_URL}/api/v1/communities/${route.params.id}/comments/${commentId}/delete/`,
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    )
    .then(() => {
      comments.value = comments.value.filter((comment) => comment.id !== commentId);

      article.value.comment_count = comments.value.length;

      // store.articles에도 최신 comment_count 반영
      const index = store.articles.findIndex((a) => a.id === article.value.id);
      if (index !== -1) {
        store.articles[index].comment_count = comments.value.length;
      }
    })
    .catch((error) => {
      console.error("댓글 삭제 실패:", error);
    });
};

// 댓글 수정 취소
const cancelEdit = () => {
  editingComment.value = null;
  updatedCommentContent.value = "";
};

// 게시글 삭제
const deleteArticle = () => {
  axios
    .delete(`${store.API_URL}/api/v1/communities/${article.value.id}/delete/`, {
      headers: { Authorization: `Token ${store.token}` },
    })
    .then(() => {
      alert("게시글이 삭제되었습니다.");
      router.push({ name: "ArticleView" }); // 전체 리뷰로 이동
    })
    .catch((error) => {
      console.error("게시글 삭제 실패:", error);
    });
};

// 뒤로가기
const goBack = () => {
  router.push({ name: "ArticleView" });
};

const goToEdit = () => {
  router.push({ name: 'EditView', params: { id: article.value.id } });
};

console.log('aa',article)
</script>

<style scoped>
/* 컨테이너 스타일 - 양쪽 마진 통일 */
.container {
  max-width: 1200px; /* 전체 페이지와 동일한 너비 */
  margin: 0 auto; /* 가운데 정렬 */
  padding: 0 20px; /* 좌우 여백 추가 */
  background-color: #1f1f1f;
}
/* 전체 페이지 스타일 */
body {
  background-color: #1c1c1c; /* 어두운 배경 */
  color: #fff; /* 기본 텍스트 색상 */
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
}

/* 컨테이너 스타일 */
div {
  padding: 7.5px;
}

/* 뒤로가기 버튼 스타일 */
button {
  background-color: #ff9f43; /* 오렌지 색상 */
  color: #fff;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}

button:hover {
  background-color: #ff6f3c; /* hover 시 더 어두운 오렌지 */
}

/* 제목 스타일 */
h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #f1c40f; /* 노란색 */
  text-align: center;
}

/* 작성자 정보 스타일 */
p {
  margin-bottom: 1px;
  margin-left: 10px;
  font-size: 14px;
}

p span {
  font-weight: bold;
  color: #ff9f43; /* 오렌지 */
}

/* 영화 카드 스타일 */
.movie-card {
  display: flex;
  gap: 15px;
  background-color: #2c2c2c; /* 어두운 회색 배경 */
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease;
}

.movie-card:hover {
  transform: scale(1.02);
}

.poster-image {
  width: 100px;
  height: 150px;
  border-radius: 8px;
  object-fit: cover;
}

.movie-info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: #fff;
}

.movie-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.movie-genres {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.genre {
  background-color: #ff9f43;
  padding: 2px 8px;
  font-size: 12px;
  border-radius: 4px;
  color: #fff;
}

.movie-overview {
  font-size: 14px;
  color: #bbb;
}

.movie-rating {
  font-weight: bold;
  color: #f1c40f; /* 노란색 */
  font-size: 16px;
  margin-top: 10px;
}

.content-text {
  margin-bottom: 70px;
}

/* 별점 컨테이너 */
.rating-container {
  display: flex;
  align-items: center;
  gap: 0px; /* 별 사이 간격 */
  margin: 0;
  padding: 0;
}

.stars {
  display: flex;
  gap: 0px;
  margin: -5px
}

.star {
  display: inline-block; /* 상속된 스타일 방지 */
  width: 5px; /* 원하는 별 크기 */
  height: 5px;
  box-sizing: border-box; /* 크기 계산 오류 방지 */
  background: url("/assets/images/gray-star.png") no-repeat center;
  background-size:  18px 18px; /* 별 이미지를 강제로 컨테이너 크기에 맞춤 */
}

.star.filled {
  background: url("/assets/images/yellow-star.png") no-repeat center;
  background-size: 18px 18px;; /* 별 이미지를 강제로 컨테이너 크기에 맞춤 */
}

/* 좋아요 및 댓글 섹션 */
.like-comment-container {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
  justify-content: center;
}

.like-button {
  display: flex;
  align-items: center;
  border: none;
  background: transparent;
  cursor: pointer;
  margin-bottom : 38px;
}

.like-icon,
.liked-icon {
  font-size: 23px;
  color: #ff6b6b;
  vertical-align: middle; /* 수직 정렬을 중앙으로 */
  margin-top: 20px; /* 아이콘을 살짝 아래로 내림 */
}

.like-count {
  font-size: 16px;
  color: #fff;
}

.comment-count {
  display: flex;
  align-items: center;
  gap: 5px;
}

.comment-section {
  margin-top: -25px;
}

.comment-content-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.comment-card {
  background-color: #2c2c2c;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  max-height: 100px;
  margin-left: auto;
  margin-right: auto;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-icon {
  font-size: 24px;
  color: #fff;
  margin-right: 25px;
}

.comment-content {
  font-size: 14px;
  color: #ddd;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex-grow: 1;
}

.comment-count-value {
  font-size: 16px;
  color: #fff;
}

.rating-container span {
  margin-right: 0px; /* 간격 강제 조정 */
  line-height: 1; /* 텍스트 라인 높이 조정 */
  display: inline-block; /* 텍스트가 중앙에 정렬되도록 설정 */
}

.no-comments {
  color: #888;
  text-align: center;
  margin-top: 20px;
}

.comment-input-container,
.comment-edit-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

/* 댓글 섹션 스타일 */
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #444;
  border-radius: 5px;
  background-color: #333;
  color: #fff;
  font-size: 14px;
  resize: none;
}


textarea:focus {
  outline: none;
  border-color: #ff9f43;
}

/* 댓글 목록 */
.comment-list {
  margin-top: 20px;
  padding: 15px;
  background-color: #2c2c2c;
  border-radius: 5px;
}

.comment-list p {
  margin-bottom: 10px;
}

.comment-list strong {
  color: #ff9f43;
}

/* 댓글 작성 버튼 */
.comment-list button {
  background-color: #ff9f43;
  border: none;
  border-radius: 5px;
  color: #fff;
  padding: 5px 10px;
  font-size: 14px;
  cursor: pointer;
  margin-left: 5px;
  transition: background-color 0.3s ease;
}

.comment-list button:hover {
  background-color: #ff6f3c;
}

/* 작성일과 수정일 위치 */
.date-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #bbb;
  margin-bottom: 10px;
  border-bottom: 2px solid #ff9800;
}

/* 내용 스타일 */
.content-container {
  margin-top: 20px;
  margin-bottom: 30px;
  padding: 15px;
  background-color: #fff; /* 어두운 회색 배경 */
  border-radius: 8px;
  color: #2c2c2c ;
  font-size: 14px;
  line-height: 1.6;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

textarea::placeholder {
  color: #888;
}

.submit-button {
  background-color: #ff9f43;
  color: #fff;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #ff7a29;
}

.cancel-button {
  background-color: #555;
  color: #fff;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #777;
}

.edit-button,
.delete-button {
  background-color: transparent;
  color: #ff9f43;
  border: none;
  cursor: pointer;
  font-size: 14px;
  transition: color 0.3s;
}

.edit-button:hover,
.delete-button:hover {
  color: #ff7a29;
}

/* 게시글 수정 및 삭제 버튼 스타일 */
.article-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.edit-article-button,
.delete-article-button {
  background-color: #ff9f43;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.edit-article-button:hover,
.delete-article-button:hover {
  background-color: #ff6f3c;
}
.titlebottom {
  justify-content: space-between;
}

.author-container {
  display: flex; /* 요소들을 가로로 정렬 */
  justify-content: space-between; /* 양 끝에 요소 배치 */
  align-items: center; /* 세로로 가운데 정렬 */
  width: 100%; /* 컨테이너의 너비를 부모에 맞춤 */
  padding: 0.5rem 0; /* 위아래 여백 */
  border-bottom: 2px solid #ff9800;
}

.author {
  font-size: 1rem;
  color: #fff;
}

.date-info {
  display: flex;
  gap: 1rem; /* 작성일과 수정일 사이 간격 */
  font-size: 0.9rem;
  color: #ccc;
}
</style>
