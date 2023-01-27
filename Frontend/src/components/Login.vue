<template>
  <v-btn v-if="!token" @click="Login()" variant="outlined"> Login </v-btn>
  <div v-if="token">
    Logged in as {{ name }}
    <v-btn href="http://localhost:3000" variant="outlined"> Logout </v-btn>
  </div>
</template>

<script lang="ts">
import axios, { AxiosError } from "axios";

export default {
  data() {
    return {
      token: null as any,
      name: null as any,
    };
  },
  methods: {
    async Login() {
      console.log("hello");
      var response = await axios
        .get("http://localhost:8040/auth/login/", { withCredentials: true })
        .then((res) => res.data)
        .catch((error: AxiosError) => {
          console.error(`There was an error with ${error.config!.url}.`);
          console.error(error.toJSON());
        });
      console.log(response);
      window.location.href = response;
    },
  },
  created: async function () {
    console.log(this.$route.query.token);
    this.token = this.$route.query.token;
    this.name = this.$route.query.name;
  },
};
</script>
