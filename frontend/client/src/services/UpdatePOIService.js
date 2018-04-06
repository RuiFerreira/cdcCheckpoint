import Api from '@/services/Api'

export default {
  updatePOI (poiInfo, poiID) {
    return Api().put('/pois/update?arg=' + poiID, poiInfo)
  }
}
