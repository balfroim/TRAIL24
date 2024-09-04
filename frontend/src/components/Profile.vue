<template>
  <h1 class="page-title">
    Welcome to <span class="colored-text"> Movielens </span>!
  </h1>
  <h2 class="page-info">Let's start by setting up your profile</h2>
  <div v-if="loading">
    <span class="loader"></span>
  </div>
  <form v-else @submit.prevent="setProfile">
    <div class="prompt-input">
      <label class="prompt" for="name">What is your name?</label><br>
      <input type="text" id="name" name="name" placeholder="Name (e.g. John Doe)" required>
    </div>
    <div class="prompt-input">
      <label class="prompt" for="gender_cat">Gender:</label><br>
      <select id="gender_cat" name="gender_cat" v-model="gender_cat" required>
        <option value="F">Female</option>
        <option value="M">Male</option>
        <option value="O">Other</option>
        <option value="P">Prefer not to specify</option>
      </select>
    </div>
    <div class="prompt-input">
      <label class="prompt" for="age_cat">Age Category:</label><br>
      <select id="age_cat" name="age_cat" v-model="age_cat" required>
        <option value="Under 18">Under 18</option>
        <option value="18-24">18-24</option>
        <option value="25-34">25-34</option>
        <option value="35-44">35-44</option>
        <option value="45-49">35-44</option>
        <option value="50-55">35-44</option>
        <option value="56+">35-44</option>
      </select>
    </div>
    <input class="continue" type="submit" value="Submit & Continue">
  </form>
</template>

<script>
import {setProfileApiCall} from "../utils.js";

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
        const userId = await setProfileApiCall(data);
        this.$emit("set-profile", userId);
      } catch (e) {
        console.log(e)
      }
      this.loading = false;

    }
  }
}
</script>
