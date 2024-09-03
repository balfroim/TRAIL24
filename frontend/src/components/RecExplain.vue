<template>
  <h1>Recommendation ({{ userId }})</h1>

  <div v-if="loading">
    <span class="loader"></span>
  </div>
  <div v-else>
    <div v-for="product in recommended_products" class="card" :key="product.pid">
      <p>{{ product.name }}</p>
      <button v-if="!explanations[product.pid]" @click="getExplanation(product.pid)">Explain</button>
      <p v-else>{{ explanations[product.pid] }}</p>
    </div>
  </div>
</template>

<script>
import {getExplanationApiCall, getRecommendationsApiCall} from "../utils.js";

export default {
  props: ['userId'],
  data() {
    return {
      recommended_products: [],
      explanations: {},
      loading: false
    }
  },
  methods: {
    async getRecommendation() {
      this.loading = true;
      try {
        this.recommended_products = await getRecommendationsApiCall(this.userId);
        this.recommended_products.map((product) => this.explanations[product.pid] = "");
      } catch (e) {
        console.log(e);
      }
      this.loading = false;
    },
    async getExplanation(productId) {
      this.loading = true;
      try {
        this.explanations[productId] = await getExplanationApiCall(this.userId, productId);
      } catch (e) {
        console.log(e);
      }
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
