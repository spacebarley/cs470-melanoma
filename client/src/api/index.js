import axios from 'axios'

const instance = axios.create({
  baseURL: "http://localhost:5000/",
  headers: {
    "Content-type": "application/json"
  }
});

export const melanoma = {
  request(file, sex, age, site) {
    var formData = new FormData();
    formData.append('file', file);
    formData.append('sex', sex)
    formData.append('age', age)
    formData.append('site', site)
    return instance.post('predict', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
      }
    })
  }
}
