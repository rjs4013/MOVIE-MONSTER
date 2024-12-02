<template>
  <div class="background-container"></div>
  <div class="app-wrapper">
    <header>
      <nav class="navbar">
        <div class="container">
          <img class="logoimage" src="/assets/logos/Monster Logo.png" alt="로고이미지">
          <!-- 네비게이션 링크 -->
          
          <RouterLink :to="{ name: 'HomeView' }" class="nav-link">HOME</RouterLink> |
          <RouterLink :to="{ name: 'MovieView' }" class="nav-link">MOVIE</RouterLink> |
          <RouterLink :to="{ name: 'ArticleView' }" class="nav-link">REVIEW</RouterLink> |
          <RouterLink :to="{ name: 'GameView' }" class="nav-link">GAME</RouterLink> |
          <RouterLink :to="{ name: 'RankView' }" class="nav-link">RANKING</RouterLink> |

          <RouterLink
            v-if="isLogin && user.username"
            :to="{ name: 'ProfileView', params: { username: user.username || '' } }"
            class="nav-link"
          >
            MY PROFILE
          </RouterLink>
          
          <div v-else>
            <RouterLink :to="{ name: 'LogInView' }" class="nav-link">로그인</RouterLink>
            <RouterLink :to="{ name: 'SignUpView' }" class="nav-link">회원가입</RouterLink>
          </div>

          <!-- 사용자 정보 -->
          <div class="user-info" v-if="!isLoading && user.username">
            <div v-if="user.rank_title" class="rank-display">
              <img :src="getRankImage(user.rank_title)" :alt="user.rank_title" class="rank-icon" />
            </div> |
            {{ user.username }} | Points: {{ user.current_points }}
          </div>

          <form @submit.prevent="logOut" v-if="isLogin">
            <input type="submit" value="로그아웃">
          </form>
        </div>
      </nav>
    </header>
    <main class="content">
      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="loading">
        <p>Loading...</p>
      </div>
      <!-- 동적 라우터 뷰 -->
      <RouterView v-else />
    </main>

    <!-- 위로 이동 버튼 -->
    <button v-if="showScrollToTop" class="scroll-to-top" @click="scrollToTop">
      ▲
    </button>

    <footer class="footer">
      <div class="footer-container">
        <!-- 왼쪽 섹션 -->
        <div class="footer-left">
          <p><strong>MovieMoster</strong> | 팀장 하건수 | <a href="mailto:rjs4013@naver.com">rjs4013@naver.com</a></p>
          <p>팀원 강혜경 | <a href="mailto:ghgghg96@naver.com">ghgghg96@naver.com</a> | 대표전화 010-1234-5678</p>
        </div>

        <!-- 오른쪽 섹션 -->
        <div class="footer-right">
          <p>Copyright &copy; 2024 by MovieMoster, Inc. All Rights Reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, ref, watchEffect, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const isLogin = computed(() => store.isLogin);
const user = computed(() => store.user);

const isLoading = ref(true); // 로딩 상태 관리
const showScrollToTop = ref(false); // 스크롤 버튼 표시 여부

// 랭크 이미지 불러오기
import bronzeRank from "@/assets/BronzeRank.png";
import silverRank from "@/assets/SilverRank.png";
import goldRank from "@/assets/GoldRank.png";
import platinumRank from "@/assets/PlatinumRank.png";
import diamondRank from "@/assets/DiamondRank.png";

// 랭크 이미지를 반환하는 함수
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

// 로그아웃 기능
const logOut = () => {
  store.logOut();
};

// 상태값이 로드되었는지 감지
watchEffect(async () => {
  if (store.token) {
    await store.fetchUser(); // 사용자 정보 로드
    await store.fetchUserPoints(); // 사용자 포인트 로드
    isLoading.value = false; // 로드 완료
  } else {
    isLoading.value = false; // 토큰이 없는 경우도 로드 완료로 처리
  }
});

// 스크롤에 따라 버튼 표시
const handleScroll = () => {
  showScrollToTop.value = window.scrollY > 300; // 스크롤이 300px 이상일 때 버튼 표시
};

// 위로 이동
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

</script>

<style scoped>
.scroll-to-top {
  position: fixed;
  bottom: 20px; /* 화면 하단에서 20px */
  right: 20px; /* 화면 우측에서 20px */
  width: 60px; /* 버튼 크기 */
  height: 60px; /* 버튼 크기 */
  background-color: #007bff; /* 파란색 배경 */
  border: none;
  border-radius: 50%; /* 원형 버튼 */
  color: #ffffff; /* 텍스트 흰색 */
  font-size: 20px; /* 텍스트 크기 */
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: transform 0.2s ease-in-out, background-color 0.3s ease;
}

.scroll-to-top:hover {
  background-color: #0056b3; /* 더 어두운 파란색 */
  transform: scale(1.1); /* 약간 확대 */
}

.scroll-to-top:active {
  transform: scale(0.9); /* 클릭 시 살짝 축소 */
}

.a11y-hidden {
    overflow: hidden;
    clip: rect(1px, 1px, 1px, 1px);
    position: absolute;
    width: 1px;
    height: 1px;
}

form input[type="submit"] {
  background: linear-gradient(135deg, #ff5858, #f09819); /* 그래디언트 색상 */
  border: none; /* 기본 테두리 제거 */
  color: white; /* 텍스트 색상 */
  padding: 10px 20px; /* 여백 설정 */
  font-size: 16px; /* 글씨 크기 */
  font-weight: bold; /* 글씨 굵기 */
  border-radius: 25px; /* 버튼 모서리를 둥글게 */
  cursor: pointer; /* 마우스 커서를 포인터로 변경 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* 그림자 추가 */
  transition: transform 0.2s ease, box-shadow 0.3s ease; /* 애니메이션 */
}

form input[type="submit"]:hover {
  transform: translateY(-2px); /* 살짝 위로 이동 */
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3); /* 호버 시 더 강한 그림자 */
}

form input[type="submit"]:active {
  transform: translateY(0); /* 클릭 시 원래 위치로 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* 클릭 시 그림자 감소 */
}

.logoimage {
  width: 60px;
  height: 50px;
  object-fit: cover;
}

.nav-link {
  position: relative;
  display: inline-block;
  padding: 10px 15px;
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  text-decoration: none;
  text-transform: uppercase;
  transition: color 0.3s ease-in-out, background-color 0.3s ease-in-out;
  z-index: 1;
}

.nav-link::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(224, 47, 240, 0.2), rgba(0, 0, 0, 0));
  border-radius: 5px;
  transform: scale(0.8);
  opacity: 0;
  transition: all 0.4s ease-in-out;
  z-index: -1; /* 텍스트 뒤로 가게 설정 */
}

.nav-link:hover {
  color: #e02ff0; /* 마우스 오버 시 텍스트 색상 */
}

.nav-link:hover::after {
  transform: scale(1);
  opacity: 1;
  background: linear-gradient(135deg, rgba(224, 47, 240, 0.4), rgba(0, 0, 0, 0));
  box-shadow: 0 0 15px rgba(224, 47, 240, 0.5), 0 0 20px rgba(224, 47, 240, 0.3);
}


</style>
