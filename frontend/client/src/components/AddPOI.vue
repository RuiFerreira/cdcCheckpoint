<template>
  <div>
  <br>
  <br>
    <h1>Add POI</h1>

    <input
      type="text"
      name="POIName"
      v-model="POIName"
      placeholder="Input a Name" />
      <br>
      <input
      type="geoLat"
      name="geoLat"
      v-model="geoLat"
      placeholder="Input Latitude"
      v-on:input="geoLatValidated()"/>
      <br>
      <input
      type="geoLong"
      name="geoLong"
      v-model="geoLong"
      placeholder="Input Longitude"
      v-on:input="geoLongValidated()"/>
      <br>
      <div class="error" v-html="error" />
      <div class="success" v-html="success" />
      <br>
      <button  :disabled="!validated"
        @click="addPOI">
        Add POI
      </button>
  </div>
</template>

<script>
import AddPOIService from '@/services/AddPOIService'
export default {
  data () {
    return {
      POIName: '',
      geoLat: '',
      geoLong: '',
      location: '',
      validLat: false,
      validLong: false,
      validated: false,
      error: null,
      success: null
    }
  },
  methods: {
    async addPOI () {
      try {
        await AddPOIService.addPOI({
          POIName: this.POIName,
          geoLat: this.geoLat,
          geoLong: this.geoLong
        })
        this.success = 'Added Successfully'
        this.$router.push('../poi')
      } catch (error) {
        this.error = error.response.data.error
      }
    },
    geoLatValidated () {
      if (this.geoLat > -90 && this.geoLat < 90) {
        this.validLat = true
      } else {
        this.validLat = false
      }
      this.submitvalidated()
    },
    geoLongValidated () {
      if (this.geoLong > -180 && this.geoLong < 180) {
        this.validLong = true
      } else {
        this.validLong = false
      }
      this.submitvalidated()
    },
    submitvalidated () {
      if (this.validLat === true && this.validLong === true) {
        this.validated = true
      } else {
        this.validated = false
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
