import axios from 'axios';

// Adapted from: https://forum.vuejs.org/t/how-to-set-base-url-right/2540

export const HTTP = axios.create({
    baseURL: 'http://127.0.0.1:5000/api/',
    timeout: 5000,
    headers: {'Content-Type': 'application/json'}
})