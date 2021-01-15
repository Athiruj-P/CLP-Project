<template>
  <v-card>
    <!-- <v-card-title class="text-center justify-center py-2">
      <span class="text-base font-normal">Size</span>
    </v-card-title> -->

    <v-tabs v-model="tab" background-color="transparent" grow>
      <v-tab>Container</v-tab>
      <v-tab>Other</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-card flat>
          <v-card-text>Text</v-card-text>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-text>
            <!-- Container width -->
            <v-row>
              <v-col md="4">
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
                    clearable
                    class="px-1"
                  ></v-text-field>
                </v-row>
              </v-col>
              <!-- Container width -->
              <!-- Container height -->
              <v-col md="4">
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
                    clearable
                    class="px-1"
                  ></v-text-field>
                </v-row>
              </v-col>
              <!-- Container height -->
              <!-- Container depth -->
              <v-col md="4">
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
                    clearable
                    class="px-1"
                  ></v-text-field>
                </v-row>
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
export default {
  props: {
    // show: {
    //   type: Boolean,
    //   required: true
    // }
  },
  data: () => ({
    tab: null
  }),
  methods: {}
};
</script>
