<template>
  <div id="app">
    <b-navbar type="dark" variant="primary" toggleable>
    <b-navbar-toggle target="nav_dropdown_collapse"></b-navbar-toggle>
      <b-collapse is-nav id="nav_dropdown_collapse">
        <b-navbar-nav>
          <b-nav-item href="/">Home</b-nav-item>
          <b-nav-item href="/map">Map</b-nav-item>
          <b-nav-item-dropdown text="List" left>
            <b-dropdown-item href="/poi">poi</b-dropdown-item>
            <b-dropdown-item href="/camera">camera</b-dropdown-item>
            <b-dropdown-item href="/prediction">prediction</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item-dropdown text="Create" left>
            <b-dropdown-item href="/poi/add">poi</b-dropdown-item>
            <b-dropdown-item href="/camera/add">camera</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item href="/about">About</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>
