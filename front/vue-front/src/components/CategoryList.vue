<template>
  <div>
    <h2>컬렉션 관리</h2>
    <form @submit.prevent="createCategory">
      <input v-model="newCategoryName" placeholder="새 컬렉션 이름" />
      <button type="submit">컬렉션 생성</button>
    </form>
    <ul>
      <li v-for="category in categories" :key="category.id">
        <router-link :to="`/categories/${category.id}`">{{ category.name }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import { useCounterStore } from '@/stores/counter';

export default {
  data() {
    return {
      newCategoryName: '',
    };
  },
  computed: {
    categories() {
      return useCounterStore().categories;
    },
  },
  methods: {
    async createCategory() {
      const store = useCounterStore();
      await store.createCategory(this.newCategoryName);
      this.newCategoryName = '';
    },
  },
  mounted() {
    useCounterStore().fetchCategories();
  },
};
</script>
