<template>
  <v-dialog v-model="dialog" persistent width="600">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="primary" dark v-bind="attrs" v-on="on">
        <v-icon left>fas fa-plus</v-icon>
        Add planner
      </v-btn>
    </template>
    <v-card>
      <!-- Toolbar header -->
      <v-toolbar color="primary">
        <v-icon left color="white">fas fa-plus</v-icon>
        <h1 class="text-white text-3xl">Add planner</h1>
        <v-spacer></v-spacer>
        <v-btn icon @click="dialog = false">
          <v-icon color="white">fas fa-times</v-icon>
        </v-btn>
      </v-toolbar>
      <!-- Toolbar header -->
      <v-container class="pl-4 pr-4">
        <v-row>
          <v-col md="1" class="text-right ml-2 pl-0 pr-0" align-self="center">
            <span>Name:</span>
          </v-col>
          <v-col md="5" class="flex items-center pr-0 pb-0 pt-5">
            <v-text-field
              dense
              outlined
              v-model="name"
              label="Planner name"
              clearable
              max-height="10px"
            ></v-text-field>
          </v-col>

          <v-col md="1" align-self="center" class="pl-0 pr-0">
            <v-tooltip top color="transparent">
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon color="primary" dark v-bind="attrs" v-on="on">
                  <v-icon>fas fa-info-circle</v-icon>
                </v-btn>
              </template>
              <v-card color="#1A237E" max-width="300" class="p-2">
                <span class="text-white text-base p-0 m-0">{{ msg.name }}</span>
              </v-card>
            </v-tooltip>
          </v-col>

          <v-col md="1" class="text-right pl-0 pr-0" align-self="center">
            <span>Unit:</span>
          </v-col>
          <v-col md="3" align-self="center">
            <v-row>
              <v-radio-group v-model="unit" row>
                <v-radio class="m-2" label="cm" value="radio-1"></v-radio>
                <v-radio class="m-2" label="in" value="radio-2"></v-radio>
              </v-radio-group>
            </v-row>
          </v-col>
        </v-row>
        <hr />

        <!-- Size -->
        <v-row>
          <v-col md="12" class="mt-3">Size:</v-col>
        </v-row>
        <v-row>
          <v-col md="12">
            <ContainerSizeTabs />
          </v-col>
        </v-row>
        <!-- Size -->
      </v-container>
      <hr />

      <v-card-actions>
        <v-btn text @click="dialog = false">
          Cancel
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="dialog = false">
          Add
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import ContainerSizeTabs from "@/components/planner/ContainerSizeTabs";
export default {
  props: {
    // show: {
    //   type: Boolean,
    //   required: true
    // }
  },
  data: () => ({
    dialog: false,
    name: "",
    unit: "",
    msg: {
      name:
        "Planner name can contain only alphanumeric characters in English and Thai including a space."
    }
  }),
  methods: {
    // onSave() {
    //   //
    //   console.log(this.editedPost);
    // },
    // onCancel() {
    //   //   to navigate back
    //   this.$router.push("/admin");
    // }
  }
};
</script>

<style scoped>
/* .tooltip-background-color {
background-color: transparent;
} */
</style>
