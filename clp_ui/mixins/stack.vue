<script>
class Box {
  constructor(x, y, z, op = 1, custom_color = "rgb(0, 0, 255)") {
    var intensity = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1];
    var white = "rgb(255, 255, 255)";
    var custom_color = custom_color;
    this.data = {
      x: x,
      y: y,
      z: z,
      i: [0, 3, 4, 7, 0, 6, 1, 7, 0, 5, 2, 7],
      j: [1, 2, 5, 6, 2, 4, 3, 5, 4, 1, 6, 3],
      k: [3, 0, 7, 4, 6, 0, 7, 1, 5, 0, 7, 2],
      intensity: intensity,
      colorscale: [
        [0, white],
        [1, custom_color]
      ],
      showscale: false,
      opacity: op,
      hoverinfo: "skip",
      flatshading: true, // important
      lighting: {
        facenormalsepsilon: 0 // important
      },
      lightposition: {
        x: 2000,
        y: 1000
      },
      type: "mesh3d",
      name: ""
    };
  }
}
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
        this.$store.commit("planner_manage/set_is_box_list_change", false);
        try {
          this.set_container();
          this.plot_redraw();
        } catch {}
      } catch {}
    },
    set_container() {
      this.plot_data = [];
      this.CON_X = this.$store.state.planner_manage.selected_planner.pln_width;
      this.CON_Z = this.$store.state.planner_manage.selected_planner.pln_height;
      this.CON_Y = this.$store.state.planner_manage.selected_planner.pln_depth;
      const container = new Box(
        [0, this.CON_X, 0, this.CON_X, 0, this.CON_X, 0, this.CON_X], // X (Width)
        [0, 0, this.CON_Y, this.CON_Y, 0, 0, this.CON_Y, this.CON_Y], // Y (Depth)
        [0, 0, 0, 0, this.CON_Z, this.CON_Z, this.CON_Z, this.CON_Z], // Z (Height)
        0.1
      );
      this.plot_data.push(container.data);
    },
    plot_redraw() {
      this.plot_graph();
      this.$refs.container.data = this.plot_data;
      this.Plotly.redraw(this.$refs.container);
    }
  }
};
</script>
