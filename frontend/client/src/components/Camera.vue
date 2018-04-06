<template>
  <div>
    <br>
    <br>
    <h1 v-if="showlist">List Cameras</h1>
    <label v-if="showlist">Choose a camera from the list:
    <input list=results name="searchbar" v-model="searchbar" @change="findByIP" /></label>
    <b-button v-if="showlist" class="newButton" href="http://localhost:8080/camera/add">New...</b-button>
    <datalist v-if="showlist" id="results">
      <li v-for="camera in cameras" v-bind:key="camera.id">
        <option>{{camera.IPaddress}}</option>
      </li>
    </datalist>
    <br>
    <br>
    <table v-if="showlist" align="center">
      <tr>
        <td>ID</td>
        <td>IP Address</td>
        <td>POI</td>
      </tr>
      <tr v-for="camera in cameras" v-bind:key="camera.id">
        <td>
          {{camera.id}}
        </td>
        <td>
          {{camera.IPaddress}}
        </td>
        <td v-for="poi in pois" v-bind:key="poi.id" v-if="camera.POI_id === poi.id">
          {{poi.POIName}}
        </td>
        <td class="buttons">
          <b-button @click="updateButtonPressed(camera.id)">
            Update
          </b-button>
        </td>
        <td class="buttons">
          <b-button @click="deleteButtonPressed(camera.id)">
            Delete
          </b-button>
        </td>
      </tr>
    </table>
    <h1 v-if="showupdate">Edit Camera</h1>
    <input
      type="IPaddress"
      name="IPaddress"
      v-if="showupdate"
      v-model="cameraToUpdate.IPaddress"
      @input="validIP(cameraToUpdate.IPaddress)"
      :placeholder="cameraToUpdate.IPaddress"  />
      <br>
      <input list=poiresults v-if="showupdate" name="poiname" v-model="poiname" @focus="findByName" @input="findByName"/>
      <datalist id="poiresults">
        <li v-for="POIFound in pois" v-bind:key="POIFound.id">
          <option>{{POIFound.POIName}}</option>
        </li>
      </datalist>
      <!-- <input
      type="POI_id"
      name="POI_id"
      v-if="showupdate"
      v-model="cameraToUpdate.POI_id"
      :placeholder="cameraToUpdate.POI_id" /> -->
      <br>
    <b-button v-if="showupdate" :disabled="!valid" @click="updateConfirmPressed(cameraToUpdate.id)">Confirm</b-button>
    <b-button v-if="showupdate" @click="back">Cancel</b-button>
    <div class="error" v-html="error" />
    <div class="success" v-html="success" />
    <div class="nomatches" v-html="nomatches" />
  </div>
</template>

<script>
import axios from 'axios'
import FindByIPService from '@/services/FindByIPService'
import FindByNameService from '@/services/FindByNameService'
import DeleteCameraService from '@/services/DeleteCameraService'
import UpdateCameraService from '@/services/UpdateCameraService'
var validateip = require('validate-ip')
export default {
  data () {
    return {
      cameras: [],
      cameraToUpdate: [],
      pois: [],
      searchbar: '',
      poiname: '',
      valid: true,
      success: null,
      error: null,
      result: null,
      nomatches: null,
      showlist: true,
      showupdate: false
    }
  },
  methods: {
    getCameras () {
      this.cameras = this.getCamerasFromBackend()
    },
    getCamerasFromBackend () {
      const path = `http://localhost:5000/cameras`
      axios.get(path)
        .then(response => {
          this.cameras = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
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
    async getCameraByIDFromBackend (cameraid) {
      const path = `http://localhost:5000/cameras/description?arg=` + cameraid
      try {
        await axios.get(path)
          .then(response => {
            this.cameraToUpdate = response.data[0]
          })
          .catch(error => {
            console.log(error)
          })
      } catch (error) {
        console.log('something happened')
      }
    },
    back () {
      window.location.reload()
    },
    deleteButtonPressed (cameraID) {
      this.$dialog.confirm('Please confirm to continue')
        .then(function () {
          try {
            DeleteCameraService.deleteCamera(cameraID)
          } catch (error) {
            console.log('not going to allow') // not working
          }
          window.location.reload()
        })
    },
    async updateButtonPressed (cameraID) {
      this.showlist = false
      console.log('button pressed')
      this.cameraToUpdate = this.getCameraByIDFromBackend(cameraID)
      this.showupdate = true
      console.log('success')
    },
    async updateConfirmPressed (cameraID) {
      try {
        if (this.pois.length === 1 && this.pois[0].POIName === this.poiname) {
          await UpdateCameraService.updateCamera({
            IPaddress: this.cameraToUpdate.IPaddress,
            POI_id: this.pois[0].id
          }, this.cameraToUpdate.id)
          window.location.reload()
          this.success = 'Updated Successfully'
        } else {
          this.error = 'please select a valid POI'
          this.success = null
        }
      } catch (error) {
        this.error = error.response.data.error
      }
    },
    async findByIP () {
      try {
        await FindByIPService.findByIP({
          IPaddress: this.searchbar
        }).then(response => {
          this.cameras = response.data
        })
        if (this.cameras.length !== 0) {
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
  },
  created () {
    this.getCameras()
    this.getPOIs()
  }
}
</script>

<style scoped>
.error {
  color: red;
}
.nomatches {
  color: red;
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
