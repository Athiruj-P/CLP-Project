<template>
  <v-dialog v-model="dialog" scrollable persistent width="600">
    <template v-slot:activator="{ attrs }">
      <v-btn id="btn-modal-edit-box" icon v-bind="attrs" @click="open_dialog">
        <v-icon>fas fa-ellipsis-h</v-icon>
      </v-btn>
    </template>
    <v-card>
      <!-- Title header -->
      <v-card-title class="warning">
        <v-icon left color="white">fas fa-edit</v-icon>
        <h1 class="text-white text-3xl">Edit box</h1>
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
                  id="edit-box-name-input"
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
                  id="edit-box-qty-input"
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
              :is_edit="true"
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
                  <v-list-item
                    :id="'edit-box-color-' + index"
                    v-if="index <= 9"
                  >
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
                  <v-list-item :id="'edit-box-color-' + index" v-if="index > 9">
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
        <!-- Delete section -->
        <v-menu
          v-model="popover"
          :close-on-content-click="false"
          :nudge-width="150"
          offset-y
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn id="btn-delete-box" color="error" dark v-bind="attrs" v-on="on">
              Delete
            </v-btn>
          </template>

          <v-card>
            <v-container class="text-center">
              <v-icon color="red" class="x-large"
                >fas fa-exclamation-triangle</v-icon
              >
              <br />
              <span>Are you sure<br />to delete these boxes</span>
            </v-container>
            <v-card-actions>
              <v-btn @click="popover = false">
                Cancel
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn id="btn-cf-delete-box" color="error" @click="delete_box">
                Yes
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
        <!-- Delete section -->
        <v-btn
          id="btn-edit-box"
          color="warning"
          @click="edit_box"
          :disabled="this.$store.state.box_dialog.btn_active"
        >
          Edit
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
  props: {
    obj_box: {
      type: Object,
      required: false
    }
  },
  data: () => ({
    popover: false,
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
      let status = JSON.parse(
        JSON.stringify(this.$store.state.planner_dialog.validation_status)
      );

      const pln_unit = this.$store.state.planner_manage.selected_planner
        .pln_unit;

      this.$store.commit("box_dialog/set_name", this.obj_box.box_name);
      this.$store.commit(
        "box_dialog/set_width",
        this.unit_convert(
          this.obj_box.box_width,
          this.obj_box.box_unit,
          pln_unit
        )
      );
      this.$store.commit(
        "box_dialog/set_height",
        this.unit_convert(
          this.obj_box.box_height,
          this.obj_box.box_unit,
          pln_unit
        )
      );
      this.$store.commit(
        "box_dialog/set_depth",
        this.unit_convert(
          this.obj_box.box_depth,
          this.obj_box.box_unit,
          pln_unit
        )
      );
      this.$store.commit("box_dialog/set_unit", pln_unit);
      this.$store.commit("box_dialog/set_qty", this.obj_box.box_quantity);
      this.$store.commit("box_dialog/set_color", this.obj_box.box_color);
      this.$store.commit("box_dialog/set_tab", 1);
      this.name = this.obj_box.box_name;
      this.qty = this.obj_box.box_quantity;
      this.$store.state.planner.units.some((val, index) => {
        if (val.un_abb === this.obj_box.box_unit) {
          this.unit = index;
          return true;
        }
      });
      this.$store.state.box.colors.some((val, index) => {
        if (val.color_hex === this.obj_box.box_color) {
          this.selected_color = index;
          return true;
        }
      });
      this.err_msg.name = "";

      // ปรับให้สถานะของ validation เป็น true ทั้งหมดเสมอ
      status.name = true;
      status.width = true;
      status.height = true;
      status.depth = true;
      status.qty = true;
      status.color = true;
      this.$store.commit("box_dialog/set_validation_status", status);
      this.check_btn_active();
      this.dialog = true;
    },
    on_keyup_name() {
      let status = JSON.parse(
        JSON.stringify(this.$store.state.box_dialog.validation_status)
      );
      status.name = false;
      if (!this.name) {
        this.err_msg.name =
          "Box name must contain between 3 and 20 characters.";
      } else if (this.name.length < 3 || this.name.length > 20) {
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
    },
    close_dialog() {
      this.dialog = false;
      this.btn_active = false;
      this.selected_color = 0;
      this.qty = 1;
      this.clear_dialog();
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
      let status = JSON.parse(
        JSON.stringify(this.$store.state.box_dialog.validation_status)
      );
      status.color = false;
      if (Number.isInteger(Number(newValue))) {
        status.color = true;
        this.$store.commit(
          "box_dialog/set_color",
          this.$store.state.box.colors[newValue]._id
        );
      }
      this.$store.commit("box_dialog/set_validation_status", status);
      this.check_btn_active();
    },
    name(newVal) {
      if (!newVal) {
        this.on_keyup_name();
      }
    }
  }
};
</script>
