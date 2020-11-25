import Vuex from 'vuex';
import Vue from 'vue';
import axios from 'axios';

Vue.use(Vuex); // Use Vuex to store state.


export default new Vuex.Store({
    state: { // The state in which all global variables are stored
        snackbarMessage: "", // Message to show in snackbar, non-empty triggers showing snackbar.
    },
    getters: {  // Getters for each variable in state.
        getSnackbarMessage: (state) => state.snackbarMessage,
    },
    mutations: { // Setters for each variable in state.
        setSnackbarMessage: (state, value) => (state.snackbarMessage = value),
    },
    actions: { // Actions, commit to state and notify system. All except one are asynchronous.
        updateVerifyVotes({commit}, keyValue) { // Update the verify votes of the worker.
            commit('setVerifyVotes', keyValue);
        },
        async loadExistingSnapshots({commit}) { // Load the existing find annotations from file.
            axios.get('/resources/findAnnotations.json').then(response => {
                commit('setExistingSnapshots', response.data)
            });
        },
        async loadVerifySnapshots({commit}) { // Load the verify annotation from file.
            axios.get('/resources/verifySnapshots.json').then(response => {
                commit('setVerifySnapshots', response.data)
            });
        },
        async loadFixSnapshots({commit}) { // Load the fix annotations from file.
            axios.get('/resources/fixSnapshots.json').then(response => {
                commit('setFixSnapshots', response.data)
            });
        },

    }
});