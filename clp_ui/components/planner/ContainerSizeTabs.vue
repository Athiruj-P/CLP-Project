<template>
  <v-card>
    <!-- <v-card-title class="text-center justify-center py-2">
      <span class="text-base font-normal">Size</span>
    </v-card-title> -->

    <v-tabs v-model="tab" background-color="transparent" grow>
      <v-tab>Container</v-tab>
      <v-tab>Custom</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-card flat>
          <v-card-text>
            <v-list dense class="overflow-y-auto h-40">
              <v-list-item-group v-model="selected_container" color="primary">
                <v-list-item
                  v-for="(item, index) in $store.state.planner.std_containers"
                  :key="index"
                >
                  <v-list-item-icon>
                    <v-icon>fab fa-codepen</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <!-- <v-list-item-title v-text="item.con_std_name"></v-list-item-title> -->
                    <div class="flex  justify-between">
                      <span>{{ item.con_std_name }}</span>
                      <span>
                        <!-- W x H x D:  -->
                        {{
                          `${unit_convert(
                            item.con_std_width,
                            item.con_std_unit,
                            $store.state.main_unit.un_abb
                          )} x ${unit_convert(
                            item.con_std_height,
                            item.con_std_unit,
                            $store.state.main_unit.un_abb
                          )} x ${unit_convert(
                            item.con_std_depth,
                            item.con_std_unit,
                            $store.state.main_unit.un_abb
                          )} ${$store.state.main_unit.un_abb}`
                        }}
                      </span>
                    </div>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card-text>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-text>
            <!-- Container width -->
            <v-row>
              <v-col md="4" class="pb-0">
                <v-row class="my-2 mx-0 flex justify-center">
                  <span class="text-base font-normal text-black">Width</span>
                </v-row>
                <v-row class="my-2">
                  <v-text-field
                    type="number"
                    dense
                    outlined
                    v-model="width"
                    label="Width"
                    class="px-1"
                  ></v-text-field>
                </v-row>
              </v-col>
              <!-- Container width -->
              <!-- Container height -->
              <v-col md="4" class="pb-0">
                <v-row class="my-2 mx-0 flex justify-center">
                  <span class="text-base font-normal text-black">Height</span>
                </v-row>
                <v-row class="my-2">
                  <v-text-field
                    type="number"
                    dense
                    outlined
                    v-model="height"
                    label="Height"
                    class="px-1"
                  ></v-text-field>
                </v-row>
              </v-col>
              <!-- Container height -->
              <!-- Container depth -->
              <v-col md="4" class="pb-0">
                <v-row class="my-2 mx-0 flex justify-center">
                  <span class="text-base font-normal text-black">Depth</span>
                </v-row>
                <v-row class="my-2">
                  <v-text-field
                    type="number"
                    dense
                    outlined
                    v-model="depth"
                    label="Depth"
                    class="px-1"
                  ></v-text-field>
                </v-row>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="pt-0">
                <span class="text-xs text-red-500">{{ err_msg.length }}</span>
              </v-col>
            </v-row>
            <!-- Container height -->
          </v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>
