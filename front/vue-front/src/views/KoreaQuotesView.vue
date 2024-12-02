<template>
  <div class="container">
    <h1 class="text-center-title my-4">한국영화 명대사</h1>

    <div v-if="gameOver" class="text-center">
      <h2>게임 종료!</h2>
      <p>모든 문제를 완료하였습니다.</p>
      <p>정답 수: {{ correctCount }} / {{ totalQuestions }}</p>
      <p>획득 가능한 포인트 : {{ 10 * correctCount }}</p>

      <!-- 포인트 획득하기 버튼 -->
      <a
        class="mt-3 add_point"
        href="#"
        @click.prevent="openConfirmModal('claim')"
        data-bs-toggle="modal"
        data-bs-target="#confirmModal"
      >
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        포인트 획득하기
      </a>


      <!-- 게임 재시작 버튼 -->
      <a
        class="mt-3 replay"
        href="#"
        @click.prevent="restartGame"
      >
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        다시 시작하기
      </a>

      <!-- 랭크 확인하기 버튼 -->
      <a
        class="mt-3 confirm_rank"
        href="#"
        @click.prevent="openConfirmModal('rank')"
        data-bs-toggle="modal"
        data-bs-target="#confirmModal"
      >
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        랭크 확인하기
      </a>
    </div>

    <div v-else>
      <p class="text-center">문제 {{ currentQuestionIndex + 1 }} / {{ totalQuestions }}</p>

      <div v-if="!showResult" class="review-container text-center">
        <!-- 타이핑 효과 -->
        <div id="typing-box">
          <span class="typing-text"></span><span class="blink">|</span>
        </div>
        <div class="input-container">
          <input
            v-model="userAnswer"
            class="form-control input-field"
            type="text"
            placeholder="정답(영화 제목)을 입력하세요"
            @keyup.enter="checkAnswer"
          />
          <button class="btn btn-success submit-btn" @click="checkAnswer">></button>
        </div>
      </div>

      <div v-if="showResult" class="result-container text-center mt-4">
        <h5 v-if="isCorrect" class="text-success">정답입니다! 🎉</h5>
        <h5 v-else class="text-danger">틀렸습니다. 정답은 "{{ currentquote.title[0] }}" 입니다. ❌</h5>
        <img
          :src="getPosterUrl(currentquote.title[0])"
          class="img-fluid poster"
          alt="영화 포스터"
        />
        <button class="btn btn-secondary next-btn" @click="nextReview">></button>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <p class="modal-title">포인트 획득하기</p>
          <button class="btn-close" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <p>{{ modalMessage }}</p>
          <p>포인트를 획득하시면 8시간에 재도전 가능합니다!</p>
          <div class="modal-actions">
            <button class="btn btn-create" @click="handleModalConfirm">확인</button>
            <button class="btn btn-cancel" @click="closeModal">취소</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const COOLDOWN_KEY = "KoreaQuotesView"; // 고유 키 설정

import { ref, onMounted, nextTick } from "vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

