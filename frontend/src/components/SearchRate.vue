<template>
  <h1 class="page-title">Almost there...</h1>
  <p class="page-info">
    To personalize your experience with Movielens, we would like to
    know your favorite movies. <br><span class="colored-text">Please provide the titles
    of 5 of your favourite movies</span> (the order does not matter).
  </p>
  <div v-if="loading">
    <span class="loader"></span>
  </div>
  <div v-else>
    <div>
      <h2>Current Ratings</h2>
      <p v-if="ratings.length">
        <ul>
          <li v-for="rating in ratings" :key="rating.productId">
            {{ rating.productName }} ({{ rating.value }})
            <button @click="deleteRating(rating.productId)">X</button>
          </li>
        </ul>
      </p>
      <p v-else>No Rating</p>
    </div>

    <div>
      <h2>Search for a movie</h2>
      <form @submit.prevent="searchProduct">
          <label for="search_query">Search:</label>
          <input class="search-input" type="text" id="search_query" name="search_query" placeholder="Movie Title (e.g. The Godfather)" v-model="searchQuery">
          <input class="search" type="submit" value="Submit">
      </form>
    </div>

    <div>
      <h2>Like the movie</h2>
      <form @submit.prevent="rateProduct">
        <div>
          <label for="select_product">Select:</label><br>
          <span v-for="(name, pid) in this.searchResults" :key="pid">
            <input type="radio" :id="`product${pid}`" name="product" :value="pid" v-model="selectedPid">
            <label for="`product${pid}`">{{ name }}</label><br>
          </span>
        </div>
        <div>
          <input type="submit" value="Like!" :disabled="!selectedPid">
        </div>
      </form>
    </div>

    <button class="continue" @click="switchToRec" :disabled="ratings.length === 0">Recommendation</button>
  </div>
</template>

<script>
import {addRateApiCall, deleteRateApiCall, searchApiCall} from "../utils.js";

export default {
  props: ['userId'],
  emits: ['switch-to-rec'],
  data() {
    return {
      searchQuery: "",
      searchResults: {},
      ratings: [],
      selectedPid: 0,
      ratingValue: 5,
      loading: false
    }
  },
  methods: {
    async searchProduct() {
      this.loading = true;
      if (this.searchQuery) {
        const data = {
          value: this.searchQuery
        }
        try {
          this.searchResults = await searchApiCall(data);
        } catch (e) {
          console.log(e);
        }
      }
      this.loading = false;
    },
    async rateProduct() {
      this.loading = true;
      this.ratings.push({
        productId: this.selectedPid,
        productName: this.searchResults[this.selectedPid],
        value: this.ratingValue
      });
      const ratingData = {
        product_id: this.selectedPid,
        value: this.ratingValue
      };
      try {
        await addRateApiCall(ratingData, this.userId);
      } catch (e) {
        console.log(e);
      }
      this.loading = false;
    },
    async deleteRating(productId) {
      this.loading = true;
      const ratingIndex = this.ratings.findIndex((rating) => rating.productId === productId);
      this.ratings.splice(ratingIndex, 1);
      try {
        await deleteRateApiCall(this.userId, productId);
      } catch (e) {
        console.log(e);
      }
      this.loading = false;
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
