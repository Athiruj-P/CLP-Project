<script>
export default {
  methods: {
    async render_container() {
      try {
        this.btn_render_status = true;
        let data = new FormData();
        data.append("user_id", this.$store.state.user_id);
        data.append(
          "pln_id",
          this.$store.state.planner_manage.selected_planner._id
        );
        const config = {
          cancelToken: this.$store.state.planner_manage.axios_cancel_token.token
        };
        let render_result = await this.$axios.$post(
          "render_container",
          data,
          config
        );
        this.btn_render_status = false;
        this.$store.commit("planner_manage/set_render_data", render_result);
        localStorage.removeItem("render_result");
        localStorage.setItem("render_result", JSON.stringify(render_result));
      } catch {}
    }
  }
};
</script>
