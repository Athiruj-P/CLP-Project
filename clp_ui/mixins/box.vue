<script>
import conversions from "conversions";
export default {
  methods: {
    set_axios_cancel_token() {
      const CancelToken = this.$axios.CancelToken;
      const source = CancelToken.source();
      this.$store.commit("planner_manage/set_axios_cancel_token", source);
    },
    unit_convert(number, old_unit, new_unit) {
      if (old_unit !== new_unit)
        return conversions(number, old_unit, new_unit).toFixed(2);
      else return number;
    },
    async get_all_box() {
      try {
        let data = new FormData();
        data.append("user_id", this.$store.state.user_id);
        data.append(
          "pln_id",
          this.$store.state.planner_manage.selected_planner._id
        );
        const config = {
          cancelToken: this.$store.state.planner_manage.axios_cancel_token.token
        };
        let boxes = await this.$axios.$post("get_all_box", data, config);
        boxes.reverse();
        this.$store.commit("box/set_boxes", boxes);
        localStorage.removeItem("boxes");
        localStorage.setItem("boxes", JSON.stringify(boxes));
      } catch {}
    },
    async get_box_std() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      let boxes = await this.$axios.$post("get_box_std", data);
      this.$store.commit("box/set_std_boxes", boxes);
      localStorage.removeItem("box_std");
      localStorage.setItem("box_std", JSON.stringify(boxes));
    },
    async get_all_color() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      let colors = await this.$axios.$post("get_all_color", data);
      this.$store.commit("box/set_colors", colors);
    },
    //
    async add_box_by_excel(file) {
      this.$store.commit("planner_manage/set_is_box_list_change", true);
      let data = new FormData();
      var set_status = this.set_btn_excel_status;
      data.append("user_id", this.$store.state.user_id);
      data.append(
        "pln_id",
        this.$store.state.planner_manage.selected_planner._id
      );
      data.append("file", file);
      set_status(true);
      const config = {
        onUploadProgress: function(progressEvent) {
          var percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          if (percentCompleted === 100) {
            set_status(false);
          }
        }
      };
      let result = await this.$axios.$post("add_box_by_excel", data, config);
      this.$refs.excel_file.value = null;
      this.get_all_box();
      this.show_alert(result);
    },
    async add_box() {
      this.$store.commit("planner_manage/set_is_box_list_change", true);
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      data.append(
        "pln_id",
        this.$store.state.planner_manage.selected_planner._id
      );
      data.append("name", this.$store.state.box_dialog.name);
      data.append("width", this.$store.state.box_dialog.width);
      data.append("height", this.$store.state.box_dialog.height);
      data.append("depth", this.$store.state.box_dialog.depth);
      data.append("unit", this.$store.state.main_unit.un_id);
      data.append("color", this.$store.state.box_dialog.color);
      data.append("qty", this.$store.state.box_dialog.qty);
      let result = await this.$axios.$post("add_box", data);
      this.get_all_box();
      this.show_alert(result);
      this.close_dialog();
    },
    //
    async edit_box() {
      this.$store.commit("planner_manage/set_is_box_list_change", true);
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      data.append("box_id", this.obj_box._id);
      data.append("name", this.$store.state.box_dialog.name);
      data.append("width", this.$store.state.box_dialog.width);
      data.append("height", this.$store.state.box_dialog.height);
      data.append("depth", this.$store.state.box_dialog.depth);
      data.append("unit", this.$store.state.main_unit.un_id);
      data.append("color", this.$store.state.box_dialog.color);
      data.append("qty", this.$store.state.box_dialog.qty);
      let result = await this.$axios.$post("edit_box", data);
      this.get_all_box();
      this.show_alert(result);
      this.close_dialog();
    },
    //
    async delete_box() {
      this.$store.commit("planner_manage/set_is_box_list_change", true);
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      data.append("box_id", this.obj_box._id);
      let result = await this.$axios.$post("delete_box", data);
      this.show_alert(result);
      this.get_all_box();
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
      } else if (un_abb === "inch") {
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
      if (Number.isInteger(qty) && qty >= 1 && qty <= 100) {
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
