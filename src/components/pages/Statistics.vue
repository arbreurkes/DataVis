<template>
  <div class="tasks-page" ref="find">
    <div v-if="!done">
      <md-tabs md-alignment="fixed" md-sync-route>
        <template slot="md-tab" slot-scope="{tab}">
                <span class="tab-label">
                    <md-icon class="tab-icon" v-if="tab.data.icon">{{ tab.data.icon }}</md-icon> {{ tab.label }}
                </span>
        </template>

        <md-tab id="tab-map" class="tab-one" md-label="States" :md-template-data="{icon: 'public'}"
                to="/stats/tabOne">
          <states-card title="US States" :stats="null" :inGrid="true" size="md-size-100"></states-card>
        </md-tab>
        <md-tab id="tab-two" class="tab-two" md-label="Counties" :md-template-data="{icon: 'map'}"
                to="/stats/tabTwo">
<!--          <counties-card title="US Counties" :stats="null" :inGrid="true" size="md-size-100"></counties-card>-->
        </md-tab>
      </md-tabs>
      <hr class="tab-divider"/>
    </div>
  </div>
</template>
<script>
import StatesCard from "@/components/elements/StatesCard";
// import CountiesCard from "@/components/elements/CountiesCard";
import {mapActions, mapGetters, mapMutations} from 'vuex'

export default {
  name: 'Statistics',
  components: {
    StatesCard,
    // CountiesCard
  },
  data: function () {
    return {
      done: false // True on submitting task.
    }
  },
  computed: {},
  watch: {},
  mounted: function () { // On first loading this page.
    this.$nextTick(() => {
    }); // On Vue's next tick (time).
  },
  methods: {
    ...mapActions([]),
    ...mapGetters([]),
    ...mapMutations(['setSnackbarMessage']),
  }
};
</script>
<style>
.tasks-page {
  width: 100%;
  height: calc(100vh - 48px);
}

.tab-divider {
  position: absolute;
  width: 100vw;
  margin-top: -1px;
  top: 96px;
}

.tab-icon {
  margin-top: -5px;
}

.tab-label {
  font-size: 16px !important;
}

.md-tab {
  height: calc(100vh - 96px);
  max-height: 100%;
  /*width: 100%;*/
}

.tab-one, .tab-two {
  overflow-y: scroll;
}

.md-content.md-tabs-content {
  padding-bottom: 8px;
  height: calc(100vh - 96px) !important;
}

.md-button.md-tab-nav-button {
  max-width: 100vw !important;
}

.md-button.md-tab-nav-button.md-active {
  color: var(--forest-green) !important;
}

.md-tabs-indicator {
  background-color: var(--forest-green) !important;
}

.md-tabs .md-tabs-navigation .md-button .md-icon {
  color: var(--forest-green) !important;
}

.map {
  margin: -16px 0 0 -16px;
  height: calc(100% + 32px);
  width: calc(100% + 32px);
}

.options {
  width: 120px;
  justify-content: center;
  position: absolute;
  left: calc(150vw - 60px);
  top: 10px;
  z-index: 999;
}

.annotate-button {
  margin-right: 0;
  margin-top: 0;
}

.snapshot-button {
  position: absolute;
  bottom: 10px;
  left: calc(150vw - 28px)
}

.big-annotation {
  margin-top: 8px;
}

.tab-one, .tab-two {
  padding: 16px !important;
}

.instruction-title {
  margin-top: 0 !important;
}

.instructions {
  text-align: center;
  position: absolute;
  /*z-index: 20;*/
  width: 33%;
}

.submit-dialog {
  z-index: 1000 !important;
}

.annotation-count {
  text-align: center;
  position: absolute;
  z-index: 20;
  bottom: -15px;
  width: 140px;
  color: white;
  left: calc(150vw - 70px);
}
</style>
<style scoped>
.instructions {
  top: 10px;
  left: calc(100vw + 10px);
  max-height: 154px !important;
}
</style>