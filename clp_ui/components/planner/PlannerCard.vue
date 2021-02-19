<template>
  <div style="width:250px; height:160px;" class="relative">
    <div class="absolute top-0 right-0 z-50 p-2">
      <EditDialog show="card" :obj_planner="planner" />
    </div>
    <v-card
      outlined
      elevation="3"
      class="cursor-pointer planner-card"
      @click="planner_manager"
    >
      <v-list-item three-line>
        <v-list-item-content>
          <v-list-item-title class="headline mb-1 flex justify-space-between">
            <v-icon>fas fa-truck-loading</v-icon>
          </v-list-item-title>
          <span class="text-sm text-gray-600 font-semibold">{{
            planner.pln_name
          }}</span>
          <br />
          <span class="text-sm text-gray-600"
            >Width : {{ planner.pln_width }} {{ planner.pln_unit }}</span
          >
          <br />
          <span class="text-sm text-gray-600"
            >Heigth : {{ planner.pln_height }} {{ planner.pln_unit }}</span
          >
          <br />
          <span class="text-sm text-gray-600"
            >Depth : {{ planner.pln_depth }} {{ planner.pln_unit }}</span
          >
          <br />
        </v-list-item-content>
      </v-list-item>
    </v-card>
  </div>
</template>

<script>
import EditDialog from "@/components/planner/EditDialog";
export default {
  props: {
    planner: {
      type: Object,
      required: true
    }
  },
  //   data: () => ({
  //     card_data: this.planner
  //   }),
  methods: {
    planner_manager() {
      this.$store.commit("planner_manage/set_selected_planner", this.planner);
      localStorage.removeItem("selected_planner");
      localStorage.setItem("selected_planner", JSON.stringify(this.planner));
      this.$router.push("planner_manager");
    }
  },
  mounted: function() {}
};
</script>
