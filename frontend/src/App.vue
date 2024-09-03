<template>
  <div class="page-content">
    <Profile v-if="content==='profile'" @set-profile="setProfile" />
    <SearchRate v-if="content==='search_rate'" :user-id="userId" @switch-to-rec="switchToRec"/>
<!-- @recommend="content = 'rec_explain'" -->
    <RecExplain v-if="content==='rec_explain'"  :user-id="userId" />
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
      this.userId = userId;
      console.log(this.userId);
      this.content = "search_rate";
    },
    switchToRec() {
      this.content = "rec_explain";
    }
  }
}
</script>

<!--<style scoped>-->
<!--.profile {-->
<!--  background-image: url("../public/background.jpg");-->
<!--  background-size: 100%;-->
<!--}-->

<!--.search_rate {-->
<!--  background-image: url("../public/background-2.jpg");-->
<!--  background-size: 100%;-->
<!--}-->

<!--.rec_explain {-->
<!--  background-image: url("../public/background-3.jpg");-->
<!--  background-size: 105%;-->
<!--}-->
<!--</style>-->
