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
      const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        const url = `http://127.0.0.1:8000/rec/${this.userId}`;
        const options = {
          method: "GET",
          headers: myHeaders,
        }
        const response = await fetch(url, options);
        this.recommendation = await response.json();
    },
    async getExplanation() {
      const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        const url = `http://127.0.0.1:8000/explain/${this.userId}`;
        const options = {
          method: "GET",
          headers: myHeaders,
        }
        const response = await fetch(url, options);
        this.explanation = await response.json();
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
