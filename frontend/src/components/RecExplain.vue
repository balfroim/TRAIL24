<template>
  <h1>Recommendation ({{ userId }})</h1>

  <div v-if="loading">
    <p>Loading...</p>
  </div>
  <div v-else>
    <div class="card">
      <p>{{ recommendation }}</p>
    </div>

    <div class="card">
      <button v-if="!explanation" @click="getExplanation">Explain</button>
      <p v-else>{{ explanation }}</p>
    </div>
  </div>
</template>

<script>
import {getExplanationApiCall, getRecommendationApiCall} from "../utils.js";

export default {
  props: ['userId'],
  data() {
    return {
      recommendation: "",
      explanation: "",
      loading: false
    }
  },
  methods: {
    async getRecommendation() {
      this.loading = true;
      this.recommendation = await getRecommendationApiCall(this.userId);
      this.loading = false;
    },
    async getExplanation() {
      this.loading = true;
      this.explanation = await getExplanationApiCall(this.userId);
      this.loading = false;
    }
  },
  mounted() {
    this.getRecommendation();
  }
}
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
