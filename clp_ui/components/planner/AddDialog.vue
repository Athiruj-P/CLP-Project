<template>
  <v-dialog v-model="dialog" persistent width="600">
    <template v-slot:activator="{ attrs }">
      <v-btn color="primary" dark v-bind="attrs" @click="open_dialog">
        <v-icon left>fas fa-plus</v-icon>
        Add planner
      </v-btn>
    </template>
    <v-card>
      <!-- Title header -->
      <v-card-title class="primary">
        <v-icon left color="white">fas fa-plus</v-icon>
        <h1 class="text-white text-3xl">Add planner</h1>
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
                  :pattern="pattern"
                  outlined
                  v-model="name"
                  label="Planner name"
                  clearable
                  max-height="10px"
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
              <v-col md="12" class="pt-0 mb-2">
                <span class="text-xs text-red-500">{{ err_msg.name }}</span>
              </v-col>
            </v-row>
          </v-col>

          <v-col md="4">
            <v-row class="mt-1 ml-0">
              <span>Unit</span>
            </v-row>
            <v-row>
              <v-col md="12" align-self="center">
                <v-row>
                  <v-radio-group
                    v-model="unit"
                    row
                    v-for="(item, index) in $store.state.planner.units"
                    :key="index"
                  >
                    <v-radio
                      class="m-2"
                      :label="item.un_abb"
                      :value="index"
                    ></v-radio>
                    <!-- <v-radio class="m-2" label="in" value="radio-2"></v-radio> -->
                  </v-radio-group>
                </v-row>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        <v-divider></v-divider>

        <!-- Size -->
        <v-row>
          <v-col md="12" class="mt-3">Size</v-col>
        </v-row>
        <v-row>
          <v-col md="12">
            <ContainerSizeTabs
              :show="dialog"
              :unit="$store.state.main_unit.un_abb"
            />
          </v-col>
        </v-row>
        <!-- Size -->
      </v-container>
      <v-divider></v-divider>

      <v-card-actions>
        <v-btn @click="close_dialog">
          Cancel
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          @click="add_planner"
          :disabled="this.$store.state.planner_dialog.btn_active"
        >
          Add
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import ContainerSizeTabs from "@/components/planner/ContainerSizeTabs";
import planner from "@/mixins/planner";
import alert from "@/mixins/alert";
export default {
  mixins: [planner, alert],
  props: {
    // show: {
    //   type: Boolean,
    //   required: true
    // }
  },
  data: () => ({
    pattern: /^([\wก-๙]+ )+[\wก-๙]+$|^[\wก-๙]+$/,
    dialog: false,
    name: "",
    unit: null,
    msg: {
      name:
        "Planner name can contain only alphanumeric characters in English and Thai including a space."
    },
    err_msg: {
      name: ""
    }
  }),
  methods: {
    open_dialog() {
      this.dialog = true;
      this.name = this.$store.state.planner_dialog.name;
      this.unit = 0;
      this.err_msg.name = "";
    },
    on_keyup_name() {
      var status = this.$store.state.planner_dialog.validation_status;
      status.name = false;
      if (this.name.length < 3 || this.name.length > 20) {
        this.err_msg.name =
          "Planner name must contain minimum 3 characters and maximum 20 characters.";
      } else if (this.name.search(this.pattern)) {
        this.err_msg.name = this.msg.name;
      } else {
        this.err_msg.name = "";
        status.name = true;
      }
      this.$store.commit("planner_dialog/set_name", this.name);
      this.$store.commit("planner_dialog/set_validation_status", status);
      this.check_btn_active();
    },
    close_dialog() {
      this.dialog = false;
      this.btn_active = false;
      this.clear_dialog();
    }
  },
  watch: {
    async unit(newValue, oldValue) {
      let status = JSON.parse(
        JSON.stringify(this.$store.state.planner_dialog.validation_status)
      );
      status.unit = true;
      let un_id = this.$store.state.planner.units[this.unit]._id;
      let un_abb = this.$store.state.planner.units[this.unit].un_abb;
      this.check_btn_active();
      this.$store.commit("set_main_unit", { un_id, un_abb });
      this.$store.commit("planner_dialog/set_unit", un_id);
      this.$store.commit("planner_dialog/set_validation_status", status);
    }
  }
};
</script>
