<template>
  <div id="app">
    <md-toolbar class="top-bar md-dense">
      <md-button class="md-icon-button" @click="showNavigation = !showNavigation">
        <md-icon>menu</md-icon>
      </md-button>
      <span class="md-title">2020 Election HQ - {{ this.$route.name }}</span>
      <md-avatar class="md-avatar-icon">
      </md-avatar>
      <md-button class="user-info" @click="disclaimerPrompt = true">
        Disclaimer
      </md-button>
    </md-toolbar>

    <md-drawer class="md-drawer md-drawer--modal" :md-active.sync="showNavigation" md-swipeable>
      <md-toolbar class="md-transparent" md-elevation="0">
        <span class="md-title">Select attributes</span>
      </md-toolbar>
      <md-list>
        <md-list-item>
          <md-field>
            <label for="statOne">Stat one</label>
            <md-select v-model="statOne" name="statOne" id="statOne">
              <md-option value="election_lead">election_lead</md-option>
              <md-option v-for="a in attributes" :key="a" :value="a" :disabled="statTwo === a">{{ a }}</md-option>
            </md-select>
          </md-field>
        </md-list-item>
        <md-list-item>
          <md-field>
            <label for="statTwo">Stat two</label>
            <md-select v-model="statTwo" name="statTwo" id="statTwo">
              <md-option value="None">None</md-option>
              <md-option v-for="a in attributes" :key="a" :value="a" :disabled="statOne === a">{{ a }}</md-option>
            </md-select>
          </md-field>
        </md-list-item>
      </md-list>
    </md-drawer>
    <md-content class="main-content" id="main-content">
      <router-view></router-view>
    </md-content>
    <md-dialog :md-active.sync="disclaimerPrompt">
      <md-dialog-title>Disclaimer</md-dialog-title>
      <md-dialog-content>
        No rights can be derived from the information on this website.
      </md-dialog-content>
      <md-dialog-actions>
        <md-button class="md-primary md-raised confirm-button" @click="disclaimerPrompt = false">
          close
        </md-button>
      </md-dialog-actions>
    </md-dialog>
  </div>
</template>
<script>
import {mapGetters, mapMutations} from 'vuex'

export default {
  name: 'app',
  components: {},
  computed: {
    attributes: function () {
      return this.getAttributes();
    }
  },
  watch: {
    statOne: function() {
      this.setStatOne(this.statOne);
    },
    statTwo: function() {
      this.setStatTwo(this.statTwo);
    }
  },
  data: () => ({
    showNavigation: false, // Show the navigation drawer.
    disclaimerPrompt: false, // Show disclaimer or not.
    statOne: "election_lead",
    statTwo: "None"
  }),
  mounted() { // On first initialization.
  },
  methods: {
    ...mapGetters(['getAttributes']),
    ...mapMutations(['setStatOne', 'setStatTwo']),
  }
}
</script>
<style>
body {
  height: 100%;
  overflow: hidden;
  background-color: var(--background-color);
}

:root {
  --MSU-green: #243E36;
  --metallic-gold: #C2A83E;
  --forest-green: #7CA982;
  --nyanza: #E0EEC6;
  --ivory: #F1F7ED;
  --ivory-white: #FFFFFF;
  --background-color: #FFFFFF;

  /* Override MDC theme colors */
  --mdc-theme-primary: var(--MSU-green) !important;
  --mdc-theme-secondary: var(--metallic-gold) !important;
}

#app {
  font-family: 'Roboto', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.top-bar {
  background-color: var(--mdc-theme-primary) !important;
}

.top-bar .md-title, .md-toolbar.md-theme-default .md-icon {
  color: var(--ivory-white) !important;
}

.md-avatar {
  margin-right: 0 !important;
  background: var(--mdc-theme-primary) !important;
}

.user-info {
  padding-left: 8px;
  text-align: center;
  color: white !important;
  text-underline: white !important;
}

.md-overlay {
  top: 48px !important;
  height: calc(100vh - 48px) !important;
}

.md-drawer {
  z-index: 1000 !important;
  top: 48px !important;
  width: 200px !important;
  height: calc(100vh - 48px) !important;
}

.md-list.md-theme-default .router-link-active .md-list-item-content {
  color: var(--mdc-theme-secondary) !important;
}

.md-select-menu {
  z-index: 1001 !important;
}

.md-list.md-theme-default .md-selected .md-list-item-content, .md-list.md-theme-default .router-link-active .md-list-item-content {
  color: var(--mdc-theme-secondary) !important;
}

.confirm-button, .empty-state-button {
  background-color: var(--mdc-theme-secondary) !important;
}

.info-icon {
  font-family: 'Material Icons Outlined' !important;
  margin-right: 0 !important;
}

.content {
  height: 100%;
  width: 100%;
  max-width: 100vw;
}

.md-dialog-container {
  transform: none !important;
}

.md-content {
  padding-bottom: 0 !important;
}
</style>
