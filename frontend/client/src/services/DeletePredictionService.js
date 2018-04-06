import Api from '@/services/Api'

export default {
  deletePrediction (predictionID) {
    return Api().delete('/predictions/delete?arg=' + predictionID)
  }
}
