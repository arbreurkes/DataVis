<template>
  <div :class="[{'md-layout-item': inGrid}, size]">
    <md-card ref="card">
      <md-card-actions class="md-alignment-left">
        <div class="md-title">{{title}}</div>
        <md-icon class="info-icon">info
          <md-tooltip md-direction="left">{{title}}</md-tooltip>
        </md-icon>
      </md-card-actions>
      <md-card-content class="card-content">
        Content here.
      </md-card-content>
      <md-card-actions class="actions">
        <md-button class="vote-button md-raised">Action</md-button>
      </md-card-actions>
    </md-card>
  </div>
</template>
<script>
import {mapActions, mapGetters} from 'vuex';

export default {
  name: 'BasicCard',
  props: {
    title: String, // Title of the card.
    size: String, // Size of card in gutter.
    inGrid: Boolean, // Is this card in gutter?
  },
  data: function() {
    return {}
  },
  computed: {},
  methods: {
    ...mapActions([]),
    ...mapGetters([]),
  }
};
</script>
<style scoped>
.card-content {
  height: calc(100% - 100px) !important;
}

.actions {
  justify-content: center !important;
}
</style>