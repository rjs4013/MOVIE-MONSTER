<template>
  <div
    ref="modalRef"
    class="modal fade"
    id="youtubeTrailerModal"
    tabindex="-1"
    aria-labelledby="youtubeTrailerLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content custom-modal-content">
        <div class="modal-header custom-modal-header">
          <h5 class="modal-title custom-modal-title" id="youtubeTrailerLabel">
            {{ movieTitle }} 공식 예고편
          </h5>
          <!-- 닫기 버튼 -->
          <button
            type="button" 
            class="btn-close custom-close-btn"
            data-bs-dismiss="modal"
            aria-label="Close"
            @click="stopVideo"
          >
            ×
          </button>
        </div>
        <div class="modal-body custom-modal-body">
          <div v-if="isLoading" class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <iframe
            v-else-if="videoData"
            class="trailer-iframe"
            :src="videoData"
            frameborder="0"
            allowfullscreen
          ></iframe>
          <div v-else>
            <p>해당 영화의 예고편을 찾을 수 없습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import axios from "axios";

const props = defineProps({
  movieTitle: String,
});

const videoData = ref("");
const isLoading = ref(false);
const modalRef = ref(null);
const youtubeKey = "AIzaSyAvDN5ECAKK-StTzlh97JIt_daHFyimQlY"; // API 키

const stopVideo = () => {
  videoData.value = ""; // 비디오 정지
};

// 트레일러 로드 함수
const fetchTrailer = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get("https://www.googleapis.com/youtube/v3/search", {
      params: {
        key: youtubeKey,
        part: "snippet",
        type: "video",
        q: `${props.movieTitle} 예고편 OR trailer`,
        maxResults: 1,
      },
    });

    const videoId = response.data.items[0]?.id?.videoId || null;
    if (videoId) {
      videoData.value = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1`;
    } else {
      videoData.value = null;
    }
  } catch (error) {
    console.error("YouTube API 호출 에러:", error);
    videoData.value = null;
  } finally {
    isLoading.value = false;
  }
};

// 포커스 관리
onMounted(() => {
  if (modalRef.value) {
    modalRef.value.addEventListener("show.bs.modal", fetchTrailer);
    modalRef.value.addEventListener("hidden.bs.modal", stopVideo);
  }
});

onBeforeUnmount(() => {
  if (modalRef.value) {
    modalRef.value.removeEventListener("show.bs.modal", fetchTrailer);
    modalRef.value.removeEventListener("hidden.bs.modal", stopVideo);
  }
});
</script>

<style scoped>
/* 모달 창 스타일 */
.custom-modal-content {
  background: linear-gradient(145deg, #1e1e1e, #2c2c2c); /* 배경색 변경 */
  border-radius: 10px;
  color: white; /* 텍스트 색상 */
  padding: 15px;
}

.custom-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

/* 닫기 버튼 스타일 */
.custom-close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 2rem; /* 닫기 버튼 크기 */
  cursor: pointer;
  transition: color 0.3s ease;
}

.custom-close-btn:hover {
  color: #fff; /* 마우스 호버 시 닫기 버튼 색상 */
}

.custom-modal-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.custom-modal-body {
  padding: 20px;
  text-align: center;
}

/* YouTube 트레일러 화면 크기 조정 */
.trailer-iframe {
  width: 100%;
  height: 550px; /* 기존보다 높이를 증가시킴 */
  display: block;
  border-radius: 8px; /* 화면 모서리를 약간 둥글게 */
  margin: 0 auto;
}

/* 로딩 스피너 */
.spinner-border {
  margin: 50px auto;
}

/* 모달 그림자 추가 */
.modal-content {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
}
</style>
