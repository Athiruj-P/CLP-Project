<template>
  <v-dialog v-model="dialog" scrollable persistent width="600">
    <template v-slot:activator="{ attrs }">
      <v-btn color="white" icon v-bind="attrs" @click="open_dialog">
        <v-icon>fas fa-plus</v-icon>
      </v-btn>
    </template>
    <v-card>
      <!-- Title header -->
      <v-card-title class="primary">
        <v-icon left color="white">fas fa-plus</v-icon>
        <h1 class="text-white text-3xl">Add box</h1>
        <v-spacer></v-spacer>
        <v-btn icon @click="close_dialog">
          <v-icon color="white">fas fa-times</v-icon>
        </v-btn>
      </v-card-title>
      <!-- Title header -->
      <v-container class="pl-4 pr-4">
        <v-row>
          <v-col md="8">
            <v-row class="mt-1 ml-0">
              <span>Name</span>
            </v-row>
            <v-row>
              <v-col md="10" class="flex items-center pr-0 pb-0 pt-5">
                <v-text-field
                  dense
                  outlined
                  v-model="name"
                  label="Box name"
                  clearable
                  @keyup="on_keyup_name"
                ></v-text-field>
                <br />
              </v-col>

              <v-col md="2" align-self="center" class="pl-0 pr-0">
                <v-tooltip top color="transparent">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn icon color="primary" dark v-bind="attrs" v-on="on">
                      <v-icon>fas fa-info-circle</v-icon>
                    </v-btn>
                  </template>
                  <v-card color="#1A237E" max-width="300" class="p-2">
                    <span class="text-white text-base p-0 m-0">{{
                      msg.name
                    }}</span>
                  </v-card>
                </v-tooltip>
              </v-col>
            </v-row>
            <v-row>
              <v-col md="12" class="pt-0 pb-0 mb-2">
                <span class="text-xs text-red-500">{{ err_msg.name }}</span>
              </v-col>
            </v-row>
          </v-col>

          <v-col md="4">
            <v-row class="mt-1 ml-0">
              <span>Quantity</span>
            </v-row>
            <v-row>
              <v-col md="10" align-self="center" class="pr-0 pb-0 pt-5">
                <v-text-field
                  type="number"
                  :rules="qty_rules"
                  dense
                  outlined
                  v-model="qty"
                  label="Box quantity"
                  class="px-1"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        <v-divider class="mt-2"></v-divider>

        <!-- Size -->
        <v-row>
          <v-col md="12" class="mt-3">Size</v-col>
        </v-row>
        <v-row>
          <v-col md="12">
            <BoxSizeTabs
              :show="dialog"
              :unit="$store.state.planner_manage.selected_planner.pln_unit"
            />
          </v-col>
        </v-row>
        <!-- Size -->

        <!-- Color list -->
        <v-row>
          <v-col md="12" class="pb-0">Color</v-col>
          <v-list dense class="h-24 w-full">
            <v-list-item-group v-model="selected_color" color="primary">
              <div class="flex flex-row justify-start">
                <div
                  v-for="(item, index) in $store.state.box.colors"
                  :key="index"
                >
                  <v-list-item v-if="index <= 9">
                    <v-list-item-icon class="mx-auto flex justify-center">
                      <v-icon medium :color="`#${item.color_hex}`"
                        >fas fa-dice-d6</v-icon
                      >
                    </v-list-item-icon>
                  </v-list-item>
                  <div class="hidden" v-else></div>
                </div>
              </div>
              <div class="flex flex-row justify-end">
                <div
                  v-for="(item, index) in $store.state.box.colors"
                  :key="index"
                >
                  <v-list-item v-if="index > 9">
                    <v-list-item-icon class="mx-auto flex justify-center">
                      <v-icon medium :color="`#${item.color_hex}`"
                        >fas fa-dice-d6</v-icon
                      >
                    </v-list-item-icon>
                  </v-list-item>
                  <div class="hidden" v-else></div>
                </div>
              </div>
            </v-list-item-group>
          </v-list>
        </v-row>
        <!-- Color list -->
      </v-container>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn @click="close_dialog">
          Cancel
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          @click="add_box"
          :disabled="this.$store.state.box_dialog.btn_active"
        >
          Add
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import BoxSizeTabs from "@/components/planner_manager/BoxSizeTabs";
import box from "@/mixins/box";
import alert from "@/mixins/alert";
export default {
  mixins: [box, alert],
  data: () => ({
    selected_color: null,
    qty_rules: [
      v => !!v || "Required",
      v => v >= 1 || "Quantity must be above 1",
      v => v <= 100 || "Quantity must be below 100",
      v => Number.isInteger(Number(v)) || "Quantity must be integer"
    ],
    pattern: /^([\wก-๙]+ )+[\wก-๙]+$|^[\wก-๙]+$/,
    dialog: false, //True เพื่อการทดสอบเท่านั้น False ต้องเป็นค่าเริ่มต้น
    name: "",
    unit: null,
    qty: 0,
    msg: {
      name:
        "Box name can contain only alphanumeric characters in English and Thai including a space."
    },
    err_msg: {
      name: ""
    }
  }),
  methods: {
    open_dialog() {
      this.dialog = true;
      this.selected_color = 0;
      this.qty = this.$store.state.box_dialog.qty;
      this.unit = this.$store.state.planner_manage.selected_planner.pln_unit;
      this.err_msg.name = "";
      this.set_selected_color();
    },
    on_keyup_name() {
      let status = JSON.parse(
        JSON.stringify(this.$store.state.box_dialog.validation_status)
      );
      status.name = false;
      if (this.name.length < 3 || this.name.length > 20) {
        this.err_msg.name =
          "Box name must contain between 3 and 20 characters.";
      } else if (this.name.search(this.pattern)) {
        this.err_msg.name = this.msg.name;
      } else {
        this.err_msg.name = "";
        status.name = true;
      }
      this.$store.commit("box_dialog/set_name", this.name);
      this.$store.commit("box_dialog/set_validation_status", status);
      this.check_btn_active();
      console.log("Key up");
      console.log(this.$store.state.box_dialog.validation_status);
    },
    set_selected_color() {
      let status = JSON.parse(
        JSON.stringify(this.$store.state.box_dialog.validation_status)
      );
      status.color = false;
      if (Number.isInteger(Number(this.selected_color))) {
        status.color = true;
        this.$store.commit(
          "box_dialog/set_color",
          this.$store.state.box.colors[this.selected_color]._id
        );
      }
      this.$store.commit("box_dialog/set_validation_status", status);
      this.check_btn_active();
    },
    close_dialog() {
      this.clear_dialog();
      this.name = "";
      this.btn_active = false;
      this.selected_color = 0;
      this.qty = 1;
      this.dialog = false;
    }
  },
  watch: {
    qty(newValue, oldValue) {
      let status = JSON.parse(
        JSON.stringify(this.$store.state.box_dialog.validation_status)
      );
      status.qty = false;
      if (newValue) {
        if (this.qty_validate(newValue)) {
          status.qty = true;
        }
      }
      this.$store.commit("box_dialog/set_qty", Number(newValue));
      this.$store.commit("box_dialog/set_validation_status", status);
      this.check_btn_active();
    },
    selected_color(newValue, oldValue) {
      this.set_selected_color();
    }
  }
};
</script>