import planner from "@/mixins/planner";
import conversions from "conversions";
export default {
  mixins: [planner],
  props: {
    show: {
      type: Boolean,
      required: true
    },
    is_edit: {
      type: Boolean,
      required: false
    },
    unit: {
      type: String,
      required: false
    }
  },
  data: () => ({
    tab: 0,
    width: 0,
    height: 0,
    depth: 0,
    selected_container: null,
    err_msg: {
      length: ""
    }
  }),
  methods: {
    unit_convert(number, old_unit, new_unit) {
      if (old_unit !== new_unit)
        return conversions(number, old_unit, new_unit).toFixed(2);
      else return number;
    },
    change_width() {
      let status = JSON.parse(
        JSON.stringify(this.$store.state.planner_dialog.validation_status)
      );
      status.width = false;
      if (this.length_validate(this.width)) {
        status.width = true;
        this.$store.commit("planner_dialog/set_width", Number(this.width));
      }
      this.$store.commit("planner_dialog/set_validation_status", status);
      this.check_btn_active();
    },
    change_height() {
      let status = JSON.parse(
        JSON.stringify(this.$store.state.planner_dialog.validation_status)
      );
      status.height = false;
      if (this.length_validate(this.height)) {
        status.height = true;
        this.$store.commit("planner_dialog/set_height", Number(this.height));
      }
      this.$store.commit("planner_dialog/set_validation_status", status);
      this.check_btn_active();
    },
    change_depth() {
      let status = JSON.parse(
        JSON.stringify(this.$store.state.planner_dialog.validation_status)
      );
      status.depth = false;
      if (this.length_validate(this.depth)) {
        status.depth = true;
        this.$store.commit("planner_dialog/set_depth", Number(this.depth));
      }
      this.$store.commit("planner_dialog/set_validation_status", status);
      this.check_btn_active();
    }
  },
  watch: {
    async tab(newValue, oldValue) {
      // this.selected_container = null;
    },
    async width(newValue, oldValue) {
      this.change_width();
    },
    async height(newValue, oldValue) {
      this.change_height();
    },
    async depth(newValue, oldValue) {
      this.change_depth();
    },
    async selected_container(newValue, oldValue) {
      if (Number.isInteger(newValue)) {
        let obj_con = this.$store.state.planner.std_containers[newValue];
        this.width = this.unit_convert(
          obj_con.con_std_width,
          obj_con.con_std_unit,
          this.$store.state.main_unit.un_abb
        );
        this.change_width();
        this.height = this.unit_convert(
          obj_con.con_std_height,
          obj_con.con_std_unit,
          this.$store.state.main_unit.un_abb
        );
        this.change_height();
        this.depth = this.unit_convert(
          obj_con.con_std_depth,
          obj_con.con_std_unit,
          this.$store.state.main_unit.un_abb
        );
        this.change_depth();
      } else {
        this.width = 0;
        this.change_width();
        this.height = 0;
        this.change_height();
        this.depth = 0;
        this.change_depth();
      }
    },

    async unit(newValue, oldValue) {
      let obj_con = this.$store.state.planner.std_containers[
        this.selected_container
      ];
      if (this.tab === 0 && newValue === obj_con.con_std_unit) {
        this.width = obj_con.con_std_width;
        this.change_width();
        this.height = obj_con.con_std_height;
        this.change_height();
        this.depth = obj_con.con_std_depth;
        this.change_depth();
      } else {
        this.width = this.unit_convert(this.width, oldValue, newValue);
        this.change_width();
        this.height = this.unit_convert(this.height, oldValue, newValue);
        this.change_height();
        this.depth = this.unit_convert(this.depth, oldValue, newValue);
        this.change_depth();
      }
    },
    async show(newValue, oldValue) {
      // if (newValue) {
        this.tab = this.$store.state.planner_dialog.tab;
        this.width = this.$store.state.planner_dialog.width;
        this.height = this.$store.state.planner_dialog.height;
        this.depth = this.$store.state.planner_dialog.depth;
        this.selected_container = this.$store.state.planner_dialog.selected_container;
      // }
        this.err_msg.length = "";
    }
  },
  mounted: function() {
    if (this.is_edit) {
      this.tab = this.$store.state.planner_dialog.tab;
      this.width = this.$store.state.planner_dialog.width;
      this.height = this.$store.state.planner_dialog.height;
      this.depth = this.$store.state.planner_dialog.depth;
      let status = JSON.parse(
        JSON.stringify(this.$store.state.planner_dialog.validation_status)
      );
      status.width = true;
      status.height = true;
      status.depth = true;
      this.$store.commit("planner_dialog/set_validation_status", status);
      this.check_btn_active();
    }
  }
};
</script>
