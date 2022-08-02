<template>
  <div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      services: [
        {
          id: 'xxx',
          time: 'xxx',
          status: 'running',
          count: 'xxx',
          averResTime: 'xxx',
          maxResTime: 'xxx',
          minResTime: 'xxx',
        },
      ],
    };
  },
  methods: {

  },
  mounted() {
    // TODO
    // 从后端获取数据
  },
};
</script>

<style>
</style>
