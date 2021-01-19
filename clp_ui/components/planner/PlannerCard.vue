<template>
  <v-card
    width="250"
    height="160"
    outlined
    elevation="3"
    class="cursor-pointer"
  >
    <v-list-item three-line>
      <v-list-item-content>
        <v-list-item-title class="headline mb-1 flex justify-space-between">
          <v-icon>fas fa-truck-loading</v-icon>
          <EditDialog show="card" :obj_planner="planner" />
          <!-- {{card_data}} -->
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
  methods: {},
  mounted: function() {}
};
</script>
