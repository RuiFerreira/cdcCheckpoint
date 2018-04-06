<template>
  <div>
  <br>
  <br>
    <h1>List Predictions</h1>
    <!-- <b-button class="newButton" href="http://localhost:8080/prediction/add">New...</b-button> -->
    <table align="center">
      <tr>
        <td>ID</td>
        <td>Prediction</td>
        <td>Camera ID</td>
        <td>Created at</td>
      </tr>
      <tr v-for="prediction in predictions" v-bind:key="prediction.id">
        <td>
          {{prediction.id}}
        </td>
        <td>
          {{prediction.Prediction}}
        </td>
        <td>
          {{prediction.Camera_id}}
        </td>
        <td>
          {{prediction.Time}}
        </td>
      </tr>
    </table>
  <br>
  <div class="error" v-html="error" />
  <div class="success" v-html="success" />
  <div class="nomatches" v-html="nomatches" />
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      predictions: [],
      success: null,
      error: null,
      result: null,
      nomatches: null
    }
  },
  methods: {
    getPredictions () {
      this.pois = this.getPredictionsFromBackend()
    },
    getPredictionsFromBackend () {
      const path = `http://localhost:5000/predictions`
      axios.get(path)
        .then(response => {
          this.predictions = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.getPredictions()
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
