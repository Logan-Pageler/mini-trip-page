<template>
  <v-btn v-if="!token" href="http://localhost:8040/auth/Login/"> Login </v-btn>
  <div v-if="token">Logged in as {{ name }}</div>
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
    async tryLogin() {
      var response = await axios
        .get("http://localhost:8040/auth/Login/")
        .then((res) => res.data)
        .catch((error: AxiosError) => {
          console.error(`There was an error with ${error.config!.url}.`);
          console.error(error.toJSON());
        });
      console.log(response);
    },
  },
  created: async function () {
    console.log(this.$route.query.token);
    this.token = this.$route.query.token;
    this.name = this.$route.query.name;
  },
};
</script>
