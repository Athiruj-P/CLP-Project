<script>
export default {
  methods: {
    async login() {
      let data = new FormData();
      data.append("username", this.username);
      data.append("password", this.password);

      this.result = await this.$axios.$post("login", data);
      if (this.result.status === "success") {
        localStorage.setItem("username", this.username);
        localStorage.setItem("user_id", this.result.user_id);
      }
    },
    async logout() {
      let data = new FormData();
      data.append("username", this.$store.state.username);
      await this.$axios.$post("logout", data);
      this.$store.commit("clear_login");
      this.$store.commit("planner_manage/clear_value");
      this.$store.commit("planner/clear_value");
      this.$store.commit("box/clear_value");
      localStorage.clear();
      this.$router.push("login");
    }
  }
};
</script>
