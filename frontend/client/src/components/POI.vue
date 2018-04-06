<template>
  <div>
  <br>
  <br>
    <h1 v-if="showlist">POIS</h1>
    <label v-if="showlist">Choose POI from the list:
    <input list=results name="searchbar" v-model="searchbar" @focus="findByName" @change="findByName" /></label>
    <b-button v-if="showlist" class="newButton" href="http://localhost:8080/poi/add">New...</b-button>
    <datalist id="results">
      <li v-for="POIFound in pois" v-bind:key="POIFound.id">
        <option>{{POIFound.POIName}}</option>
      </li>
    </datalist>
    <br>
    <br>
    <table align="center" v-if="showlist" >
      <tr>
        <td>ID</td>
        <td>Name</td>
        <td>Latitude</td>
        <td>Longitude</td>
      </tr>
      <tr v-for="poi in pois" v-bind:key="poi.id">
        <td>
          {{poi.id}}
        </td>
        <td>
          {{poi.POIName}}
        </td>
        <td>
          {{poi.geoLat}}
        </td>
        <td>
          {{poi.geoLong}}
        </td>
        <td class="buttons">
          <b-button @click="updateButtonPressed(poi.id)">
            Update
          </b-button>
        </td>
        <td class="buttons">
          <b-button @click="deleteButtonPressed(poi.id)">
            Delete
          </b-button>
        </td>
      </tr>
    </table>
    <h1 v-if="showupdate">Edit POI</h1>
    <input
      type="POIName"
      name="POIName"
      v-if="showupdate"
      v-model="poiToUpdate.POIName"
      :placeholder="poiToUpdate.POIName"  />
      <br>
      <input
      type="geoLat"
      name="geoLat"
      v-if="showupdate"
      v-model="poiToUpdate.geoLat"
      :placeholder="poiToUpdate.geoLat" />
      <br>
      <input
      type="geoLong"
      name="geoLong"
      v-if="showupdate"
      v-model="poiToUpdate.geoLong"
      :placeholder="poiToUpdate.geoLong" />
    <br>
    <b-button v-if="showupdate" @click="updateConfirmPressed(poiToUpdate.id)">Confirm</b-button>
    <b-button v-if="showupdate" @click="back">Cancel</b-button>
    <div class="error" v-html="error" />
    <div class="success" v-html="success" />
    <div class="nomatches" v-html="nomatches" />
  </div>
</template>

<script>
import axios from 'axios'
import FindByNameService from '@/services/FindByNameService'
import DeletePOIService from '@/services/DeletePOIService'
import UpdatePOIService from '@/services/UpdatePOIService'

export default {
  data () {
    return {
      pois: [],
      poiToUpdate: [],
      searchbar: '',
      success: null,
      error: null,
      result: null,
      nomatches: null,
      showlist: true,
      showupdate: false
    }
  },
  methods: {
    getPOIs () {
      this.pois = this.getPOIsFromBackend()
    },
    getPOIsFromBackend () {
      const path = `http://localhost:5000/pois`
      axios.get(path)
        .then(response => {
          this.pois = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    back () {
      window.location.reload()
    },
    async getPOIByIDFromBackend (poiid) {
      const path = `http://localhost:5000/pois/description?arg=` + poiid
      try {
        await axios.get(path)
          .then(response => {
            this.poiToUpdate = response.data[0]
          })
          .catch(error => {
            console.log(error)
          })
      } catch (error) {
        console.log('something happened')
      }
    },
    deleteButtonPressed (poiID) {
      this.$dialog.confirm('Please confirm to continue')
        .then(function () {
          try {
            DeletePOIService.deletePOI(poiID)
          } catch (error) {
            console.log('not going to allow') // not working
          }
          window.location.reload()
        })
    },
    async updateButtonPressed (poiID) {
      this.showlist = false
      this.poiToUpdate = this.getPOIByIDFromBackend(poiID)
      this.showupdate = true
    },
    async updateConfirmPressed (poiID) {
      try {
        await UpdatePOIService.updatePOI({
          POIName: this.poiToUpdate.POIName,
          geoLat: this.poiToUpdate.geoLat,
          geoLong: this.poiToUpdate.geoLong
        }, poiID)
        window.location.reload()
      } catch (error) {
        this.error = error.response.data.error
      }
      this.success = 'Updated Successfully'
    },
    async findByName () {
      try {
        await FindByNameService.findByName({
          POIName: this.searchbar
        }).then(response => {
          this.pois = response.data
        })
        if (this.pois.length !== 0) {
          this.success = 'Found Successfully'
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
  },
  created () {
    this.getPOIs()
  }
}
</script>

<style scoped>
.error {
  color: red;
}
.nomatches {
  color: yellow;
}
.success {
  color: green;
}
table{
  align: center;
  width: 80%;
}
table td{
  position: relative;
  border: 1px solid #000;
  padding: 2px;
}
.buttons {
  position: relative;
  border: none;
  padding: 3px;
  width:5%;
}
.newButton {
  float: right;
  margin-right: 12%;
  padding: 3px;
  width: 10%;
}
</style>
