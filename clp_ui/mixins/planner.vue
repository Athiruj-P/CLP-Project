<script>
export default {
  methods: {
    async get_all_planner() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      let planners = await this.$axios.$post("get_all_planner", data);
      this.$store.commit("planner/set_planner", planners);
      console.log(this.planners);
    },
    async get_all_unit() {
      let data = new FormData();
      data.append("user_id", this.$store.state.user_id);
      let units = await this.$axios.$post("get_all_unit", data);
      this.$store.commit("planner/set_unit", units);
      console.log(this.units);
    }
  }
};
</script>
