<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <Login />
      <ExcelTable />

      
    </v-responsive>
  </v-container>
</template>

<script type='ts' setup >
  import ExcelTable from '@/components/ExcelTable.vue';
  import Login from '@/components/Login.vue'
</script>
