import Api from '@/services/Api'

export default {
  updateCamera (cameraInfo, cameraID) {
    return Api().put('/cameras/update?arg=' + cameraID, cameraInfo)
  }
}
