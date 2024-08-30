<template>
  <h1>Search & Rate ({{ userId }})</h1>

  <div class="card">
    <form @submit.prevent="searchProduct">
      <div>
        <label for="search_query">Search for a movie:</label><br>
        <input type="text" id="search_query" name="search_query" v-model="searchQuery">
      </div>
      <div>
        <input type="submit" value="Submit">
      </div>
    </form>
  </div>

  <div class="card">
    <form @submit.prevent="rateProduct">
      <div>
        <label for="select_product">Select a movie:</label><br>
        <select id="select_product" name="select_product" v-model="selectedPid">
          <option v-for="(name, pid) in this.searchResults" :value="pid" :key="pid">{{ name }}</option>
        </select>
      </div>
      <div>
        <label for="rating_value">Rate the selected movie:</label><br>
        <select id="rating_value" name="rating_value" v-model="ratingValue">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
      </div>
      <div>
        <input type="submit" value="Submit" :disabled="!selectedPid">
      </div>
    </form>
  </div>

  <div class="card">
    <button @click="switchToRec">Recommendation</button>
  </div>
</template>

<script>
import {addRateApiCall, searchApiCall} from "../utils.js";

export default {
  props: ['userId'],
  emits: ['switch-to-rec'],
  data() {
    return {
      searchQuery: "",
      searchResults: [],
      ratings: [],
      selectedPid: 0,
      ratingValue: 3
    }
  },
  methods: {
    async searchProduct() {
      if (this.searchQuery) {
        const data = {
          value: this.searchQuery
        }
        this.searchResults = await searchApiCall(data);
      }
    },
    async rateProduct() {
      const data = {
        product_id: this.selectedPid,
        value: this.ratingValue
      }
      await addRateApiCall(data, this.userId);
    },
    switchToRec() {
      this.$emit('switch-to-rec');
    }
  }
}
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
