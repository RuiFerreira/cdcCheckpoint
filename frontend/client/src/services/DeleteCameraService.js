import Api from '@/services/Api'

export default {
  deleteCamera (cameraID) {
    return Api().delete('/cameras/delete?arg=' + cameraID)
  }
}
