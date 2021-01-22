<script>
export default {
  methods: {
    async get_all_planner() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      let planners = await this.$axios.$post("get_all_planner", data);
      this.$store.commit("planner/set_planner", planners);
      localStorage.removeItem("planners");
      localStorage.setItem("planners", JSON.stringify(planners));
    },
    async get_planner() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      data.append("pln_id", this.$store.state.planner_dialog.planner_id);
      let planner = await this.$axios.$post("get_planner", data);
      this.$store.commit("planner_manage/set_selected_planner", planner);
      localStorage.removeItem("selected_planner");
      localStorage.setItem("selected_planner", JSON.stringify(planner));
    },
    async get_all_container() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      let container = await this.$axios.$post("get_continer_std", data);
      this.$store.commit("planner/set_std_container", container);
    },
    async get_all_unit() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      let units = await this.$axios.$post("get_all_unit", data);
      this.$store.commit("planner/set_unit", units);
    },
    async get_all_color() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      let color = await this.$axios.$post("get_all_color", data);
      this.$store.commit("planner/set_colors", color);
    },
    async add_planner() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      data.append("name", this.$store.state.planner_dialog.name);
      data.append("width", parseFloat(this.$store.state.planner_dialog.width));
      data.append(
        "height",
        parseFloat(this.$store.state.planner_dialog.height)
      );
      data.append("depth", parseFloat(this.$store.state.planner_dialog.depth));
      data.append("unit", this.$store.state.planner_dialog.unit);
      let result = await this.$axios.$post("add_planner", data);
      this.get_all_planner();
      this.show_alert(result);
      this.close_dialog();
    },
    async edit_planner() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      data.append("pln_id", this.$store.state.planner_dialog.planner_id);
      data.append("name", this.$store.state.planner_dialog.name);
      data.append("width", parseFloat(this.$store.state.planner_dialog.width));
      data.append(
        "height",
        parseFloat(this.$store.state.planner_dialog.height)
      );
      data.append("depth", parseFloat(this.$store.state.planner_dialog.depth));
      data.append("unit", this.$store.state.planner_dialog.unit);
      let result = await this.$axios.$post("edit_planner", data);
      console.log(result);
      this.get_planner();
      this.get_all_planner();
      this.show_alert(result);
      this.close_dialog();
    },
    async delete_planner() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      data.append("pln_id", this.$store.state.planner_dialog.planner_id);
      let result = await this.$axios.$post("delete_planner", data);
      console.log(result);
      this.show_alert(result);
      this.get_all_planner();
      this.close_dialog();
    },
    length_validate(length) {
      let cm_lower = 1;
      let cm_upper = 1500;
      let in_lower = 0.39;
      let in_upper = 590;
      if (this.$store.state.main_unit.un_abb === "cm") {
        var lower = cm_lower;
        var upper = cm_upper;
      } else if (this.$store.state.main_unit.un_abb === "in") {
        var lower = in_lower;
        var upper = in_upper;
      }
      length = Number(length);
      let status;
      status = false;
      if (this.count_decimals(length) > 4) {
        this.err_msg.length = "Length must contain maximum 4 decimal digits.";
      } else if (length < lower || length > upper) {
        let un_abb = this.$store.state.main_unit.un_abb;
        this.err_msg.length = `Length must contain minimum ${lower} ${un_abb} and maximum ${upper} ${un_abb}.`;
      } else {
        status = true;
      }

      if (this.tab === 0) {
        this.err_msg.length = "";
      }
      return status;
    },
    count_decimals(number) {
      if (Math.floor(number) === number) return 0;
      return number.toString().split(".")[1].length || 0;
    },
    check_btn_active() {
      const status = this.$store.state.planner_dialog.validation_status;
      if (
        status.name &&
        status.unit &&
        status.width &&
        status.height &&
        status.depth
      ) {
        this.err_msg.length = "";
        this.$store.commit("planner_dialog/set_btn_active", false);
      } else {
        this.$store.commit("planner_dialog/set_btn_active", true);
      }
    },
    clear_dialog() {
      this.$store.commit("planner_dialog/clear_dialog");
    }
  }
};
</script>
