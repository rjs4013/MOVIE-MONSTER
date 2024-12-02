<template>
  <div>
    <h2>컬렉션 생성</h2>
    <form @submit.prevent="createCategory">
      <input
        v-model="categoryName"
        placeholder="컬렉션 이름을 입력하세요"
        class="form-control"
      />
      <button type="submit" class="btn btn-primary mt-2">컬렉션 생성</button>
    </form>
    <p v-if="message" class="mt-2">{{ message }}</p>
  </div>
</template>

<script>
import { ref } from "vue";
import axiosInstance from "@/axios";
import {useCounterStore} from "@/stores/counter.js"

export default {
  setup() {
    const categoryName = ref(""); // 입력된 컬렉션 이름
    const message = ref(""); // 사용자 메시지

    const createCategory = async () => {
      try {
        const response = await axiosInstance.post("http://127.0.0.1:8000/accounts/categories/",{
            headers: {
              Authorization: `Token ${store.token}`,
            },
          }, {
          name: categoryName.value,
        });
        message.value = `컬렉션 "${response.data.name}"가 생성되었습니다.`;
        categoryName.value = ""; // 입력 필드 초기화
      } catch (error) {
        if (error.response && error.response.data) {
          message.value =
            error.response.data.error || "컬렉션 생성에 실패했습니다.";
        } else {
          message.value = "서버와의 연결에 문제가 발생했습니다.";
        }
      }
    };

    return {
      categoryName,
      message,
      createCategory,
    };
  },
};
</script>

<style scoped>
form {
  max-width: 400px;
  margin: 0 auto;
}
</style>
