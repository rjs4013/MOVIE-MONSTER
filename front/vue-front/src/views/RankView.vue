<template>
  <div class="ranking-container">
    <h1 class="text-center tracking-in-expand-fwd my-4">MOVIE MONSTER RANKING</h1>
    <!-- 랭크 시스템 안내 버튼 -->
    <div class="info-container">
      <a href="#" class="rankinfo" @click="showModal = true">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        랭크 시스템 안내
      </a>
    </div>



    <table class="ranking-table">
      <thead>
        <tr>
          <th class="with-border">순위</th>
          <th>프로필</th>
          <th>이름</th>
          <th>랭크</th>
          <th>게시물 수</th>
          <th>좋아요 수</th>
          <th>팔로워 수</th>
          <th>추천 영화</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(user, index) in rankings"
          :key="user.id"
          :class="{ 'text-focus-in': animatedIndexes.includes(index), hidden: !animatedIndexes.includes(index) }"
        >
          <!-- 순위 -->
          <td class="with-border">
            <div v-if="index === 0">
              <img src="@/assets/gold.png" alt="Gold Medal" class="medal-icon" />
            </div>
            <div v-else-if="index === 1">
              <img src="@/assets/silver.png" alt="Silver Medal" class="medal-icon" />
            </div>
            <div v-else-if="index === 2">
              <img src="@/assets/bronze.png" alt="Bronze Medal" class="medal-icon" />
            </div>
            <div v-else>{{ index + 1 }}</div>
          </td>
          <!-- 프로필 -->
          <td>
            <div class="profile-picture">
              <img :src="`http://127.0.0.1:8000${user.profile_picture}`" alt="프로필 사진" class="profile-img" />
            </div>
          </td>
          <!-- 이름 -->
          <td>
            <RouterLink :to="{ name: 'ProfileView', params: { username: user.username } }">
              {{ user.username }}
            </RouterLink>
          </td>
          <!-- 랭크 -->
          <td>
            <div class="rank-display">
              <img :src="getRankImage(user.rank_title)" :alt="user.rank_title" class="rank-icon" />
              {{ user.points }}
            </div>
          </td>
          <!-- 게시물 수 -->
          <td>{{ user.articles_count }}</td>
          <!-- 좋아요 수 -->
          <td>{{ user.likes_count }}</td>
          <!-- 팔로워 수 -->
          <td>{{ user.followers_count }}</td>
          <!-- 추천 영화 -->
          <td>
            <div v-if="user.recommended_movie">
              <RouterLink :to="{ name: 'MovieDetail', params: { id: user.recommended_movie.movie.id } }">
                {{ user.recommended_movie.movie.title }}
              </RouterLink>
            </div>
            <div v-else>
              <span>X</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- RankInfoModal 컴포넌트 -->
    <RankInfoModal v-if="showModal" :isVisible="showModal" @close="showModal = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import RankInfoModal from "@/components/RankInfoModal.vue";

// Pinia 상태 관리
const store = useCounterStore();
const rankings = computed(() => store.rankings); // 순위를 고정시키기 위한 데이터
const showModal = ref(false);

// 애니메이션 상태
const animatedIndexes = ref([]); // 애니메이션이 적용된 인덱스를 저장

const applySequentialAnimation = () => {
  rankings.value.forEach((_, index) => {
    setTimeout(() => {
      animatedIndexes.value.push(index);
    }, index * 300); // 각 행마다 300ms의 지연 추가
  });
};

// 랭크 이미지를 가져오는 함수
import bronzeRank from "@/assets/BronzeRank.png";
import silverRank from "@/assets/SilverRank.png";
import goldRank from "@/assets/GoldRank.png";
import platinumRank from "@/assets/PlatinumRank.png";
import diamondRank from "@/assets/DiamondRank.png";

const getRankImage = (rankTitle) => {
  switch (rankTitle) {
    case "Bronze": return bronzeRank;
    case "Silver": return silverRank;
    case "Gold": return goldRank;
    case "Platinum": return platinumRank;
    case "Diamond": return diamondRank;
    default: return bronzeRank;
  }
};

// 컴포넌트 로드 시 실행
onMounted(() => {
  if (!store.isLogin) {
    alert("로그인이 필요합니다.");
    store.router.push({ name: "LogInView" });
  } else {
    store.fetchRankings().then(() => {
      applySequentialAnimation(); // 순차적으로 애니메이션 적용
    });
  }
});
</script>


