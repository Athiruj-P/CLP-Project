<template>
  <div dense class="bg-gray-200 overflow-y-auto overflow-x-hidden h-96">
    <div class="" v-for="(item, index) in $store.state.box.boxes" :key="index">
      <v-card class="h-20" color="#E5E7EB" tile outlined>
        <v-row class="h-full w-full pa-1 ma-0">
          <v-col md="2" class="flex justify-center pl-0 pr-0">
            <v-icon large :color="`#${item.box_color}`">fas fa-dice-d6</v-icon>
          </v-col>
          <v-col md="8" class="flex flex-col justify-start pa-0">
            <div class="text-gray-600 font-black">{{ item.box_name }}</div>
            <div class="text-sm text-gray-600 flex justify-between">
                <span>Size: {{`${item.box_width} x ${item.box_height} x ${item.box_depth} ${item.box_unit}`}}</span>
                <span>Qty: {{ item.box_quantity }}</span>
            </div>
            <div class="text-sm text-gray-600 flex justify-between">
                <span>Loaded: X</span>
                <span>Unloaded: X</span>
            </div>
          </v-col>
          <v-col md="2" class="flex justify-center pl-4 pr-0">
            <EditBoxDialog />
          </v-col>
        </v-row>
      </v-card>
    </div>
    <v-divider color="white"></v-divider>
  </div>
</template>

<script>
import EditBoxDialog from "@/components/planner_manager/EditBoxDialog";
export default {};
</script>
