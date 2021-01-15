<template>
  <v-app>
    <v-row class="flex flex-wrap justify-center content-center">
      <v-col md="4">
        <v-card elevation="2" class="p-3">
          <v-img
            class="ml-auto mr-auto"
            max-width="200px"
            aspect-ratio="1"
            :src="require('~/assets/img/clp_logo.png')"
          ></v-img>

          <p class="text-center mt-4 text-3xl ">Welcome to CLP</p>

          <v-text-field
            class="ml-3 mr-3"
            v-model="username"
            label="Username"
            required
          >
          </v-text-field>
          <v-text-field
            class="ml-3 mr-3"
            type="password"
            v-model="password"
            label="Password"
            required
          ></v-text-field>

          <v-btn class="btn-login" block color="primary" @click="login">
            Login
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar
      class="pt-4"
      v-model="show_alert"
      :timeout="timeout"
      absolute
      right
      shaped
      top
      :color="color_alert"
    >
      <v-icon>{{ icon_alert }}</v-icon>
      <span class="ml-3 text-base">{{ text_alert }}</span>

      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="show_alert = false">
          <v-icon>fas fa-times</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import login from "@/mixins/login";
export default {
  layout: "login",
  data: () => ({
    username: "",
    password: "",
    result: {},
    show_alert: false,
    text_alert: "",
    color_alert: "",
    icon_alert: "",
    timeout: 2000
  }),
  mixins: [login],
  watch: {
    async result(newValue, oldValue) {
      if (newValue.status !== "success") {
        this.show_alert = true;
        this.text_alert = newValue.mes;
        this.color_alert = "red";
        this.icon_alert = "fas fa-exclamation-circle";
      } else {
        this.$store.commit("set_login", {
          status: true,
          username: this.username,
          user_id: newValue.user_id,
        });
        this.username = "";
        this.password = "";
        this.$router.push("planner");
      }
    }
  },
  methods: {}
};
</script>

<style scoped>
.v-application {
  position: relative;
  background-color: rgb(238, 235, 235);
}
</style>
