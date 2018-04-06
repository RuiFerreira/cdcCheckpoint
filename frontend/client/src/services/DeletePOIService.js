import Api from '@/services/Api'

export default {
  deletePOI (poiID) {
    return Api().delete('/pois/delete?arg=' + poiID)
  }
}
