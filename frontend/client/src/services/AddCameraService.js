import Api from '@/services/Api'

export default {
  addCamera (cameraInfo) {
    return Api().post('/cameras/add', cameraInfo)
  }
}
