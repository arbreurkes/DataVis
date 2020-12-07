<template>
  <div ref="card">
    <span class="map-title">
          <span :style="statOne === 'DEM_votes' ? 'color:#439AD3;' : 'color:#C63432;'">
            {{ statOne === "normalized_election_outcome" ? "Republican" : statOne }}</span>
            {{ statOne === 'normalized_election_outcome' || statTwo !== 'None' ? "vs. " : "" }}
          <span v-if="statOne === 'normalized_election_outcome' || statTwo !== 'None'" style="color:#439AD3;">
            {{ statOne === "normalized_election_outcome" ? "Democratic" : statTwo }}</span>
            {{ statOne === "normalized_election_outcome" ? "lead " : "" }}during 2020 presidential election
        </span>
    <div :id="'map-' + this.hashCode"></div>
  </div>
</template>
<script>
import * as d3 from "d3";
import * as topojson from "topojson-client";
import {legendColor} from 'd3-svg-legend'
import {mapActions, mapGetters} from 'vuex';

export default {
  name: 'StatesCard',
  props: {
    title: String, // Title of the card.
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
    },
    statOne: function () {
      return this.getStatOne()
    },
    statTwo: function () {
      return this.getStatTwo()
    }
  },
  watch: {
    statOne: function () {
      this.initializeMap();
    },
    statTwo: function () {
      // if (this.statOne) this.initializeMap();
    }
  },
  mounted: function () {
    this.$nextTick(() => {
      d3.select("body").append("div")
          .attr("id", "county-tt")
          .attr("class", "tooltip")
          .style("opacity", 0);

      this.initializeMap()
    })
  },
  methods: {
    ...mapActions([]),
    ...mapGetters(['getStatOne', 'getStatTwo']),
    initializeMap: function () {
      var that = this;
      var width = this.$refs.card.scrollWidth;
      var height = width / 2.16; // Keep ratio of map.

      var projection = d3.geoAlbersUsa()
          .translate([width / 2, height / 2])
          .scale([width]);

      var path = d3.geoPath(projection)

      d3.select('#map-' + that.hashCode).html("")
      var svg = d3.select('#map-' + that.hashCode)
          .append("svg")
          .attr("width", width)
          .attr("height", height + 36)
          .attr("class", "map-svg");

      var div = d3.select("#county-tt")

      d3.selection.prototype.moveToFront = function () {
        return this.each(function () {
          this.parentNode.appendChild(this);
        });
      };

      d3.selection.prototype.moveToBack = function () {
        return this.each(function () {
          var firstChild = this.parentNode.firstChild;
          if (firstChild) {
            this.parentNode.insertBefore(this, firstChild);
          }
        });
      };

      d3.json("/data/uscounties.json").then(json => {
        that.counties = json;

        d3.csv("/data/countyData.csv").then(data => {
          that.results = data.reduce((k, v) => ({...k, [v.id]: v}), {})
          var stat = data.map((x) => parseInt(x[that.statOne]));

          var color = null
          if (that.statOne === "normalized_election_outcome" && that.statTwo === "None") {
            color = d3.scaleQuantile()
                .domain([0, .40, .45, .5, .55, .60, 1])
                .range(["#C63432", "#E37D71", "#F6BEB6", "#C8DCf1", "#8DBAE2", "#439AD3"]);
          } else if (that.statTwo === "None" && that.statOne === "DEM_votes") {
            color = d3.scaleLinear()
                .domain([0, Math.max(...stat)])
                .range(["#FFFFFF", "#439AD3"]);
          } else if (that.statTwo === "None") {
            color = d3.scaleLinear()
                .domain([0, Math.max(...stat)])
                .range(["#FFFFFF", "#C63432"]);
          }

          svg.selectAll("path")
              .data(topojson.feature(that.counties, that.counties.objects.counties).features)
              .enter()
              .append("path")
              .attr("d", path)
              .attr("id", function (d) {
                return d.id
              })
              .style("stroke", "#FFF")
              .style("stroke-width", "1")
              .style("fill", function (d) {
                if (that.results[d.id]) {
                  var result = that.results[d.id][that.statOne];
                  var value = result === "" ? null : result > .5 ? "DEM" : "REP";

                  if (value) return color(result);
                  return "#888";
                }

                return "#888";
              })
              .on("mouseover", function (d) {
                var sel = d3.select(this);
                sel.moveToFront();
                d3.select(this).transition().duration(300)
                    .style('stroke', '#000')
                    .style('stroke-width', 1.5);
                div.transition().duration(300)
                    .style("opacity", 1)
                div.text(that.results[this.id] !== undefined
                    ? that.results[this.id]["county"] : "No Data")
                    .style("left", (d.pageX) + "px")
                    .style("top", (d.pageY -30) + "px")
                    .style("opacity", 1);
              })
              .on("mouseout", function () {
                var sel = d3.select(this);
                sel.moveToBack();
                d3.select(this)
                    .transition().duration(300)
                    .style('stroke', '#FFF')
                    .style('stroke-width', 1);
                div.transition().duration(300)
                    .style("opacity", 0);
              });

          svg.append("g")
              .attr("class", "legendLinear")
              .attr("transform", "translate(" + (width / 2 - 110) + ", " + height + ")");

          var legendLinear = legendColor()
              .shapeWidth(30)
              .cells(6)
              .labels((d) => {
                if (that.statOne === "normalized_election_outcome")
                  return ["20+%", ">20%", ">10%", ">10%", ">20%", "20+%"][d.i];
                else if (d.domain[1] > 10000000) {
                  return (parseInt(d.generatedLabels[d.i]) / 1000000).toFixed(0) + "M";
                } else if (d.domain[1] > 1000000) {
                  return (parseInt(d.generatedLabels[d.i]) / 1000000).toFixed(1) + "M";
                } else if (d.domain[1] > 10000) {
                  return (parseInt(d.generatedLabels[d.i]) / 1000).toFixed(0) + "K";
                } else if (d.domain[1] > 1000) {
                  return (parseInt(d.generatedLabels[d.i]) / 1000).toFixed(1) + "K";
                } else if (d.domain[1] <= 100 && d.domain[1] > 10) {
                  return (parseInt(d.generatedLabels[d.i])).toFixed(0) + "%";
                } else return (parseInt(d.generatedLabels[d.i])).toFixed(1) + "%";
              })
              .labelFormat(d3.format(".2f"))
              .orient('horizontal')
              .scale(color);

          svg.select(".legendLinear")
              .call(legendLinear);
        });
      });
    }
  }
}
;
</script>
<style>
.map-svg {
  margin: 0 auto;
}

.map-title {
  display: inline-block;
  width: 100%;
  text-align: center;
  font-size: 12pt !important;
}

.label {
  line-height: 8pt;
  font-size: 8pt;
}

.actions {
  justify-content: center !important;
}

div.tooltip {
  position: absolute;
  left: 75px;
  text-align: center;
  height: 36px;
  line-height: 16px;
  padding: 10px;
  font-size: 14px;
  background: #FFFFFF;
  border: 1px solid #989898;
  pointer-events: none;
}
</style>