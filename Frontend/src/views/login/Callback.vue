<template>
  <div>
    <h1>Logging in...</h1>
  </div>
</template>

<script lang="ts">
import axios, { AxiosError } from "axios";

export default {
  async mounted() {
    var response = await axios
      .get("http://localhost:8040/auth/callback" + window.location.search, {
        withCredentials: true,
      })
      .then((res) => res.data)
      .catch((error: AxiosError) => {
        console.error(`There was an error with ${error.config!.url}.`);
        console.error(error.toJSON());
      });
    window.location.href = response;
  },
};
</script>
