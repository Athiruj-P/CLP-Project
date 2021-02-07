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
      <!-- Stack list tab -->
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
              class="mr-2 w-1/6"
              @click="click_each_stack"
            ></v-checkbox>
          </v-item-group>
        </div>
      </v-tab-item>
      <!-- Stack list tab -->

      <!-- Stack detail tab -->
      <v-tab-item>
        <v-menu top :offset-y="true" v-model="menu_open">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              small
              color="primary"
              dark
              v-bind="attrs"
              v-on="on"
              class="mt-1 ml-1"
            >
              {{ menu_title }}
              <v-icon v-if="menu_open" right dark>
                fas fa-angle-up
              </v-icon>
              <v-icon v-else right dark>
                fas fa-angle-down
              </v-icon>
            </v-btn>
          </template>

          <v-list
            v-if="$store.state.planner_manage.render_data"
            height="auto"
            max-height="300px"
            class="overflow-y-auto"
          >
            <v-list-item @click="click_menu('0000')">
              <v-list-item-title>--Select stack--</v-list-item-title>
            </v-list-item>
            <v-list-item
              v-for="(val, index) in $store.state.planner_manage.render_data
                .boxes_stack"
              :key="index"
              link
              @click="click_menu(val, index)"
            >
              <v-list-item-title>{{ `Stack ${index}` }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <v-container>
          <v-list dense style="height:70%; background-color:#E5E7EB">
            <!-- <v-list-item-group v-model="selected_container" color="primary"> -->
            <!-- <v-list-item-group color="primary" class="overflow-y-auto" > -->
            <v-list-item
              v-for="(item, index) in selected_menu"
              :key="index"
              class="mb-2"
            >
              <v-list-item-icon>
                <v-icon large :color="`#${item.box_color}`"
                  >fas fa-dice-d6</v-icon
                >
              </v-list-item-icon>
              <v-list-item-content class="overflow-y-auto">
                <v-list-item-title class="flex justify-between">
                  <span class="text-base w-1/5">Name: {{ item.box_name }}</span>
                  <span class="text-base w-1/5"
                    >Quantity: {{ item.box_fitted_qty }}</span
                  >
                  <span class="text-base w-1/5">
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
                      )} ${
                        $store.state.planner_manage.selected_planner.pln_unit
                      }`
                    }}
                  </span>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <!-- </v-list-item-group> -->
          </v-list>
        </v-container>
      </v-tab-item>
      <!-- Stack detail tab -->
    </v-tabs-items>
  </v-card>
</template>

<script>
import box from "@/mixins/box";
export default {
  mixins: [box],
  data: () => ({
    tab: 0,
    menu_open: null,
    selected_menu: null,
    menu_title: "Select stack",
    init: false,
    selected_all: [],
    selected_stack_list: []
  }),
  mounted() {
    console.log(this.$store.state.planner_manage.render_data);
  },
  methods: {
    // Stack list
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
    },
    // Stack list

    // Stack detail
    click_menu(select, index) {
      if (select === "0000") {
        this.menu_title = "Select stack";
        this.selected_menu = null;
      } else {
        this.menu_title = `Stack ${index}`;
        var tmp_box_arr = [];

        select.forEach(val => {
          let tmp_obj = JSON.parse(JSON.stringify(val.box_detail));
          let tmp_name = tmp_obj.box_name;
          tmp_obj.box_name = tmp_name.substr(0, tmp_name.lastIndexOf("-"));
          tmp_box_arr.push(tmp_obj);
        });

        const filtered_arr = [
          ...new Map(tmp_box_arr.map(item => [item.box_id, item])).values()
        ];

        let tmp_num = 0;

        filtered_arr.forEach((filtered_val, index) => {
          tmp_num = 0;
          tmp_box_arr.forEach(tmp_val => {
            if (tmp_val.box_id === filtered_val.box_id) {
              ++tmp_num;
            }
          });
          filtered_arr[index].box_fitted_qty = tmp_num;
        });

        this.selected_menu = filtered_arr;
      }
    }

    // Stack detail
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
    // selected_menu(newVal) {
    //   console.log(newVal);
    // }
  }
};
</script>
