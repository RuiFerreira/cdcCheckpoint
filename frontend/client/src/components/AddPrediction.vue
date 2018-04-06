<template>
  <div>
  <br>
  <br>
    <h1>Add Prediction</h1>

    <select v-model="Prediction" name="Prediction">
      <option disabled value="">Please select one</option>
      <option>low_density</option>
      <option>medium_low_density</option>
      <option>medium_density</option>
      <option>medium_high_density</option>
      <option>high_density</option>
    </select>
      <br>
      <input
      type="number"
      name="Camera_id"
      v-model="Camera_id"
      placeholder="Camera_id"
      min="1"
      step="1" />
      <br>
      <div class="error" v-html="error" />
      <div class="success" v-html="success" />
      <br>
      <button
        @click="addPrediction">
        Add Prediction
      </button>
  </div>
</template>

<script>
import AddPredictionService from '@/services/AddPredictionService'
export default {
  data () {
    return {
      Prediction: '',
      Camera_id: '',
      error: null,
      success: null
    }
  },
  methods: {
    async addPrediction () {
      try {
        await AddPredictionService.addPrediction({
          Prediction: this.Prediction,
          Camera_id: this.Camera_id
        })
        this.success = 'Added Successfully'
        this.$router.push('../prediction')
      } catch (error) {
        this.error = 'Please select valid camera'
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
