<template>
  <v-app class="h-screen overflow-y-hidden overflow-x-hidden">
    <nuxt />
    <Alert />
  </v-app>
</template>
<script>
import Alert from "@/components/Alert";
import login from "@/mixins/login";
export default {
  head: {
    titleTemplate: "CLP app"
  },
  mixins: [login],
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
.v-application {
  position: relative;
  background-color: rgb(238, 235, 235);
}
</style>
