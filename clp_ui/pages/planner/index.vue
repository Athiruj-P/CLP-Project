<template>
  <div>
    <!-- Header -->
    <v-card flat>
      <v-toolbar dense height="70px">
        <v-img
          class="mr-4"
          max-width="50px"
          aspect-ratio="1"
          :src="require('~/assets/img/clp_logo.png')"
        ></v-img>

        <v-toolbar-title class="font-semibold"
          ><span class="text-3xl text-gray-600"
            >Container Loading Planner</span
          ></v-toolbar-title
        >
        <v-spacer></v-spacer>

        <span>{{ $store.state.username }}</span>
        <v-menu bottom offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon class="hidden-xs-only" v-bind="attrs" v-on="on">
              <v-icon>fas fa-user-circle</v-icon>
            </v-btn>
          </template>

          <v-list>
            <v-list-item>
              <v-list-item-title class="cursor-pointer" @click="logout">
                <span>
                  <v-icon>fas fa-sign-out-alt</v-icon>
                </span>
                Logout
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar>
    </v-card>
    <!-- Header -->

    <v-main class="m-5">
      <v-row>
        <v-col md="3">
          <AddDialog />
        </v-col>
      </v-row>
      <v-row>
        <div
          v-if="this.$store.state.planner.planners"
          class="flex flex-wrap overflow-y-auto"
        >
          <div
            v-for="(item, index) in this.$store.state.planner.planners"
            :key="index"
            class="m-4"
          >
            <PlannerCard :planner="item" />
          </div>
        </div>
        <p v-else class="">Click + Add planner to create your plan</p>
      </v-row>
    </v-main>

    <!-- Alert -->
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
    <!-- Alert -->
  </div>
</template>

<script>
import login from "@/mixins/login";
import planner from "@/mixins/planner";
import AddDialog from "@/components/planner/AddDialog";
import PlannerCard from "@/components/planner/PlannerCard";

export default {
  mixins: [login, planner],
  async beforeMount() {
    try {
      var local_store_planners = localStorage.getItem("planners");
      if (local_store_planners) {
        this.$store.commit(
          "planner/set_planner",
          JSON.parse(local_store_planners)
        );
      } else {
        this.get_all_planner();
      }
    } catch {
      this.logout();
    }
  },
  mounted: function() {
    this.get_all_container();
    this.get_all_unit();
    var local_store_username = localStorage.getItem("username");
    if (!local_store_username) {
      this.show_alert = true;
      this.text_alert = "Login success";
      this.color_alert = "success";
      this.icon_alert = "fas fa-check-circle";
      this.username = this.$store.state.username;
      this.planners = this.$store.state.planner.planners;
    }
  },
  data: () => ({
    planners: null,
    username: "",
    show_alert: false,
    text_alert: "",
    color_alert: "",
    icon_alert: "",
    timeout: 2000
  }),
  computed: {
    change_alert() {
      return this.$store.state.counter;
    }
  },
  watch: {
    async planners(newValue, oldValue) {
      if (newValue.status === "error" || newValue.status === "system_error") {
        this.show_alert = true;
        this.text_alert = newValue.mes;
        this.color_alert = "red";
        this.icon_alert = "fas fa-exclamation-circle";
      } else {
        // this.$store.commit("planner/get_all_planner", planners);
      }
    }
  }
};
</script>
