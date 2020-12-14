<template>
  <div>
      <states-card class="states-card" title="US States"></states-card>
  </div>
</template>
<script>
import StatesCard from "@/components/elements/StatesCard";

export default {
  name: 'Statistics',
  components: {
    StatesCard
  },
  data: function () { return {} },
  computed: {},
  watch: {},
  mounted: function () {},
  methods: {
  }
};
</script>
<style>
.states-card {
  margin-top: 10px;
}
</style>