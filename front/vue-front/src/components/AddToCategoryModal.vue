<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">컬렉션 선택</h5>
        <button class="btn-close" @click="$emit('close')">&times;</button>
      </div>
      <div class="modal-body">
        <!-- 컬렉션 리스트 -->
        <ul class="category-list">
          <li
            v-for="category in categories"
            :key="category.id"
            class="category-item"
          >
            {{ category.name }}
            <button
              class="btn btn-add"
              @click="addMovieToCategory(category.id)"
            >
              추가
            </button>
          </li>
        </ul>

        <!-- 새 컬렉션 생성 -->
        <div class="new-category">
          <input
            v-model="newCategoryName"
            placeholder="새 컬렉션 이름을 입력하세요."
            class="category-input"
          />
          <button class="btn btn-create" @click="createCategory">
            컬렉션 생성
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axiosInstance from "@/axios";
import {useCounterStore} from "@/stores/counter.js"

export default {
  props: {
    movieId: Number, // 영화 ID
  },
  setup(props) {
    const categories = ref([]); // 컬렉션 목록
    const newCategoryName = ref(""); // 새 컬렉션 이름
    const store = useCounterStore()
    // 컬렉션 목록 가져오기
    const fetchCategories = async () => {
      try {
        const response = await axiosInstance.get(
          "http://127.0.0.1:8000/accounts/categories/", {
            headers: {
              Authorization: `Token ${store.token}`,
            },
          }
        );
        categories.value = response.data;
      } catch (error) {
        console.error("Error fetching categories:", error);
        alert("컬렉션을 불러오는 데 실패했습니다.");
      }
    };

    // 새 컬렉션 생성
    const createCategory = async () => {
      if (!newCategoryName.value.trim()) {
        alert("컬렉션 이름을 입력해주세요.");
        return;
      }
      try {
        const response = await axiosInstance.post(
          "http://127.0.0.1:8000/accounts/categories/create/",
          { name: newCategoryName.value },
          {
            headers: {
              Authorization: `Token ${store.token}`,
            },
          }
        );
        categories.value.push(response.data);
        newCategoryName.value = ""; // 입력 필드 초기화
        alert("컬렉션이 생성되었습니다.");
      } catch (error) {
        console.error("Error creating category:", error.response || error.message);
        alert(
          "컬렉션을 생성하는 데 실패했습니다: " +
            (error.response?.data?.detail || "알 수 없는 오류")
        );
      }
    };

    // 영화를 컬렉션에 추가
    const addMovieToCategory = async (categoryId) => {
      try {
        await axiosInstance.post(
          "http://127.0.0.1:8000/accounts/categories/add-movie/",
          {
            category_id: categoryId,
            movie_id: props.movieId,
          },
          {
            headers: {
              Authorization: `Token ${store.token}`,
            },
          }
        );
        alert("영화가 컬렉션에 추가되었습니다.");
      } catch (error) {
        console.error("Error adding movie to category:", error);
        alert("영화를 추가하는 데 실패했습니다.");
      }
    };

    // 컴포넌트가 마운트되면 컬렉션 목록 가져오기
    onMounted(fetchCategories);

    return {
      categories,
      newCategoryName,
      fetchCategories,
      createCategory,
      addMovieToCategory,
    };
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

/* 컬렉션 리스트 */
.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  margin-bottom: 10px;
  background: #292929;
  border-radius: 8px;
  color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.category-item:hover {
  background: #353535;
  transform: translateY(-2px);
  transition: all 0.3s ease;
}

/* 추가 버튼 */
.btn-add {
  background: #39ffe585;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}
.btn-add:hover {
  background: #39ffe5c2;
}

/* 새 컬렉션 생성 섹션 */
.new-category {
  margin-top: 20px;
}

.category-input {
  /* width: calc(100% - 100px); */
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

/* 생성 버튼 */
.btn-create {
  background: #39ffe585;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.btn-create:hover {
  background: #39ffe5c2;
}
</style>
