<template>
  <h1>Set Profile</h1>
  <div v-if="loading">
    <span class="loader"></span>
  </div>
  <form v-else @submit.prevent="setProfile">
    <div class="card">
      <label for="gender_cat">Gender:</label><br>
      <select id="gender_cat" name="gender_cat" v-model="gender_cat">
        <option value="F">Female</option>
        <option value="M">Male</option>
      </select>
    </div>
    <div class="card">
      <label for="age_cat">Age Category:</label><br>
      <select id="age_cat" name="age_cat" v-model="age_cat">
        <option value="Under 18">Under 18</option>
        <option value="18-24">18-24</option>
        <option value="25-34">25-34</option>
        <option value="35-44">35-44</option>
        <option value="45-49">35-44</option>
        <option value="50-55">35-44</option>
        <option value="56+">35-44</option>
      </select>
    </div>
    <div class="card">
      <input type="submit" value="Submit">
    </div>
  </form>
</template>

<script>
import {setProfile} from "../utils.js";

export default {
  emits: ["set-profile"],
  data() {
    return {
      gender_cat: "F",
      age_cat: "25-34",
      loading: false
    }
  },
  methods: {
    async setProfile() {
      this.loading = true;
      const data = {
        gender_cat: this.gender_cat,
        age_cat: this.age_cat
      }
      try {
        const userId = await setProfile(data);
        this.$emit("set-profile", userId);
      } catch (e) {
        console.log(e)
      }
      this.loading = false;

    }
  }
}
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
