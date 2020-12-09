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
        <div id="scatterPlot"></div>
      </md-card-content>
    </md-card>
  </div>
</template>
<script>
import {mapActions, mapGetters} from 'vuex';
// import * as d3 from "d3";

export default {
  name: 'ScatterCard',
  props: {
    title: String, // Title of the card.
    size: String, // Size of card in gutter.
    inGrid: Boolean, // Is this card in gutter?
  },
  data: function() {
    return {
      x: {},
      y: {}
    }
  },
  computed: {

  },
  mounted: function () {
    this.initializePlot()
  },
  methods: {
    ...mapActions([]),
    ...mapGetters([]),
    initializePlot: function () {
      // // set the dimensions and margins of the graph
      // var margin = {top: 10, right: 30, bottom: 30, left: 60},
      //         width = 460 - margin.left - margin.right,
      //         height = 400 - margin.top - margin.bottom;
      //
      // // append the svg object to the body of the page
      // var svg = d3.select("#scatterPlot")
      //         .append("svg")
      //         .attr("width", width + margin.left + margin.right)
      //         .attr("height", height + margin.top + margin.bottom)
      //         .append("g")
      //         .attr("transform",
      //                 "translate(" + margin.left + "," + margin.top + ")");
      // //Read example data
      // d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/2_TwoNum.csv", function(data) {
      //
      //   // Add X axis
      //   var x = d3.scaleLinear()
      //           .domain([0, 4000])
      //           .range([ 0, width ]);
      //   svg.append("g")
      //           .attr("transform", "translate(0," + height + ")")
      //           .call(d3.axisBottom(x));
      //
      //   // Add Y axis
      //   var y = d3.scaleLinear()
      //           .domain([0, 500000])
      //           .range([ height, 0]);
      //   svg.append("g")
      //           .call(d3.axisLeft(y));
      //
      //   // Add dots
      //   svg.append('g')
      //           .selectAll("dot")
      //           .data(data)
      //           .enter()
      //           .append("circle")
      //           .attr("cx", function (d) { return x(d.GrLivArea); } )
      //           .attr("cy", function (d) { return y(d.SalePrice); } )
      //           .attr("r", 1.5)
      //           .style("fill", "#69b3a2")
      //
      // })
    }
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