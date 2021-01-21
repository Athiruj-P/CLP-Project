<script>
export default {
  methods: {
    async get_all_box() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      data.append("pln_id", this.selected_planner._id);
      let boxes = await this.$axios.$post("get_all_box", data);
      this.$store.commit("box/set_boxes", boxes);
      localStorage.removeItem("boxes");
      localStorage.setItem("boxes", JSON.stringify(boxes));
    },
    async get_box_std() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      let boxes = await this.$axios.$post("get_box_std", data);
      this.$store.commit("box/set_std_boxes", boxes);
    },
    async get_all_color() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      let colors = await this.$axios.$post("get_all_color", data);
      this.$store.commit("box/set_colors", colors);
    },
    //
    async add_box() {
      console.log(this.$store.state.planner_manage.selected_planner._id);
      console.log(this.$store.state.box_dialog.name);
      console.log(this.$store.state.box_dialog.width);
      console.log(this.$store.state.box_dialog.height);
      console.log(this.$store.state.box_dialog.depth);
      console.log(this.$store.state.main_unit.un_id);
      console.log(this.$store.state.box_dialog.qty);
      console.log(this.$store.state.box_dialog.color);
      //   let data = new FormData();
      //   data.append("user_id", this.$store.state.user_id);
      //   data.append("name", this.$store.state.planner_dialog.name);
      //   data.append("width", parseFloat(this.$store.state.planner_dialog.width));
      //   data.append(
      //     "height",
      //     parseFloat(this.$store.state.planner_dialog.height)
      //   );
      //   data.append("depth", parseFloat(this.$store.state.planner_dialog.depth));
      //   data.append("unit", this.$store.state.planner_dialog.unit);
      //   let result = await this.$axios.$post("add_planner", data);
      //   this.get_all_planner();
      //   this.show_alert(result);
      //   this.close_dialog();
    },
    //
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
      this.get_all_planner();
      this.show_alert(result);
      this.close_dialog();
    },
    //
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
      let un_abb = this.$store.state.main_unit.un_abb;
      if (un_abb === "cm") {
        var lower = cm_lower;
        var upper = cm_upper;
      } else if (un_abb === "in") {
        var lower = in_lower;
        var upper = in_upper;
      }
      length = Number(length);
      let status;
      status = false;
      if (!Number(length) || length < lower || length > upper) {
        this.err_msg.length = `Length must contain minimum ${lower} ${un_abb} and maximum ${upper} ${un_abb}.`;
      } else if (this.count_decimals(length) > 4) {
        this.err_msg.length = "Length must contain maximum 4 decimal digits.";
      } else {
        status = true;
      }

      if (this.tab === 0) {
        this.err_msg.length = "";
      }
      return status;
    },
    qty_validate(qty) {
      qty = Number(qty);
      let status;
      status = false;
      if (!Number.isInteger(qty) || qty < 1) {
      } else {
        status = true;
        this.err_msg.length = "";
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
      const status = this.$store.state.box_dialog.validation_status;
      if (
        status.name &&
        status.qty &&
        status.width &&
        status.height &&
        status.depth &&
        status.color
      ) {
        this.err_msg.length = "";
        this.$store.commit("box_dialog/set_btn_active", false);
      } else {
        this.$store.commit("box_dialog/set_btn_active", true);
      }
    },
    clear_dialog() {
      this.$store.commit("box_dialog/clear_dialog");
    }
  }
};
</script>
