<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">새 컬렉션 만들기</h5>
        <button class="btn-close" @click="$emit('close')">&times;</button>
      </div>
      <div class="modal-body">
        <!-- <p>새 컬렉션 이름을 입력하세요:</p> -->
        <input
          v-model="categoryName"
          class="category-input"
          placeholder="컬렉션 이름을 입력하세요."
        />
        <div class="modal-actions">
          <button class="btn btn-create" @click="createCategory">생성</button>
          <button class="btn btn-cancel" @click="$emit('close')">취소</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useCounterStore } from "@/stores/counter";

export default {
  data() {
    return {
      categoryName: "",
    };
  },
  methods: {
    async createCategory() {
      if (!this.categoryName.trim()) {
        alert("컬렉션 이름을 입력하세요.");
        return;
      }
      try {
        const store = useCounterStore();
        const { data } = await axios.post(
          `http://127.0.0.1:8000/accounts/categories/create/`,
          { name: this.categoryName },
          {
            headers: {
              Authorization: `Token ${store.token}`,
            },
          }
        );
        alert("컬렉션이 생성되었습니다.");
        this.$emit("categoryCreated", data); // 생성된 컬렉션를 부모 컴포넌트로 전달
        this.$emit("close"); // 모달 닫기
      } catch (error) {
        console.error("Error creating category:", error);
        alert("컬렉션 생성에 실패했습니다.");
      }
    },
  },
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
  width: 400px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4),
              0 4px 8px rgba(0, 0, 0, 0.2);
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
  font-size: 1.4rem;
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

/* 입력 필드 */
.category-input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #444;
  background: #1f1f1f;
  color: white;
  margin-bottom: 10px;
}
.category-input::placeholder {
  color: #666;
}

/* 모달 하단 버튼 */
.modal-actions {
  display: flex;
  justify-content: space-between;
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
