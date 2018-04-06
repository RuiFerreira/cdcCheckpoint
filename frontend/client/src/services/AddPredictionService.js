import Api from '@/services/Api'

export default {
  addPrediction (predictionInfo) {
    return Api().post('/predictions/add', predictionInfo)
  }
}
