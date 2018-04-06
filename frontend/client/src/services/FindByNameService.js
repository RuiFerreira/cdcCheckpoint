import Api from '@/services/Api'

export default {
  findByName (pois) {
    return Api().get('/pois/findbyname?arg=' + pois.POIName)
  }
}
