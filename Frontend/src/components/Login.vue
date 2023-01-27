<template>
  <v-btn v-if="!loggedIn" @click="Login()" variant="outlined"> Login </v-btn>
  <div v-if="loggedIn">
    Logged in as {{ name }}
    <v-btn @click="Logout()" variant="outlined"> Logout </v-btn>
  </div>
</template>

<script lang="ts">
import axios, { AxiosError } from "axios";

export default {
  data() {
    return {
      loggedIn: false,
      name: null as any,
    };
  },
  methods: {
    async Login() {
      var response = await axios
        .get("http://localhost:8040/auth/login/", { withCredentials: true })
        .then((res) => res.data)
        .catch((error: AxiosError) => {
          console.error(`There was an error with ${error.config!.url}.`);
          console.error(error.toJSON());
        });
      window.location.href = response;
    },
    async Logout() {
      var response = await axios
        .get("http://localhost:8040/auth/logout/", { withCredentials: true })
        .then((res) => res.data)
        .catch((error: AxiosError) => {
          console.error(`There was an error with ${error.config!.url}.`);
          console.error(error.toJSON());
        });
      window.location.reload();
    },
  },
  created: async function () {
    this.loggedIn = await axios
      .get("http://localhost:8040/auth/checkLogin/", { withCredentials: true })
      .then((res) => res.data)
      .catch((error: AxiosError) => {
        console.error(`There was an error with ${error.config!.url}.`);
        console.error(error.toJSON());
      });

    if (this.loggedIn) {
      this.name = await axios
        .get("http://localhost:8040/api/getName/", { withCredentials: true })
        .then((res) => res.data)
        .catch((error: AxiosError) => {
          console.error(`There was an error with ${error.config!.url}.`);
          console.error(error.toJSON());
        });
    }
  },
};
</script>
