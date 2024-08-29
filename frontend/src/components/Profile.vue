<template>
  <h1>Set Profile</h1>
  <form @submit.prevent="setProfile">
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
export default {
  emits: ["set-profile"],
  data() {
    return {
      gender_cat: "F",
      age_cat: "25-34"
    }
  },
  methods: {
    async setProfile() {
      const myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");
      const url = "http://127.0.0.1:8000/set_profile";
      const data = {
        gender_cat: this.gender_cat,
        age_cat: this.age_cat
      }
      const options = {
        method: "POST",
        body: JSON.stringify(data),
        headers: myHeaders,
      }
      const response = await fetch(url, options);
      const userId = await response.json();

      this.$emit("set-profile", userId);
    }
  }
}
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
