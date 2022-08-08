<template>
  <div id="errorPageDivBox">
    <img name="404Pic.png" id="errorImg" class="themeImage" alt="404pic">
  </div>
</template>

<script>
import changeAllImgUrl from '@/getThemeImg';

export default {
  data() {
    return {
    };
  },
  mounted() {
    changeAllImgUrl();
  },
};

</script>

<style>
#errorPageDivBox {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#errorImg {
  width: 60%;
}
</style>
