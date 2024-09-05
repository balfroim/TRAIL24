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
      <button class="continue" @click="switchToRec" :disabled="ratings.length === 0">Get Recommendations</button>
    </div>

    <div>
      <h2>Search for a movie</h2>
      <form @submit.prevent="searchProduct">
          <label for="search_query">Search:</label>
          <input class="search-input" type="text" id="search_query" name="search_query" placeholder="Movie Title (e.g. Godfather)" v-model="searchQuery">
          <input class="search" type="submit" value="Submit">
      </form>
    </div>

    <div>
      <h2>Like the movie</h2>
      <div v-if="isSearchResults" class="horizontal-list">
        <div v-for="(name, pid) in searchResults" class="horizontal-list-elem" :key="pid">
          <img class="movie-poster" :src="getPosterUrl(pid)" :alt="name">
          <p>{{ name }}</p>
          <button type="button" class="btn" @click="addRating(pid)">
            Like!
          </button>
        </div>
      </div>
      <p v-else>No Result</p>
    </div>
  </div>
</template>

<script>
import {addRateApiCall, apiBaseUrl, deleteRateApiCall, searchApiCall} from "../utils.js";

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
  computed: {
    isSearchResults() {
      return Object.keys(this.searchResults).length;
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
    async addRating(productId) {
      this.loading = true;
      if (!this.ratings.some((rating) => rating.productId === productId)) {
        this.ratings.push({
          productId: productId,
          productName: this.searchResults[productId],
          value: this.ratingValue
        });
        const ratingData = {
          product_id: productId,
          value: this.ratingValue
        };
        try {
          await addRateApiCall(ratingData, this.userId);
        } catch (e) {
          console.log(e);
        }
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
    getPosterUrl(productId) {
      return `${apiBaseUrl}/poster/${productId}`;
      // const isPosterAvailable = await getPosterApiCall(productId);
      // if (isPosterAvailable) {
      //   return `http://localhost:8000/poster/${productId}`;
      // } else {
      //   return "../../public/sample-poster-1x.jpeg";
      // }
    },
    switchToRec() {
      this.$emit('switch-to-rec');
    }
  }
}
</script>
