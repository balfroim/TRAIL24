<template>
  <h1>Search & Rate ({{ userId }})</h1>

  <div class="card">
    <form>
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
    <form>
      <div>
        <label for="select_product">Select a movie:</label><br>
        <select id="select_product" name="select_product" v-model="selectedProduct">
          <option value="product_id">Product Name</option>
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
        <input type="submit" value="Submit">
      </div>
    </form>
  </div>
</template>

<script>
export default {
  props: ['userId'],
  data() {
    return {
      searchQuery: "",
      ratings: [],
      selectedProduct: {},
      ratingValue: 3
    }
  },
  methods: {

  }
}
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
