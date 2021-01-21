<template>
  <div class="h-full">
    <v-col md="3" class="h-full px-0 py-0">
      <v-navigation-drawer class="primary" permanent width="100%">
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
            <span v-if="planner_name" class="text-white mx-2 text-xl font-bold">
              {{ planner_name }}
            </span>
          </div>
          <div v-if="selected_planner" class="text-white">
            <EditDialog show="manage" :obj_planner="selected_planner" />
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

        <!-- Browse file and Render BTN -->
        <template v-slot:append>
          <div class="p-2">
            <v-btn block>
              Browse file
            </v-btn>
          </div>
          <div class="p-2">
            <v-btn block color="warning">
              Render
            </v-btn>
          </div>
        </template>
        <!-- Browse file and Render BTN -->
      </v-navigation-drawer>
    </v-col>
  </div>
</template>

<script>
import box from "@/mixins/box";
import login from "@/mixins/login";
import EditDialog from "@/components/planner/EditDialog";
import AddBoxDialog from "@/components/planner_manager/AddBoxDialog";
import BoxList from "@/components/planner_manager/BoxList";
export default {
  mixins: [login, box],
  async beforeMount() {
    var local_store_selected_planner = localStorage.getItem("selected_planner");
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
      this.get_all_box();
      this.get_box_std();
      this.get_all_color();
    } else {
      this.$router.push("planner");
    }
  },
  data: () => ({
    selected_planner: null,
    planner_name: null
  }),
  async destroyed() {
    localStorage.removeItem("selected_planner");
    localStorage.removeItem("boxes");
    this.$store.commit("box/set_boxes", []);
    this.$store.commit("box_dialog/clear_dialog");
    console.log("destroyed ");
  }
};
</script>