export default {
  setup() {
    const reviews = ref([]);
    const selectedQuotes = ref([]);
    const currentquote = ref({});
    const currentQuestionIndex = ref(0);
    const totalQuestions = ref(5);
    const userAnswer = ref("");
    const isCorrect = ref(false);
    const showResult = ref(false);
    const gameOver = ref(false);
    const correctCount = ref(0);

    // 모달 관련 데이터와 메서드
    const showModal = ref(false); // 모달 표시 여부
    const modalMessage = ref(""); // 모달 메시지
    const modalAction = ref(""); // 모달에서 수행할 액션

    const router = useRouter();
    const store = useCounterStore();

    const setCooldown = () => {
      localStorage.setItem(COOLDOWN_KEY, Date.now());
    };

    const openConfirmModal = (action) => {
      modalAction.value = action;
      modalMessage.value = `${10 * correctCount.value}p를 획득 하시겠어요?`;
      showModal.value = true; // 모달 열기
    };

    const closeModal = () => {
      showModal.value = false; // 모달 닫기
    };

    const handleModalConfirm = async () => {
      if (modalAction.value === "claim") {
        await claimPoints();
        setCooldown();
      } else if (modalAction.value === "rank") {
        await goToRank();
        setCooldown();
      }
      closeModal();
    };

    const handleModalCancel = () => {
      modalMessage.value = "";
    };

    const claimPoints = async () => {
      if (correctCount.value > 0) {
        await updatePoints(correctCount.value * 10);
      }
      await store.fetchUserPoints();
      router.push({ name: "GameView" });
    };

    const goToRank = async () => {
      if (correctCount.value > 0) {
        await updatePoints(correctCount.value * 10);
      }
      await store.fetchUserPoints();
      router.push({ name: "RankView" });
    };

    const updatePoints = async (points) => {
      try {
        await axios.post(
          `${store.API_URL}/accounts/user/points/`,
          { points },
          {
            headers: {
              Authorization: `Token ${store.token}`,
            },
          }
        );
        store.points += points;
      } catch (error) {
        console.error("Error updating points:", error);
      }
    };

    const restartGame = () => {
      currentQuestionIndex.value = 0;
      correctCount.value = 0;
      gameOver.value = false;
      userAnswer.value = "";
      showResult.value = false;
      isCorrect.value = false;
      selectRandomReviews();
      currentquote.value = selectedQuotes.value[currentQuestionIndex.value];

      // 타이핑 효과를 초기화하고 다시 실행
      nextTick(() => typingEffect(currentquote.value.movietext));
    };

    const fetchReviews = async () => {
      try {
        const response = await axios.get("/korea_movies_quotes.json");
        reviews.value = response.data;
        selectRandomReviews();
        currentquote.value = selectedQuotes.value[currentQuestionIndex.value];
        await nextTick();
        typingEffect(currentquote.value.movietext); // 타이핑 효과 시작
      } catch (error) {
        console.error("Error loading reviews:", error);
      }
    };

    const selectRandomReviews = () => {
      const shuffled = reviews.value.sort(() => 0.5 - Math.random());
      selectedQuotes.value = shuffled.slice(0, totalQuestions.value);
    };

    const checkAnswer = () => {
      if (userAnswer.value.trim() === "") return;
      isCorrect.value = currentquote.value.title.some(
        (correctTitle) =>
          userAnswer.value.trim().toLowerCase() === correctTitle.toLowerCase()
      );
      if (isCorrect.value) {
        correctCount.value += 1;
      }
      showResult.value = true;
    };

    const nextReview = () => {
      userAnswer.value = "";
      showResult.value = false;
      isCorrect.value = false;
      currentQuestionIndex.value += 1;
      if (currentQuestionIndex.value < totalQuestions.value) {
        currentquote.value = selectedQuotes.value[currentQuestionIndex.value];
        nextTick(() => typingEffect(currentquote.value.movietext)); // 다음 문제 타이핑 효과
      } else {
        gameOver.value = true;
      }
    };

    const getPosterUrl = (title) => `/korea_movie_poster/${title}.jpg`;

    const typingEffect = (text) => {
      const typingText = document.querySelector(".typing-text");
      typingText.textContent = "";
      let idx = 0;
      const type = () => {
        if (idx < text.length) {
          typingText.textContent += text[idx++];
          setTimeout(type, 100);
        }
      };
      type();
    };

    onMounted(() => {
      fetchReviews();
    });

    return {
      reviews,
      selectedQuotes,
      currentquote,
      currentQuestionIndex,
      totalQuestions,
      userAnswer,
      isCorrect,
      showResult,
      gameOver,
      correctCount,
      showModal,
      modalMessage,
      modalAction,
      openConfirmModal,
      closeModal,
      handleModalConfirm,
      handleModalCancel,
      claimPoints,
      goToRank,
      restartGame,
      fetchReviews,
      selectRandomReviews,
      checkAnswer,
      nextReview,
      getPosterUrl,
      modalMessage,
      setCooldown,
    };
  },
};
</script>


<style scoped>
.container {
  margin-top: 40px;
}

.poster {
  width: 350px; /* 고정 너비 */
  height: 525px; /* 고정 높이 */
  object-fit: cover; /* 이미지가 고정 크기에 맞게 잘림 */
  border-radius: 10px; /* 모서리 둥글게 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 약간의 그림자 추가 */
  margin-top: 15px; /* 위아래 간격 */
  margin-right: 20px;
}

.input-container {
  display: flex; /* Flexbox로 정렬 */
  justify-content: center; /* 중앙 정렬 */
  align-items: center; /* 수직 정렬 */
  gap: 10px; /* 텍스트 입력란과 버튼 사이 간격 */
}

.input-field {
  margin-top: 155px;
  width: 350px; /* 입력란의 너비를 줄임 */
  height: 40px; /* 입력란 높이 조정 */
  font-size: 14px; /* 글자 크기 조정 */
}

