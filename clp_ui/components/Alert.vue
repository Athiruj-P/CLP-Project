<template>
  <!-- Alert -->
  <v-snackbar
    class="pt-4"
    :color="$store.state.color_alert"
    v-model="show_alert"
    :timeout="$store.state.timeout"
    absolute
    right
    shaped
    top
  >
    <v-icon>{{ $store.state.icon_alert }}</v-icon>
    <span class="ml-3 text-base"
      >{{ $store.state.text_alert }}</span
    >

    <template v-slot:action="{ attrs }">
      <v-btn text v-bind="attrs" @click="show_alert = false">
        <v-icon>fas fa-times</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
  <!-- Alert -->
</template>

<script>
export default {
  computed: {
    show_alert: {
      get() {
        return this.$store.state.show_alert;
      },
      set(value) {
        this.$store.commit("set_show_alert", value);
      }
    },
  },
  watch: {}
};
</script>
