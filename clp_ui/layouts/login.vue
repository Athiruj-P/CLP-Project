<template>
  <div class="h-full overflow-y-hidden">
    <nuxt />
  </div>
</template>
<script>
export default {
  async beforeMount() {
    try {
      var local_store_user_id = localStorage.getItem("user_id");
      var local_store_username = localStorage.getItem("username");
      if (local_store_user_id && local_store_username) {
        if (!this.$store.state.user_id) {
          this.$store.commit("set_login", {
            statue: true,
            username: local_store_username,
            user_id: local_store_user_id
          });
        }
        this.$router.push("planner");
      } else {
        this.logout();
      }
    } catch {
      this.logout();
    }
  }
};
</script>
<style scoped>
* {
  font-family: "Ubuntu";
}
</style>
