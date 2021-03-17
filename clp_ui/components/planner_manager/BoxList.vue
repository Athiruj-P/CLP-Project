<template>
  <div
    dense
    class="bg-gray-200 overflow-y-auto overflow-x-hidden"
    style="height:56.5vh"
  >
    <div v-for="(item, index) in $store.state.box.boxes" :key="index">
      <v-card class="h-20" color="#E5E7EB" tile>
        <v-row
          v-if="$store.state.box.boxes.length > 0"
          class="h-full w-full pa-1 ma-0"
        >
          <v-col md="2" class="flex justify-center pl-0 pr-0">
            <v-icon large :color="`#${item.box_color}`">fas fa-dice-d6</v-icon>
          </v-col>
          <v-col md="8" class="flex flex-col justify-start pa-0">
            <div class="text-gray-600 font-black">{{ item.box_name }}</div>
            <div class="text-sm text-gray-600 flex justify-between">
              <span>
                Size:
                <!-- W x H x D:  -->
                {{
                  `${unit_convert(
                    item.box_width,
                    item.box_unit,
                    $store.state.planner_manage.selected_planner.pln_unit
                  )} x ${unit_convert(
                    item.box_height,
                    item.box_unit,
                    $store.state.planner_manage.selected_planner.pln_unit
                  )} x ${unit_convert(
                    item.box_depth,
                    item.box_unit,
                    $store.state.planner_manage.selected_planner.pln_unit
                  )} ${$store.state.planner_manage.selected_planner.pln_unit}`
                }}
              </span>
            </div>
            <div class="text-sm text-gray-600 flex justify-between">
              <span>Qty: {{ item.box_quantity }}</span>
              <span v-if="$store.state.planner_manage.render_data"
                >Loaded:
                <span
                  v-if="!$store.state.planner_manage.is_box_list_change"
                  class="text-green-600"
                  >{{ cal_loaded(item) }}</span
                >
                <span v-else class="text-green-600">0</span>
              </span>
              <span v-if="$store.state.planner_manage.render_data"
                >Unloaded:
                <span
                  v-if="!$store.state.planner_manage.is_box_list_change"
                  class="text-red-600"
                  >{{ cal_unloaded(item) }}</span
                >
                <span v-else class="text-red-600">0</span>
              </span>
            </div>
          </v-col>
          <v-col md="2" class="flex justify-center items-center my-0 pl-4 pr-0">
            <EditBoxDialog :obj_box="item" />
          </v-col>
        </v-row>
      </v-card>
      <v-divider color="white" class="mt-0.5"></v-divider>
    </div>
    <div
      v-if="$store.state.box.boxes.length === 0"
      class="h-full flex justify-center items-center"
    >
      <span class="text-gray-600  font-semibold"
        >Click <v-icon dense class="mx-1">fas fa-plus</v-icon> to add new
        boxes</span
      >
    </div>
  </div>
</template>

<script>
import EditBoxDialog from "@/components/planner_manager/EditBoxDialog";
import box from "@/mixins/box";
export default {
  mixins: [box],
  data: () => ({}),
  methods: {
    cal_loaded(box) {
      if (!this.$store.state.planner_manage.set_is_box_list_change) {
        var number = box.box_quantity;
        const unfit_boxes = this.$store.state.planner_manage.render_data
          .container_detail.unfit_boxes;
        unfit_boxes.forEach((obj, index) => {
          if (obj.box_name === box.box_name) {
            number = number - obj.box_unfitted;
          }
        });
        return number;
      } else {
        return 0;
      }
    },
    cal_unloaded(box) {
      var number = 0;
      if (!this.$store.state.planner_manage.set_is_box_list_change) {
        const unfit_boxes = this.$store.state.planner_manage.render_data
          .container_detail.unfit_boxes;
        unfit_boxes.forEach((obj, index) => {
          if (obj.box_name === box.box_name) {
            number = obj.box_unfitted;
          }
          return number;
        });
      }
      return number;
    }
  },
  watch: {}
};
</script>
