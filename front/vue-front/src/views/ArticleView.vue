<template>
  <div class="review-page-container">
    <h1 class="text-center tracking-in-expand-fwd my-4">MONSTER'S REVIEWS</h1>
    <!-- 페이지 상단: 리뷰 제목과 설명 -->
    <div class="header">
      <div class="title-section">
        <p>영화에 대한 유저들의 리뷰들을 모아봤어요.</p>
      </div>
      <RouterLink :to="{ name: 'CreateView' }" class="create-button">리뷰 작성하기</RouterLink>
    </div>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const store = useCounterStore()

onMounted(() => {
  // mount 되기 전에 store에 있는 전체 게시글 요청 함수를 호출
  store.getArticles()
})
</script>

<style scoped>
.text-center {
  padding-top: 20px;
  color: #ff9800;
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
.review-page-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 25px; /* 섹션 간 간격 */
  background-color: #1f1f1f; /* 배경색을 어두운 톤으로 설정하여 집중도를 높임 */
  border-radius: 10px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #ff9800; /* 탭 컨테이너와의 일관성을 위해 강조선 추가 */
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.header h1 {
  font-size: 28px;
  color: #ffffff; /* 색상을 하얀색으로 변경 */
  font-weight: bold; /* 글씨를 굵게 설정 */
}

.header p {
  font-size: 16px;
  color: #888888; /* 부드러운 회색으로 설명 추가 */
  margin: 0;
}

.create-button {
  padding: 10px 16px;
  background-color: #ff9800; /* 버튼 색상을 따뜻한 오렌지로 유지 */
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.create-button:hover {
  background-color: #e68900;
}
</style>
