<template>
  <div ref="container" id="container" class="h-full py-3"></div>
</template>

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
import stack from "@/mixins/stack";
export default {
  mixins: [stack],
  data: () => ({
    Plotly: null,
    CON_X: null,
    CON_Z: null,
    CON_Y: null,
    plot_data: [],
    boxes_stack: []
  }),
  beforeMount() {
    if (this.$store.state.planner_manage.selected_stack_list) {
      this.boxes_stack = this.$store.state.planner_manage.selected_stack_list;
      // this.boxes_stack = JSON.parse(local_store_render_result).boxes_stack;
    }
    this.Plotly = require("plotly.js/dist/plotly");
    this.set_container();
  },
  mounted() {
    this.plot_graph();
    this.init_plotly();
    // this.plot_redraw();
  },
  methods: {
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
    init_plotly() {
      var layout = {
        hoverlabel: { bgcolor: "#FFF" },
        scene: {
          aspectmode: "data",
          domain: { row: 1, column: 1 }
        },
        modebar: {
          orientation: "v"
        },
        margin: { t: 0, l: 0, b: 0, r: 0 }
      };
      var config = { responsive: true };
      this.Plotly.plot(this.$refs.container, this.plot_data, layout, config);
    },
    plot_graph() {
      this.plot_data = [];
      var data = [];
      const container = new Box(
        [0, this.CON_X, 0, this.CON_X, 0, this.CON_X, 0, this.CON_X], // X (Width)
        [0, 0, this.CON_Y, this.CON_Y, 0, 0, this.CON_Y, this.CON_Y], // Y (Depth)
        [0, 0, 0, 0, this.CON_Z, this.CON_Z, this.CON_Z, this.CON_Z], // Z (Height)
        0.2
      );
      data.push(container.data);
      // Temporary
      if (this.boxes_stack.length > 0) {
        this.boxes_stack.forEach(item_index => {
          item_index.forEach(element => {
            const obj = new Box(
              Object.values(element.box_dim.x),
              Object.values(element.box_dim.y),
              Object.values(element.box_dim.z),
              1,
              element.box_detail.box_color
            );
            data.push(obj.data);
          });
        });
      }
      this.plot_data = data;
      // Temporary
    },
    plot_redraw() {
      this.plot_graph();
      this.$refs.container.data = this.plot_data;
      this.Plotly.redraw(this.$refs.container);
    }
  },
  watch: {
    "$store.state.planner_manage.render_data"(render_data) {
      // this.boxes_stack = render_data.boxes_stack;
      // this.plot_redraw();
    },
    "$store.state.planner_manage.selected_stack_list"(data) {
      this.boxes_stack = this.$store.state.planner_manage.selected_stack_list;
      this.plot_redraw();
    },
    "$store.state.planner_manage.selected_planner"(data) {
      this.set_container();
      this.plot_redraw();
    }
  },
  destroyed() {
    localStorage.removeItem("render_result");
  }
};
</script>

<style scoped></style>