.submit-btn {
  margin-top: 155px;
  margin-left: 10px;
  height: 40px; /* 버튼 높이 입력란과 동일하게 설정 */
  font-size: 18px; /* 버튼 글자 크기 조정 */
  padding: 0 15px; /* 좌우 여백 추가 */
}

.next-btn {
  margin-top: 10px;
  height: 40px; /* 버튼 높이 입력란과 동일하게 설정 */
  font-size: 18px; /* 버튼 글자 크기 조정 */
  padding: 0 15px; /* 좌우 여백 추가 */
}


.text-center-title {
  color: #4caf50;
  text-align: center;
}

#typing-box {
  font-size: 1.5rem;
  color: #dddddd;
  margin-top: 120px;
}

.blink {
  animation: blink 0.5s infinite;
}

@keyframes blink {
  to {
    opacity: 0;
  }
}

/* 포인트획득하기 버튼: 네온 스타일 */
.add_point {
  position: relative;
  display: inline-block;
  padding: 15px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
    margin: 50px 0; /* 여백 조정 */
  color: #4caf50;
  text-decoration: none;
  text-transform: uppercase;
  transition: 0.5s;
  letter-spacing: 1px;
  overflow: hidden;
  margin-right: 20px;
  margin-top: 40px;
}

.add_point:hover {
  background: #4caf50;
  color: #050801;
  box-shadow: 0 0 5px #4caf50, 0 0 25px #4caf50, 0 0 50px #4caf50,
    0 0 200px #4caf50;
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0005);
}

.add_point span {
  position: absolute;
  display: block;
}

.add_point span:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #4caf50);
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

.add_point span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #4caf50);
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

.add_point span:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #4caf50);
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

.add_point span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #4caf50);
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

/* 다시 시작하기 버튼: 네온 스타일 */
.replay {
  position: relative;
  display: inline-block;
  padding: 15px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
    margin: 50px 0; /* 여백 조정 */
  color: #f54a4a;
  text-decoration: none;
  text-transform: uppercase;
  transition: 0.5s;
  letter-spacing: 1px;
  overflow: hidden;
  margin-right: 20px;
  margin-top: 40px;
}

.replay:hover {
  background: #f54a4a;
  color: #050801;
  box-shadow: 0 0 5px #f54a4a, 0 0 25px #f54a4a, 0 0 50px #f54a4a,
    0 0 200px #f54a4a;
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0005);
}

.replay span {
  position: absolute;
  display: block;
}

.replay span:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #f54a4a);
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

.replay span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #f54a4a);
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

.replay span:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #f54a4a);
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

.replay span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #f54a4a);
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

/* 랭크 확인하기 버튼: 네온 버튼 스타일 */
.confirm_rank {
  position: relative;
  display: inline-block;
  padding: 15px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
    margin: 50px 0; /* 여백 조정 */
  color: #3358ff;
  text-decoration: none;
  text-transform: uppercase;
  transition: 0.5s;
  letter-spacing: 1px;
  overflow: hidden;
  margin-right: 20px;
  margin-top: 40px;
}

.confirm_rank:hover {
  background: #3358ff;
  color: #050801;
  box-shadow: 0 0 5px #3358ff, 0 0 25px #3358ff, 0 0 50px #3358ff,
    0 0 200px #3358ff;
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0005);
}

.confirm_rank span {
  position: absolute;
  display: block;
}

.confirm_rank span:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #3358ff);
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

.confirm_rank span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #3358ff);
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

.confirm_rank span:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #3358ff);
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

.confirm_rank span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #3358ff);
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

/* 모달 전체 배경 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

/* 모달 컨테이너 */
.modal-content {
  background: linear-gradient(145deg, #1e1e1e, #2c2c2c);
  color: white;
  padding: 20px;
  border-radius: 15px;
  width: 500px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4), 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
}

/* 모달 헤더 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 10px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
}

/* 닫기 버튼 */
.btn-close {
  background: none;
  border: none;
  color: #ccc;
  font-size: 2rem;
  cursor: pointer;
  transition: color 0.3s ease;
}
.btn-close:hover {
  color: #fff;
}

/* 모달 본문 */
.modal-body p {
  font-size: 1rem;
  margin-bottom: 20px;
  color: #eee;
}

/* 모달 하단 버튼 */
.modal-actions {
  display: flex;
  justify-content: space-around;
}

.btn-create {
  background: #3a3a3a;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}
.btn-create:hover {
  background: #555555;
}

.btn-cancel {
  background: #c0392b;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}
.btn-cancel:hover {
  background: #e74c3c;
}

</style>
