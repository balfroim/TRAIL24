<template>
  <h1>Recommendation ({{ userId }})</h1>

  <div class="card">
    <p>{{ recommendation }}</p>
  </div>

  <div class="card">
    <button v-if="!explanation" @click="getExplanation">Explain</button>
    <p v-else>{{ explanation }}</p>
  </div>
</template>

<script>
import {getExplanationApiCall, getRecommendationApiCall} from "../utils.js";

export default {
  props: ['userId'],
  data() {
    return {
      recommendation: "",
      explanation: ""
    }
  },
  methods: {
    async getRecommendation() {
      this.recommendation = await getRecommendationApiCall(this.userId);
    },
    async getExplanation() {
      this.explanation = await getExplanationApiCall(this.userId);
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
