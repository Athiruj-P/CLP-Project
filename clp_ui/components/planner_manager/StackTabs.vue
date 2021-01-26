<template>
  <v-card color="#E5E7EB" class="h-full" style="position: relative">
    <v-tabs v-model="tab" background-color="#E5E7EB">
      <v-tab>
        Stack list
      </v-tab>

      <v-tab>
        Stack detail
      </v-tab>
    </v-tabs>
    <v-tabs-items
      v-model="tab"
      class="overflow-y-auto px-2 pb-1"
      style="height:80%; background-color:#E5E7EB"
    >
      <v-tab-item>
        <v-checkbox
          v-model="selected_all"
          label="All stacks"
          hide-details
          value="all"
          class="mt-0"
          @click="click_all_stack"
        ></v-checkbox>

        <div v-if="$store.state.planner_manage.render_data">
          <v-item-group class="mt-1 flex flex-wrap flex-row">
            <v-checkbox
              v-for="(val, index) in $store.state.planner_manage.render_data
                .boxes_stack"
              :key="index"
              v-model="selected_stack_list"
              :label="`Stack ${index}`"
              :value="index"
              hide-details
              class="mr-2"
              @click="click_each_stack"
            ></v-checkbox>
          </v-item-group>
        </div>
      </v-tab-item>
      <v-tab-item>
        <v-checkbox
          v-model="selected_all"
          label="All stacks"
          hide-details
          value="all"
          class="mt-0"
          @click="click_all_stack"
        ></v-checkbox>

        <div v-if="$store.state.planner_manage.render_data">
          <v-item-group class="mt-1 flex flex-wrap flex-row">
            <v-checkbox
              v-for="(val, index) in $store.state.planner_manage.render_data
                .boxes_stack"
              :key="index"
              v-model="selected_stack_list"
              :label="`Stack ${index}`"
              :value="index"
              hide-details
              class="mr-2"
              @click="click_each_stack"
            ></v-checkbox>
          </v-item-group>
        </div>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>
import box from "@/mixins/box";
export default {
  mixins: [box],
  data: () => ({
    tab: 0,
    init: false,
    selected_all: [],
    selected_stack_list: []
  }),
  mounted() {},
  methods: {
    click_all_stack() {
      var tmp_arr_stack = [];
      var tmp_arr_index = [];
      if (
        this.selected_all[0] === "all" &&
        this.$store.state.planner_manage.render_data
      ) {
        this.$store.state.planner_manage.render_data.boxes_stack.forEach(
          (stack_val, index) => {
            tmp_arr_stack.push(stack_val);
            tmp_arr_index.push(index);
          }
        );
      } else {
        this.selected_all = [];
      }
      this.$store.commit(
        "planner_manage/set_selected_stack_list",
        tmp_arr_stack
      );
      this.selected_stack_list = tmp_arr_index;
    },
    click_each_stack() {
      var tmp_arr_stack = [];
      this.selected_stack_list.forEach((stack_val, index) => {
        tmp_arr_stack.push(
          this.$store.state.planner_manage.render_data.boxes_stack[stack_val]
        );
      });
      this.$store.commit(
        "planner_manage/set_selected_stack_list",
        tmp_arr_stack
      );
    }
  },
  watch: {
    "$store.state.planner_manage.render_data"(data) {
      //   if (!this.init) {
      //     this.init = true;
      //     this.selected_all = ["all"];
      //     this.click_all_stack();
      //   }
      this.selected_all = ["all"];
      this.click_all_stack();
    }
  }
};
</script>
