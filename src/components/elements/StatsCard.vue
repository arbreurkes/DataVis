<template>
  <div :class="[{'md-layout-item': inGrid}, size]">
    <md-card ref="card">
      <md-card-actions class="md-alignment-left">
        <div class="md-title">{{ title }}</div>
        <md-icon class="info-icon">info
          <md-tooltip md-direction="left">{{ title }} Statistics</md-tooltip>
        </md-icon>
      </md-card-actions>
      <md-card-content class="card-content">
        <div :id="'map-' + this.hashCode"></div>
        <!--        <md-empty-state-->
        <!--            v-if="stats === null"-->
        <!--            md-icon="track_changes"-->
        <!--            :md-label="'No ' + title + ' Statistics'">-->
        <!--        </md-empty-state>-->
      </md-card-content>
      <!--      <md-card-actions v-if="stats !== null" class="actions">-->
      <!--        <md-button class="vote-button md-raised" @click="verifyPrompt = true">VOTE</md-button>-->
      <!--      </md-card-actions>-->
    </md-card>
  </div>
</template>
<script>
import * as d3 from "d3";
import {mapActions, mapGetters} from 'vuex';

export default {
  name: 'StatsCard',
  props: {
    title: String, // Title of the card.
    size: String, // Size of card in gutter.
    inGrid: Boolean, // Is this card in gutter?
    stats: Object, // Statistics
  },
  data: function () {
    return {
      states: {}
    }
  },
  computed: {
    hashCode: function () {
      return window.hashCode(Math.round(Math.random() * 100000) + "")
    }
  },
  mounted: function () {
    this.$nextTick(() => {
      this.initializeMap()
    })
  },
  methods: {
    ...mapActions([]),
    ...mapGetters([]),
    initializeMap: function () {
      var that = this;
      var width = this.$refs.card.$el.scrollWidth - 32;
      var height = 500;

      var projection = d3.geoAlbersUsa()
          .translate([width / 2, height / 2])
          .scale([1000]);

      var path = d3.geoPath(projection)

      var color = {"DEM": "rgb(67,154,211)", "REP": "rgb(198,52,50)"};

      var svg = d3.select('#map-' + that.hashCode)
          .append("svg")
          .attr("width", width)
          .attr("height", height);

      d3.json("/data/usstates.json").then(json => {
        that.states = json;

        d3.csv("/data/statesElection.csv").then(data => {
          for (var i = 0; i < data.length; i++) {
            that.states.features[i].party = data[i].party;
          }

          svg.selectAll("path")
              .data(that.states.features)
              .enter()
              .append("path")
              .attr("d", path)
              .style("stroke", "#fff")
              .style("stroke-width", "1")
              .style("fill", function (d) {
                var value = d.party;

                if (value) return color[value];
                return "#888";
              });
        });
      });
    }
  }
};
</script>
<style scoped>
.card-content {
  height: 530px !important;
}

.actions {
  justify-content: center !important;
}
</style>