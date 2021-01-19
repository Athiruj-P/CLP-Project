<script>
export default {
  methods: {
    show_alert(data) {
      if (data.status === "error" || data.status === "system_error") {
        this.$store.commit("set_alert_data", {
          text_alert: data.mes,
          color_alert: "red",
          icon_alert: "fas fa-exclamation-circle"
        });
      } else {
        this.$store.commit("set_alert_data", {
          text_alert: data.mes,
          color_alert: "success",
          icon_alert: "fas fa-check-circle"
        });
      }
      this.$store.commit("set_show_alert", true);
    }
  }
};
</script>
