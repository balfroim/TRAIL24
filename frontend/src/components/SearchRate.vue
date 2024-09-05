<template>
  <h1 class="page-title">Almost there...</h1>
  <p class="page-info">
    To personalize your experience with Movielens, we would like to
    know your favorite movies. <br><span class="colored-text">Please provide the titles
    of 3 of your favourite movies</span> (the order does not matter).
  </p>
  <div v-if="loading">
    <span class="loader"></span>
  </div>
  <div v-else>
    <div>
      <h2>
        Current Favorites
        <button class="continue" @click="switchToRec" :disabled="ratings.length === 0">Go to Recommendations</button>
      </h2>
      <p v-if="ratings.length">
        <ul>
          <li v-for="rating in ratings" :key="rating.productId">
            {{ rating.productName }} ({{ rating.value }})
            <button class="search" @click="deleteRating(rating.productId)">X</button>
          </li>
        </ul>
      </p>
      <p v-else>No Favorite</p>

    </div>

    <div>
      <h2>Look for a movie (2000 or older)</h2>
      <form @submit.prevent="randomProduct">
        <label for="search_query">Generate Random:</label>
        <input class="search" type="submit" value="Random">
      </form>
      <form @submit.prevent="searchProduct">
        <label for="search_query">Search for a Title:</label>
        <input class="search-input" type="text" id="search_query" name="search_query" placeholder="Movie Title (e.g. Godfather)" v-model="searchQuery">
        <input class="search" type="submit" value="Search">
      </form>
    </div>

    <div>
      <h2>Like the movie</h2>
      <div v-if="isSearchResults" class="horizontal-list">
        <div v-for="(name, pid) in searchResults" class="horizontal-list-elem" :key="pid">
          <img class="movie-poster" :src="getPosterUrl(pid)" :alt="name">
          <p>{{ name }}</p>
          <button type="button" class="btn" @click="addRating(pid)">
            Add to Favorites!
          </button>
        </div>
      </div>
      <p v-else>No Result</p>
    </div>
  </div>
</template>

<script>
import {addRateApiCall, apiBaseUrl, deleteRateApiCall, randomApiCall, searchApiCall} from "../utils.js";

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
    async randomProduct() {
      this.loading = true;
      try {
        this.searchResults = await randomApiCall();
      } catch (e) {
        console.log(e);
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

<style scoped>
form {
  margin-bottom: 10px;
}
</style>