import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex); // Use Vuex to store state.


export default new Vuex.Store({
    state: { // The state in which all global variables are stored
        attributes: ["DEM_votes","REP_votes","dem_votes_%","rep_votes_%","TotalPop","percentageMen","percentageWomen",
            "Men","Women","Hispanic","White","Black","Native","Asian","Pacific","IncomePerCap","Income","Poverty",
            "ChildPoverty","Unemployment"],
        statOne: "election_lead",
        statTwo: "None"
    },
    getters: {  // Getters for each variable in state.
        getAttributes: (state) => state.attributes,
        getStatOne: (state) => state.statOne,
        getStatTwo: (state) => state.statTwo
    },
    mutations: { // Setters for each variable in state.
        setStatOne: (state, value) => (state.statOne = value),
        setStatTwo: (state, value) => (state.statTwo = value)
    },
    actions: {} // Actions, commit to state and notify system. All except one are asynchronous.
});