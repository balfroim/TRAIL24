<template>
  <div>
    <Profile v-if="content==='profile'" @set-profile="setProfile" />
    <SearchRate v-if="content==='search_rate'" :user-id="userId" />
<!-- @recommend="content = 'rec_explain'" -->
    <RecExplain v-if="content==='rec_explain'"  user-id="userId" />
  </div>
</template>

<script>
import Profile from "./components/Profile.vue";
import SearchRate from "./components/SearchRate.vue";
import RecExplain from "./components/RecExplain.vue";

export default {
  components: {
    Profile,
    SearchRate,
    RecExplain
  },
  data() {
    return {
      userId: -1,
      content: "profile" // "search_rate" or "rec_explain"
    }
  },
  methods: {
    async setProfile(userId) {
      console.log('coucou ' + userId);
      console.log(this.userId);
      this.userId = userId;
      console.log(this.userId);
      this.content = "search_rate";
    }
  }
}
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
