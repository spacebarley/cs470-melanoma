import axios from 'axios'

const instance = axios.create({
  baseURL: "http://localhost:5000/",
  headers: {
    "Content-type": "application/json"
  }
});

export const melanoma = {
  request(file) {
    var formData = new FormData();
    formData.append('file', file);
    return instance.post('predict', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
      }
    })
  }
}
