<template>
  <div class="modal-overlay" v-if="isVisible">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">랭크 시스템 안내</h5>
        <button class="btn-close" @click="closeModal" aria-label="Close Modal">&times;</button>
      </div>
      <div class="modal-body">
  <section class="faq-section">
    <h4>Q) 포인트는 무엇인가요?</h4>
    <p>
      포인트는 리뷰 작성과 게임 플레이를 통해 얻을 수 있는 MovieMoster의 보상 시스템입니다.<br/>
      <span class="highlight">리뷰 작성 시 10점, 게임의 정답 1개당 10점씩 포인트가 부여됩니다.</span>
    </p>
  </section>

  <section class="faq-section">
    <h4>Q) 포인트로 무엇을 할 수 있나요?</h4>
    <p>
      포인트는 누적되어 MovieMoster의 등급 시스템을 통해 등급이 부여됩니다.<br/>
      등급이 높을수록 <span class="highlight">RANK 페이지의 상단에 노출</span>되며, 커뮤니티에서 더 높은 신뢰도를 가지게 됩니다.
    </p>
  </section>

  <section class="faq-section">
    <h4>Q) 등급과 포인트 기준은 어떻게 되나요?</h4>
    <table class="rank-table">
      <thead>
        <tr>
          <th>등급</th>
          <th>누적 포인트</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Bronze</td><td>0</td></tr>
        <tr><td>Silver</td><td>1000</td></tr>
        <tr><td>Gold</td><td>2000</td></tr>
        <tr><td>Platinum</td><td>3000</td></tr>
        <tr><td>Diamond</td><td>4000+</td></tr>
      </tbody>
    </table>
    <p>
    포인트를 꾸준히 누적하면 등급이 상승하며, <span class="highlight">리뷰 작성</span>과 <span class="highlight">게임</span>을 통해 포인트를 얻을 수 있습니다.
  </p>
  </section>

  <section class="faq-section">
    <h4>Q) 게임 제한 시간은 어떻게 동작하나요?</h4>
    <p>
      각 게임은 플레이 후 일정 시간 동안 재시도가 제한됩니다.<br />
      제한 시간 동안 해당 게임은 비활성화 상태로 표시되며, 클릭 시 <span class="highlight">남은 시간 안내</span> 모달창이 나타납니다.<br />
      예) "이 게임은 3시간 12분 후에 다시 이용할 수 있습니다."
    </p>
  </section>

  <section class="faq-section">
    <h4>Q) 높은 등급의 유저는 어떤 혜택을 받을 수 있나요?</h4>
    <p>
      높은 등급의 유저는 커뮤니티에서 더 두드러진 노출과 인정을 받을 수 있습니다.<br />
      <ul>
        <li><span class="highlight">RANK 상단 노출</span>: 높은 등급 유저가 우선적으로 노출됩니다.</li>
        <li><span class="highlight">컬렉션 추천</span>: 높은 등급 유저의 콘텐츠가 홈 페이지에 우선 표시됩니다.</li>
      </ul>
    </p>
  </section>
</div>

      <div class="modal-actions">
        <button class="btn-cancel" @click="closeModal">닫기</button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { defineProps, defineEmits } from "vue";

defineProps(["isVisible"]);
const emit = defineEmits(["close"]);

const closeModal = () => {
  emit("close");
};
</script>

<style scoped>

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
  backdrop-filter: blur(1px); /* 배경 흐림 효과 */
}

/* 모달 컨테이너 */
.modal-content {
  background: linear-gradient(145deg, #1e1e1e, #2c2c2c);
  color: white;
  padding: 25px;
  border-radius: 15px;
  max-width: 80%;
  width: 800px;
  max-height: 90%;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4), 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: left;
  display: flex;
  flex-direction: column; /* 헤더, 본문, 액션 정렬 */
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
  font-size: 1.2rem;
  font-weight: bold;
}

/* 모달 본문 스크롤 추가 */
.modal-body {
  font-family: 'Arial', sans-serif;
  font-size: 1rem;
  color: #c7c7c7;
  line-height: 1.5;
  overflow-y: auto; /* 본문 스크롤 가능 */
  max-height: 60vh; /* 본문 최대 높이 설정 */
  padding-right: 15px; /* 스크롤 바 여백 */
  margin-bottom: 10px;
}

.modal-body h4 {
  font-size: 1.0rem;
  color: #c7c7c7;
}
.modal-body p {
  font-size: 0.8rem;
  color: #c7c7c7;
}

.modal-body table {
  width: 100%; /* 표 너비 줄이기 */
  margin: 20px auto; /* 중앙 정렬 */
  border-collapse: collapse;
}

.modal-body th,
.modal-body td {
  border: 1px solid #444; /* 테두리 설정 */
  padding: 8px; /* 안쪽 여백 */
  text-align: center; /* 글씨 중앙 정렬 */
  vertical-align: middle; /* 세로 중앙 정렬 */
}

.modal-body th {
  background-color: #555; /* 헤더 배경색 */
  color: #fff; /* 헤더 글씨색 */
  font-weight: bold;
}

.modal-body td {
  background-color: #444; /* 데이터 셀 배경색 */
  color: #ccc; /* 데이터 셀 글씨색 */
}


/* 모달 하단 버튼 고정 */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
  position: sticky; /* 모달 하단에 고정 */
  bottom: 0;
  background: linear-gradient(145deg, #1e1e1e, #2c2c2c);
  padding-top: 10px;
}

/* 닫기 버튼 스타일 */
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

.faq-section {
  margin-bottom: 40px;
}

.faq-section h4 {
  font-size: 1.2rem;
  color: #ffffff;
  margin-bottom: 10px;
  text-transform: capitalize;
}

.faq-section p {
  margin: 0;
}

.highlight {
  color: #00d1b2; /* 강조 색상 */
  font-weight: bold;
}

.rank-table {
  width: 100%;
  margin: 10px 0;
  border-collapse: collapse;
  background: #333;
  border: 1px solid #555;
}

.rank-table th,
.rank-table td {
  padding: 4px 6px; /* 셀 높이 줄이기 */
  text-align: center; /* 텍스트 중앙 정렬 */
  vertical-align: middle;
  height: 30px; /* 각 셀 높이를 일정하게 설정 */
  color: white;
  border: 1px solid #555;
}

.rank-table th {
  background-color: #333;
}

.rank-table td {
  background: #444;
  color: #ccc;
}

ul {
  padding-left: 20px;
}

ul li {
  list-style-type: disc;
  margin-bottom: 5px;
}


</style>