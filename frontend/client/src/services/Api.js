// used to setup a connector to the back end
import axios from 'axios'

export default () => {
  return axios.create({
    baseURL: 'http://localhost:5000/'
  })
}
