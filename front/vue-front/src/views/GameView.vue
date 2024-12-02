<template>
  <div class="container">
    <h1 class="text-center tracking-in-expand-fwd my-4">MOVIE MONSTER GAME</h1>

    <div class="game-list">
      <!-- 한국영화 명대사 -->
      <div
        class="game-card"
        :class="{ disabled: isDisabled('KoreaQuotesView') }"
        @click="handleGameClick('KoreaQuotesView', '한국영화 명대사')"
      >
        <img
          src="@/assets/koreansumnail.jpg"
          alt="한국영화 명대사"
          class="thumbnail"
        />
        <div class="badge difficulty-badge">쉬움</div>
        <div class="game-info">
          <h2>한국영화 명대사</h2>
          <p>느그 서장 남천동 살제?</p>
        </div>
      </div>

      <!-- 해외영화 명대사 -->
      <div
        class="game-card"
        :class="{ disabled: isDisabled('ForeignQuotesView') }"
        @click="handleGameClick('ForeignQuotesView', '해외영화 명대사')"
      >
        <img
          src="@/assets/foreignsumbnail.jpg"
          alt="해외영화 명대사"
          class="thumbnail"
        />
        <div class="badge difficulty-badge medium">중간</div>
        <div class="game-info">
          <h2>해외영화 명대사</h2>
          <p>Good afternoon, good evening,<br/> and good night!</p>
        </div>
      </div>

      <!-- 이동진의 한줄평 -->
      <div
        class="game-card"
        :class="{ disabled: isDisabled('OneLineView') }"
        @click="handleGameClick('OneLineView', '이동진의 한줄평')"
      >
        <img
          src="@/assets/leedongjin.jpg"
          alt="이동진의 한줄평"
          class="thumbnail"
        />
        <div class="badge difficulty-badge hard">어려움</div>
        <div class="game-info">
          <h2>이동진의 한줄평</h2>
          <p>안녕하세요. 평론계의 아이돌입니다.</p>
        </div>
      </div>
    </div>

    <!-- 모달 -->
    <div v-if="showModal" class="modal-overlay">
  <div class="modal-content">
    <p>{{ modalMessage }}</p>
    <div class="modal-actions">
      <button class="btn-cancel" @click="closeModal">닫기</button>
    </div>
  </div>
</div>

  </div>
</template>


<script>
export default {
  name: "GameView",
  data() {
    return {
      cooldownTime: 8 * 60 * 60 * 1000, // 8시간 제한 시간
      // cooldownTime: 2 * 60 * 1000, // 테스트용 시간조절(2분)
      showModal: false,
      modalMessage: "",
    };
  },
  methods: {
    handleGameClick(gameKey, gameName) {
      const lastPlayed = localStorage.getItem(gameKey);
      const now = Date.now();

      if (lastPlayed && now - lastPlayed < this.cooldownTime) {
        const remainingTime = this.cooldownTime - (now - lastPlayed);
        const hours = Math.floor(remainingTime / (1000 * 60 * 60));
        const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
        this.modalMessage = `${gameName}은(는) ${hours}시간 ${minutes}분 후에 다시 이용할 수 있습니다.`;
        this.showModal = true; // 모달 열기
      } else {
        this.$router.push({ name: gameKey }); // 게임 페이지로 이동
      }
    },
    isDisabled(gameKey) {
      const lastPlayed = localStorage.getItem(gameKey);
      const now = Date.now();
      return lastPlayed && now - lastPlayed < this.cooldownTime;
    },
    closeModal() {
      this.showModal = false;
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.text-center {
  color: #4caf50;
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

.game-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* 그리드 레이아웃 */
  gap: 25px;
  width: 100%;
  margin: 10px;
  padding: 20px;
}

.game-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative; /* 레이블 배치를 위해 */
  text-align: center;
  padding: 15px;
  border-radius: 15px;
  background: linear-gradient(145deg, #ffffff, #e6e6e6);
  transition: all 0.3s ease-in-out;
  animation: fadeIn 0.5s ease-in-out; /* 등장 애니메이션 */
  height: 500px; /* 세로 길이를 기존보다 늘림 */
  border: 2px solid #4caf50; /* 네온 효과 색상 */
  box-shadow: 0 0 10px #4caf50, 0 0 20px #4caf50; /* 네온 효과 추가 */
}

.game-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 15px #4caf50, 0 0 30px #4caf50; /* 호버 시 네온 효과 강화 */
}

.game-card.disabled {
  background-color: #777777;
  cursor: not-allowed;
  opacity: 0.5;
}

.thumbnail {
  width: 100%;
  max-height: 210px;
  margin-top: 50px;
  border-radius: 15px;
  object-fit: cover;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
}

.thumbnail:hover {
  transform: scale(1.05);
}

.difficulty-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #4caf50;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 0.9rem;
  font-weight: bold;
}

.difficulty-badge.medium {
  background: #ff9800; /* 중간 레이블 색상 */
}

.difficulty-badge.hard {
  background: #f44336; /* 어려움 레이블 색상 */
}

.game-info {
  color: #222222;
}

.game-info h2 {
  font-size: 2rem;
  font-weight: bold;
  margin-top: 50px;
}

.game-info p {
  margin-top: 20px;
  font-size: 1.2rem;
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

/* 닫기 버튼 컨테이너 */
.modal-actions {
  display: flex;
  justify-content: center; /* 버튼 중앙 정렬 */
  margin-top: 20px; /* 버튼 상단 여백 */
}

/* 닫기 버튼 */
.btn-cancel {
  align-items: center;
  background: #c0392b;
  border: none;
  width: 100px;
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
