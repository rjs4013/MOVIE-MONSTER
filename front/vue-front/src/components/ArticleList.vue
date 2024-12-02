<template>
  <div>
    <!-- <h3>리뷰 목록</h3> -->

    <!-- 정렬 버튼 -->
    <div class="tabs-container">
      <button @click="setSortOrder('popular')" :class="{ active: sortOrder === 'popular' }">인기순</button>
      <button @click="setSortOrder('recent')" :class="{ active: sortOrder === 'recent' }">최신순</button>
    </div>

    <div v-if="store.articles.length === 0">
      <p>등록된 리뷰가 없습니다.</p>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="articles.length > 0">
      <ArticleListItem
        v-for="article in articles"
        :key="article.id"
        :article="article"
        @update-article="updateArticle"
      />
    </div>
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue'
import { useCounterStore } from '@/stores/counter'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const searchQuery = ref('')
const errorMessage = ref('')
const router = useRouter()

const store = useCounterStore()

const articles = computed(() => store.articles);
console.log('vvv',articles)

const sortOrder = ref('recent') // 기본 정렬 기준: 최신순

// 정렬 버튼 클릭 시 정렬 기준 변경
const setSortOrder = (order) => {
  sortOrder.value = order
  store.getSortedArticles(order) // 정렬된 데이터 가져오기
}

const updateArticle = (updatedArticle) => {
  const index = store.articles.findIndex((article) => article.id === updatedArticle.id);
  if (index !== -1) {
    store.articles[index] = { ...updatedArticle };
    console.log("Updated article in parent component:", store.articles[index]);
  }
};



// 컴포넌트 마운트 시 초기 데이터 로드
onMounted(async () => {
  try {
    // // 데이터가 없거나 강제로 새로 고침이 필요한 경우만 호출
    // if (!store.articles.length) {
      await store.getSortedArticles(sortOrder.value);
    
    console.log('dfdf', articles.value)
  } catch (err) {
    console.error("Error loading articles:", err);
    errorMessage.value = "게시글을 불러오는 중 오류가 발생했습니다.";
  }
});

</script>


<style scoped>
/* 탭 스타일링 */
.tabs-container {
  display: flex;
  justify-content: flex-start;
  gap: 25px; /* 탭 간 간격을 넓혀서 더 명확히 구분 */
  border-bottom: 2px solid #ff9800; /* 탭 아래에 강조선 추가 */
  padding-bottom: 10px; /* 탭과 아래 내용 간격을 넉넉히 */
  margin-bottom: 25px; /* 리뷰 목록과의 간격 추가 */
}

.tabs-container button {
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 18px;
  color: #888888; /* 기본 탭 색상: 회색 */
  transition: color 0.3s, border-bottom 0.3s;
  font-weight: 600;
}

.tabs-container button.active {
  color: #ffffff; /* 활성화된 탭 색상: 흰색 */
  border-bottom: 3px solid #ffffff; /* 활성화된 탭 하단 강조선 */
}

/* 에러 메시지 스타일 */
.error-message {
  color: #ff4d4d; /* 빨간색으로 강조 */
  margin-top: 20px;
}

/* 리뷰가 없을 때 메시지 스타일 */
.empty-message {
  color: #cccccc; /* 조금 더 밝은 회색 */
  font-size: 18px;
  text-align: center; /* 중앙 정렬 */
  margin-top: 30px;
}
</style>