<style scoped>
.text-center {
  color: #4da0ff;
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

/* 랭킹 컨테이너 */
.ranking-container {
  max-width: 1000px; /* 테이블 컨테이너 고정 */
  margin: 40px auto;
  text-align: center;
  color: #f0f8ff; /* 연한 파랑 텍스트 */
  overflow-x: auto; /* 가로 스크롤 활성화 */
  padding-bottom: 10px; /* 스크롤 바와 겹치지 않도록 여백 추가 */
}

.info-container {
  text-align: right;
  margin-bottom: 15px;
}

/* 테이블 스타일 */
.ranking-table {
  width: 1000px; /* 고정된 테이블 너비 */
  border-collapse: separate;
  border-spacing: 0;
  background-color: #1a2a44; /* 테이블 배경색 - 진한 남색 */
  border: 1px solid #4169e1; /* 파랑색 외곽선 */
  table-layout: fixed; /* 고정된 레이아웃 */
}

.ranking-table th,
.ranking-table td {
  padding: 10px;
  text-align: center;
  background-color: #243653; /* 셀 배경색 - 중간 남색 */
  color: #e6f0ff; /* 텍스트 색상 - 연한 파랑 */
  border-bottom: 1px solid #4169e1; /* 파랑색 하단 경계선 */
  white-space: normal; /* 텍스트 줄바꿈 허용 */
  word-wrap: break-word; /* 긴 단어 줄바꿈 */
  overflow-wrap: break-word; /* 단어가 칸을 넘어가면 줄바꿈 */
  font-size: 0.9rem; /* 폰트 크기 조정 */
}

.ranking-table th {
  font-weight: bold;
  background-color: #2a4066; /* 헤더 배경 - 더 밝은 남색 */
  color: #f0faff; /* 헤더 텍스트 색상 */
  border-bottom: 1px solid #6090d0; /* 헤더 경계선 */
  font-size: 1rem; /* 헤더 글자 크기 */
}

.ranking-table th.with-border,
.ranking-table td.with-border {
  border-right: 1px solid #4169e1; /* 세로 구분선 */
}

.ranking-table tbody tr {
  border-bottom: 1px solid #4169e1; /* 행 경계선 */
}

/* 테이블 너비 조정 */
.ranking-table th:first-child,
.ranking-table td:first-child {
  width: 5%; /* 순위 */
}

.ranking-table th:nth-child(2),
.ranking-table td:nth-child(2) {
  width: 10%; /* 프로필 */
}

.ranking-table th:nth-child(3),
.ranking-table td:nth-child(3) {
  width: 15%; /* 이름 */
}

.ranking-table th:nth-child(4),
.ranking-table td:nth-child(4) {
  width: 10%; /* 랭크 */
}

.ranking-table th:nth-child(5),
.ranking-table td:nth-child(5) {
  width: 10%; /* 게시물 수 */
}

.ranking-table th:nth-child(6),
.ranking-table td:nth-child(6) {
  width: 10%; /* 좋아요 수 */
}

.ranking-table th:nth-child(7),
.ranking-table td:nth-child(7) {
  width: 10%; /* 팔로워 수 */
}

.ranking-table th:last-child,
.ranking-table td:last-child {
  width: 20%; /* 추천 영화 */
}

.medal-icon {
  width: 32px;
  height: 32px;
}

/* 프로필 이미지 */
.profile-img {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  object-fit: cover;
  border: 0.5px solid #87cefa; /* 연한 파랑 테두리 */
}

.rank-icon {
  width: 40px;
  height: 40px;
  object-fit: cover;
}

/* 라우터 링크 스타일 */
.ranking-table a {
  color: #e6f0ff; /* 링크 글자색을 셀과 동일하게 설정 */
  text-decoration: none; /* 밑줄 제거 */
  font-weight: normal;
}

.ranking-table a:hover {
  color: #87cefa; /* 호버 시 연한 파랑색 */
  text-decoration: underline; /* 호버 시 밑줄 표시 */
}

/* 애니메이션 */
.text-focus-in {
  animation: text-focus-in 1s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
}

@keyframes text-focus-in {
  0% {
    filter: blur(12px);
    opacity: 0;
  }
  100% {
    filter: blur(0px);
    opacity: 1;
  }
}

/* 숨김 */
.hidden {
  opacity: 0;
}


/* 네온 버튼 스타일 */
.rankinfo {
  position: relative;
  display: inline-block;
  padding: 15px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
    margin: 20px 0; /* 여백 조정 */
  color: #4169e1;
  text-decoration: none;
  text-transform: uppercase;
  transition: 0.5s;
  letter-spacing: 1px;
  overflow: hidden;
  /* margin-right: 20px; */
  margin-top: 40px;
  margin-bottom: 0px;
}

.rankinfo:hover {
  background: #4169e1;
  color: #050801;
  box-shadow: 0 0 5px #4169e1, 0 0 25px #4169e1, 0 0 50px #4169e1,
    0 0 200px #4169e1;
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0005);
}

.rankinfo span {
  position: absolute;
  display: block;
}

.rankinfo span:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #4169e1);
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

.rankinfo span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #4169e1);
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

.rankinfo span:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #4169e1);
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

.rankinfo span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #4169e1);
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
