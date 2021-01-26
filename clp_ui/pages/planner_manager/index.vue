<template>
  <v-row class="h-full w-screen flex">
    <v-col md="3" class="mx-0 my-0 pr-0">
      <v-navigation-drawer class="primary sticky" permanent width="100%">
        <div style="height:10%">
          <!-- Header -->
          <div class="px-2 py-2 flex flex-wrap items-center justify-around">
            <div class="flex items-center">
              <v-img
                max-width="65px"
                aspect-ratio="1"
                :src="require('@/assets/img/clp_logo.png')"
              ></v-img>
              <span class="text-3xl font-black text-white">CLP</span>
            </div>

            <!-- Logout btn -->
            <div>
              <v-menu bottom offset-y>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="hidden-xs-only"
                    outlined
                    color="white"
                    v-bind="attrs"
                    v-on="on"
                  >
                    {{ $store.state.username }}
                    <v-icon right>fas fa-user-circle</v-icon>
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
            </div>
            <!-- Logout btn -->
          </div>
          <!-- Header -->
        </div>
        <div style="height:73%;">
          <!-- Back BTN -->
          <div class="m-2 flex items-center">
            <NuxtLink to="/planner"
              ><v-icon color="white">fas fa-arrow-left</v-icon>
              <span class="text-white mx-2 text-xl font-bold">Back</span>
            </NuxtLink>
            <!-- <div class="cursor-pointer">
            
          </div> -->
          </div>
          <!-- Back BTN -->

          <v-divider color="white"></v-divider>

          <!-- Planner btn -->
          <div class="m-2 flex items-center justify-between">
            <div>
              <v-icon color="white">fas fa-truck-loading</v-icon>
              <span
                v-if="planner_name"
                class="text-white mx-2 text-xl font-bold"
              >
                {{ planner_name }}
              </span>
            </div>
            <div
              v-if="$store.state.planner_manage.selected_planner"
              class="text-white"
            >
              <EditDialog
                show="manage"
                :obj_planner="$store.state.planner_manage.selected_planner"
              />
            </div>
          </div>
          <!-- Planner btn -->
          <v-divider color="white"></v-divider>

          <!-- Box BTN -->
          <div class="m-2 flex items-center justify-between">
            <div>
              <v-icon color="white">fas fa-box-open</v-icon>
              <span class="text-white mx-2 text-xl font-bold">Box</span>
            </div>
            <div v-if="selected_planner" class="text-white">
              <AddBoxDialog />
            </div>
          </div>
          <!-- Box BTN -->
          <v-divider color="white"></v-divider>

          <!-- Box list -->
          <BoxList />
          <!-- Box list -->
        </div>

        <!-- Browse file and Render BTN -->
        <div style="height:17%" class="bg-gray-200">
          <div
            style="height:17%"
            class="absolute bottom-0 left-0 flex flex-col justify-center w-full"
          >
            <div class="pb-2 pt-8 px-2">
              <v-btn block elevation="2" color="indigo">
                <span class="text-white">Browse file</span>
              </v-btn>
            </div>
            <div class="pb-1 px-2">
              <v-btn
                v-if="$store.state.box.boxes.length > 0"
                block
                color="warning"
                @click="render_container"
              >
                Render
              </v-btn>
              <div v-else class="cursor-not-allowed">
                <v-btn block color="warning" :disabled="true">
                  Render
                </v-btn>
              </div>
            </div>
          </div>
        </div>
        <!-- Browse file and Render BTN -->
      </v-navigation-drawer>
    </v-col>
    <v-col md="9" class="h-full pl-3 pr-1 flex flex-col">
      <div class="h-3/4 pa-2">
        <Graph3D />
      </div>
      <div style="height:30%" class="mb-3 ">
        <StackTabs />
      </div>
    </v-col>
  </v-row>
</template>

<script>
import box from "@/mixins/box";
import login from "@/mixins/login";
import stack from "@/mixins/stack";
import EditDialog from "@/components/planner/EditDialog";
import AddBoxDialog from "@/components/planner_manager/AddBoxDialog";
import BoxList from "@/components/planner_manager/BoxList";
import Graph3D from "@/components/planner_manager/Graph3D";
import StackTabs from "@/components/planner_manager/StackTabs";
export default {
  layout: "planner_manager",
  mixins: [login, box, stack],
  async beforeMount() {
    if (process.browser) {
      var local_store_selected_planner = localStorage.getItem(
        "selected_planner"
      );
      if (local_store_selected_planner) {
        this.$store.commit(
          "planner_manage/set_selected_planner",
          JSON.parse(local_store_selected_planner)
        );
        this.selected_planner = JSON.parse(local_store_selected_planner);
        this.planner_name = this.selected_planner.pln_name;
        this.$store.commit("set_main_unit", {
          un_id: this.selected_planner.pln_unit_id,
          un_abb: this.selected_planner.pln_unit
        });
        this.render_container();
        this.get_all_box();
        this.get_box_std();
        this.get_all_color();
      } else {
        this.$router.push("planner");
      }
    }
  },
  data: () => ({
    selected_planner: null,
    planner_name: null
  }),
  methods: {},
  async destroyed() {
    localStorage.removeItem("selected_planner");
    localStorage.removeItem("boxes");
    this.$store.commit("box/set_boxes", []);
    this.$store.commit("box_dialog/clear_dialog");
    console.log("destroyed ");
  }
};
</script>
