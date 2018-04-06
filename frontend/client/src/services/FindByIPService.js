import Api from '@/services/Api'

export default {
  findByIP (ip) {
    return Api().get('/cameras/findbyip?arg=' + ip.IPaddress)
  }
}
