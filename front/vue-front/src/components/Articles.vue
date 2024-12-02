<template>
  <div>
    <h1>게시글 목록</h1>
    <div v-if="loading">로딩 중...</div>
    <div v-else>
      <div v-for="article in articles" :key="article.id" class="article">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../axios"; // Axios 설정 파일

export default {
  data() {
    return {
      articles: [],
      loading: true,
    };
  },
  async created() {
    try {
      const response = await axios.get("/communities/articles/");
      this.articles = response.data; // Django API 응답
      this.loading = false;
    } catch (error) {
      console.error("API 요청 실패:", error);
      alert("데이터를 불러오는 데 실패했습니다.");
      this.loading = false;
    }
  },
};
</script>

<style>
.article {
  margin: 10px 0;
}
</style>
