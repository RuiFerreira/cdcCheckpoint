import Api from '@/services/Api'

export default {
  addPOI (poiInfo) {
    return Api().post('/pois/add', poiInfo)
  }
}
