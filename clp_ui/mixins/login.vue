<script>
export default {
  methods: {
    async login() {
      let data = new FormData();
      data.append("username", this.username);
      data.append("password", this.password);

      this.result = await this.$axios.$post("login", data);
    },
    async logout() {
      let data = new FormData();
      data.append("username", this.username);
      await this.$axios.$post("logout", data);
      this.$store.commit("clear_login");
      this.$router.push("login");
    }
  }
};
</script>
