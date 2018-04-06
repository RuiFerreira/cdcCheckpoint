<template>
  <div>
  <br>
  <br>
    <h1>Add Camera</h1>

    <input
      type="IPaddress"
      name="IPaddress"
      v-model="IPaddress"
      placeholder="IPaddress"
      v-on:change="validIP(IPaddress)"
      v-on:input="validIP(IPaddress)" />
      <br>
      <input list=poiresults name="poiname" v-model="poiname" @focus="findByName" @input="findByName"/>
      <datalist id="poiresults">
        <li v-for="POIFound in pois" v-bind:key="POIFound.id">
          <option>{{POIFound.POIName}}</option>
        </li>
      </datalist>
      <br>
      <div class="error" v-html="error" />
      <div class="success" v-html="success" />
      <br>
      <button :disabled="!valid" @click="addCamera">
        Add Camera
      </button>
  </div>
</template>

<script>
import AddCameraService from '@/services/AddCameraService'
import FindByNameService from '@/services/FindByNameService'
var validateip = require('validate-ip')
export default {
  data () {
    return {
      IPaddress: '',
      POI_id: '',
      poiname: '',
      pois: [],
      error: null,
      valid: false,
      success: null
    }
  },
  methods: {
    async addCamera () {
      try {
        await AddCameraService.addCamera({
          IPaddress: this.IPaddress,
          POI_id: this.pois[0].id
        })
        this.success = 'Added Successfully'
        this.$router.push('../camera')
      } catch (error) {
        this.error = 'Please select an existing Point of Interest'
      }
    },
    async validIP (ip) {
      const validation = await validateip(ip)
      if (validation === true) {
        this.valid = true
      } else {
        this.valid = false
      }
    },
    async findByName () {
      try {
        await FindByNameService.findByName({
          POIName: this.poiname
        }).then(response => {
          this.pois = response.data
        })
        if (this.pois.length !== 0) {
          this.error = null
          this.nomatches = null
        } else {
          this.error = null
          this.success = null
          this.nomatches = 'No matches found'
        }
      } catch (error) {
        this.error = 'Something happened'
        this.success = null
        this.nomatches = null
      }
    }
  }
}
</script>

<style scoped>
.error {
  color: red;
}
.success {
  color: green;
}
</style>
