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
      </md-card-content>
      <!--      <md-card-actions v-if="stats !== null" class="actions">-->
      <!--        <md-button class="vote-button md-raised" @click="verifyPrompt = true">VOTE</md-button>-->
      <!--      </md-card-actions>-->
    </md-card>
  </div>
</template>
<script>
import * as d3 from "d3";
import * as topojson from "topojson-client";
import {mapActions, mapGetters} from 'vuex';

export default {
  name: 'StatesCard',
  props: {
    title: String, // Title of the card.
    size: String, // Size of card in gutter.
    inGrid: Boolean, // Is this card in gutter?
    stats: Object, // Statistics
  },
  data: function () {
    return {
      counties: {},
      results: {}
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
      var height = width / 2.16; // Keep ratio of map.

      var projection = d3.geoAlbersUsa()
          .translate([width / 2, height / 2])
          .scale([width]);

      var path = d3.geoPath(projection)

      var color = {"DEM": "rgb(67,154,211)", "REP": "rgb(198,52,50)"};

      var svg = d3.select('#map-' + that.hashCode)
          .append("svg")
          .attr("width", width)
          .attr("height", height);

      // var div = d3.select('#map-' + that.hashCode).append("div")
      //     .attr("class", "tooltip")
      //     .style("opacity", 0);

      d3.json("/data/uscounties.json").then(json => {
            that.counties = json;

            d3.csv("/data/out.csv").then(data => {
              that.results = data.reduce((k, v) => ({...k, [v.id]: v}), {})

              svg.selectAll("path")
                  .data(topojson.feature(that.counties, that.counties.objects.counties).features)
                  .enter()
                  .append("path")
                  .attr("d", path)
                  .style("stroke", "#fff")
                  .style("stroke-width", "1")
                  .style("fill", function (d) {
                    if (that.results[d.id]) {
                      var result = that.results[d.id]["normalized_election_outcome"];
                      var value = result === "" ? null : result > .5 ? "DEM" : "REP";

                      if (value) return color[value];
                      return "#888";
                    }

                    return "#888";
                  });
            });

            // .style("opacity", 0.8)
            //     .on("mouseover", function (d) {
            //       var sel = d3.select(this);
            //       sel.moveToFront();
            //       d3.select(this).transition().duration(300).style({'opacity': 1, 'stroke': 'black', 'stroke-width': 1.5});
            //       div.transition().duration(300)
            //           .style("opacity", 1)
            //       div.text(pairNameWithId[d.id] + ": " + pairRateWithId[d.id])
            //           .style("left", (d3.event.pageX) + "px")
            //           .style("top", (d3.event.pageY - 30) + "px");
            //     })
            //     .on("mouseout", function () {
            //       var sel = d3.select(this);
            //       sel.moveToBack();
            //       d3.select(this)
            //           .transition().duration(300)
            //           .style({'opacity': 0.8, 'stroke': 'white', 'stroke-width': 1});
            //       div.transition().duration(300)
            //           .style("opacity", 0);
            //     });

            // d3.csv("/data/farms.csv").then(data => {
            //   for (var i = 0; i < data.length; i++) {
            //     that.states.features[i].party = data[i].party;
            //   }
            //
            //   svg.selectAll("path")
            //       .data(that.states.features)
            //       .enter()
            //       .append("path")
            //       .attr("d", path)
            //       .style("stroke", "#fff")
            //       .style("stroke-width", "1")
            //       .style("fill", function (d) {
            //         var value = d.party;
            //
            //         if (value) return color[value];
            //         return "#888";
            //       });
            // });
          }
      )
      ;
    }
  }
}
;
</script>
<style scoped>
.card-content {
  /*height: 530px !important;*/
}

.actions {
  justify-content: center !important;
}

div.tooltip {
  position: absolute;
  left: 75px;
  text-align: center;
  height: 16px;
  padding: 10px;
  font-size: 14px;
  background: #FFFFFF;
  border: 1px solid #989898;
  pointer-events: none;
}
</style>