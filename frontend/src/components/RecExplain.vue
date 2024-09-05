<template>
  <h1 class="title">Start watching!</h1>
  <h2 class="page-info">
    Here are some movies we recommend based on your profile.
    <span class="colored-text">You can inspect why an item was recommended
    to you by hovering over it.</span>
  </h2>
  <div v-if="loading">
    <span class="loader"></span>
  </div>
  <div v-else class="horizontal-list">
    <div v-for="product in recommended_products" class="horizontal-list-elem" :key="product.pid">
      <div class="photo-container">
        <img class="movie-poster" :src="getPosterUrl(product.pid)" :alt="product.name">
        <p>{{ product.name }}</p>
        <button type="button" class="btn" @click="showExplanation(product.pid)">
          Explain
        </button>
      </div>
    </div>
  </div>

  <Modal
    v-show="isModalVisible"
    @close="hideExplanation"
  >
    <template v-slot:header>
      {{ activeExplanationHeader }}
    </template>

    <template v-slot:body>
      <p v-for="(explanation, index) in activeExplanationContent" :key="index">
        Explanation <b>{{ index+1 }}</b><br>
        {{ explanation }}
      </p>
    </template>

    <template v-slot:footer>
      {{ "" }}
    </template>
  </Modal>
</template>

<script>
import {apiBaseUrl, getExplanationApiCall, getRecommendationsApiCall} from "../utils.js";
import Modal from "./Modal.vue";

export default {
  components: {Modal},
  props: ['userId'],
  data() {
    return {
      recommended_products: [],
      explanations: {},
      loading: false,
      isModalVisible: false,
      activeExplanationPid: undefined
    }
  },
  methods: {
    async getRecommendation() {
      this.loading = true;
      try {
        this.recommended_products = await getRecommendationsApiCall(this.userId);
        this.recommended_products.map((product) => this.explanations[product.pid] = []);
      } catch (e) {
        console.log(e);
      }
      this.loading = false;
    },
    async getExplanations(productId) {
      this.loading = true;
      try {
        this.explanations[productId] = await getExplanationApiCall(this.userId, productId);
      } catch (e) {
        console.log(e);
      }
      this.loading = false;
    },
    async showExplanation(productId) {
      if (!this.explanations[productId].length) {
        await this.getExplanations(productId);
      }
      this.activeExplanationPid = productId;
      this.isModalVisible = true;
    },
    getPosterUrl(productId) {
      return `${apiBaseUrl}/poster/${productId}`;
    },
    hideExplanation() {
      this.isModalVisible = false;
    }
  },
  computed: {
    activeExplanationContent() {
      if (this.activeExplanationPid) {
        return this.explanations[this.activeExplanationPid];
      } else {
        return "";
      }
    },
    activeExplanationHeader() {
      if (this.activeExplanationPid) {
        const productName = this.recommended_products.find((product) => product.pid === this.activeExplanationPid).name;
        return `Explanations for ${productName}`;
      } else {
        return "";
      }
    }
  },
  mounted() {
    this.getRecommendation();
  }
}
</script>
